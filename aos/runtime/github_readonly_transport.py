import os
import urllib.request
import urllib.error
import json
import time
import socket
from typing import Dict, Any
from types import MappingProxyType

NETWORK_TIMEOUT_SECONDS = 30
MAXIMUM_RESPONSE_BYTES = 10 * 1024 * 1024
TRANSPORT_RETRY_LIMIT = 3

PREDEFINED_GRAPHQL_QUERIES = MappingProxyType({
    "review_threads": """
        query($owner: String!, $name: String!, $number: Int!, $cursor: String) {
          repository(owner: $owner, name: $name) {
            pullRequest(number: $number) {
              reviewThreads(first: 100, after: $cursor) {
                pageInfo { hasNextPage endCursor }
                totalCount
                nodes {
                  isResolved
                  comments(first: 1) { nodes { body } }
                }
              }
            }
          }
        }
    """
})

class GitHubTransportError(Exception):
    def __init__(self, error_code: str, category: str, http_status: int, retryable: bool, message: str):
        self.error_code = error_code
        self.category = category
        self.http_status = http_status
        self.retryable = retryable
        self.message = message
        super().__init__(self.message)

class NoCrossHostRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not newurl.startswith("https://api.github.com/"):
            raise urllib.error.URLError(f"Redirect to unauthorized host blocked: {newurl}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)

def _get_token() -> str:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise GitHubTransportError(
            error_code="GITHUB_AUTHENTICATION_UNAVAILABLE",
            category="AUTH",
            http_status=0,
            retryable=False,
            message="GitHub token missing from environment"
        )
    return token

def _execute_request(req: urllib.request.Request, opener: urllib.request.OpenerDirector) -> Any:
    retries = 0
    while retries <= TRANSPORT_RETRY_LIMIT:
        try:
            with opener.open(req, timeout=NETWORK_TIMEOUT_SECONDS) as response:
                content_length = response.getheader('Content-Length')
                if content_length and int(content_length) > MAXIMUM_RESPONSE_BYTES:
                    raise GitHubTransportError("OVERSIZED_RESPONSE", "LIMIT", response.getcode(), False, "Response too large")
                
                body = response.read(MAXIMUM_RESPONSE_BYTES + 1)
                if len(body) > MAXIMUM_RESPONSE_BYTES:
                    raise GitHubTransportError("OVERSIZED_RESPONSE", "LIMIT", response.getcode(), False, "Response too large")
                    
                try:
                    return json.loads(body.decode('utf-8'))
                except (json.JSONDecodeError, UnicodeDecodeError):
                    raise GitHubTransportError("MALFORMED_JSON", "PARSING", response.getcode(), False, "Invalid JSON in response")
        
        except urllib.error.HTTPError as e:
            code = e.code
            if code in (500, 502, 503, 504) and retries < TRANSPORT_RETRY_LIMIT:
                retries += 1
                time.sleep(2 ** retries)
                continue
            
            error_code = f"HTTP_{code}"
            if code == 401:
                error_code = "UNAUTHORIZED"
            elif code == 403:
                error_code = "FORBIDDEN_OR_RATE_LIMIT"
            elif code == 404:
                error_code = "NOT_FOUND"
                
            raise GitHubTransportError(error_code, "HTTP", code, False, f"HTTP Error {code}")
            
        except urllib.error.URLError as e:
            if "Redirect to unauthorized host blocked" in str(e.reason):
                raise GitHubTransportError("REDIRECT_TO_UNAUTHORIZED_HOST", "SECURITY", 0, False, "Redirected to unauthorized host")
            if retries < TRANSPORT_RETRY_LIMIT:
                retries += 1
                time.sleep(2 ** retries)
                continue
            raise GitHubTransportError("NETWORK_ERROR", "NETWORK", 0, False, "Network error")
            
        except (TimeoutError, socket.timeout):
            if retries < TRANSPORT_RETRY_LIMIT:
                retries += 1
                time.sleep(2 ** retries)
                continue
            raise GitHubTransportError("TIMEOUT", "NETWORK", 0, False, "Network timeout")
            
    raise GitHubTransportError("RETRY_EXHAUSTED", "NETWORK", 0, False, "Retries exhausted")

class GitHubReadOnlyTransport:
    def __init__(self, opener=None):
        self.opener = opener or urllib.request.build_opener(NoCrossHostRedirectHandler())

    def request_rest(self, path: str) -> Any:
        if not path.startswith("/"):
            path = "/" + path
        url = "https://api.github.com" + path
        token = _get_token()
        
        req = urllib.request.Request(url, method="GET")
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("X-GitHub-Api-Version", "2022-11-28")
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("User-Agent", "AOS-Merge-Authorization/1.0")
        
        return _execute_request(req, self.opener)

    def request_graphql(self, query_name: str, variables: Dict[str, Any]) -> Any:
        if query_name not in PREDEFINED_GRAPHQL_QUERIES:
            raise GitHubTransportError("UNKNOWN_GRAPHQL_QUERY", "VALIDATION", 0, False, "Query name not in predefined registry")
            
        query_text = PREDEFINED_GRAPHQL_QUERIES[query_name]
        if "mutation" in query_text.lower():
            raise GitHubTransportError("GITHUB_MUTATION_DOCUMENT_FORBIDDEN", "SECURITY", 0, False, "GraphQL mutation operation detected in predefined query")
            
        url = "https://api.github.com/graphql"
        token = _get_token()
        
        payload = json.dumps({"query": query_text, "variables": variables}).encode("utf-8")
        
        req = urllib.request.Request(url, data=payload, method="POST")
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("Content-Type", "application/json")
        req.add_header("User-Agent", "AOS-Merge-Authorization/1.0")
        
        return _execute_request(req, self.opener)
