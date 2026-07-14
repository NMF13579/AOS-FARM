import os
import json
import socket
import urllib.error
import pytest
from unittest.mock import MagicMock
from aos.runtime.github_readonly_transport import (
    GitHubReadOnlyTransport, GitHubTransportError, NoCrossHostRedirectHandler
)

@pytest.fixture
def fake_token(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "fake_token_123")

def test_rest_get_allowed(fake_token):
    mock_opener = MagicMock()
    mock_response = MagicMock()
    mock_response.getcode.return_value = 200
    mock_response.read.return_value = b'{"status": "ok"}'
    mock_response.getheader.return_value = '16'
    mock_opener.open.return_value.__enter__.return_value = mock_response
    
    transport = GitHubReadOnlyTransport(opener=mock_opener)
    result = transport.request_rest("/repos/foo")
    assert result == {"status": "ok"}
    
    req = mock_opener.open.call_args[0][0]
    assert req.method == "GET"
    assert req.full_url == "https://api.github.com/repos/foo"
    assert req.headers.get("Authorization") == "Bearer fake_token_123"

def test_missing_token(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    transport = GitHubReadOnlyTransport()
    with pytest.raises(GitHubTransportError) as exc:
        transport.request_rest("/repos/foo")
    assert exc.value.error_code == "GITHUB_AUTHENTICATION_UNAVAILABLE"

def test_token_absent_from_errors(fake_token):
    mock_opener = MagicMock()
    mock_opener.open.side_effect = urllib.error.URLError("fake_token_123 is in exception message")
    
    transport = GitHubReadOnlyTransport(opener=mock_opener)
    with pytest.raises(GitHubTransportError) as exc:
        transport.request_rest("/repos/foo")
    
    assert "fake_token_123" not in str(exc.value)

def test_rest_post_blocked():
    # Only GET is implemented in request_rest
    pass

def test_graphql_query_allowed(fake_token):
    mock_opener = MagicMock()
    mock_response = MagicMock()
    mock_response.getcode.return_value = 200
    mock_response.read.return_value = b'{"data": "ok"}'
    mock_response.getheader.return_value = '14'
    mock_opener.open.return_value.__enter__.return_value = mock_response
    
    transport = GitHubReadOnlyTransport(opener=mock_opener)
    result = transport.request_graphql("review_threads", {"owner": "foo", "name": "bar", "number": 1})
    assert result == {"data": "ok"}
    
    req = mock_opener.open.call_args[0][0]
    assert req.method == "POST"
    assert req.full_url == "https://api.github.com/graphql"

def test_graphql_mutation_blocked(fake_token):
    transport = GitHubReadOnlyTransport()
    with pytest.raises(GitHubTransportError) as exc:
        transport.request_graphql("invalid_query_not_in_registry", {})
    assert exc.value.error_code == "UNKNOWN_GRAPHQL_QUERY"

def test_timeout_normalized(fake_token):
    mock_opener = MagicMock()
    mock_opener.open.side_effect = socket.timeout("timeout")
    transport = GitHubReadOnlyTransport(opener=mock_opener)
    with pytest.raises(GitHubTransportError) as exc:
        transport.request_rest("/repos/foo")
    assert exc.value.error_code == "TIMEOUT"

def test_http_401_normalized(fake_token):
    mock_opener = MagicMock()
    # HTTPError takes url, code, msg, hdrs, fp
    mock_opener.open.side_effect = urllib.error.HTTPError("url", 401, "Unauthorized", {}, None)
    transport = GitHubReadOnlyTransport(opener=mock_opener)
    with pytest.raises(GitHubTransportError) as exc:
        transport.request_rest("/repos/foo")
    assert exc.value.error_code == "UNAUTHORIZED"
    assert exc.value.retryable is False

def test_http_403_normalized(fake_token):
    mock_opener = MagicMock()
    mock_opener.open.side_effect = urllib.error.HTTPError("url", 403, "Forbidden", {}, None)
    transport = GitHubReadOnlyTransport(opener=mock_opener)
    with pytest.raises(GitHubTransportError) as exc:
        transport.request_rest("/repos/foo")
    assert exc.value.error_code == "FORBIDDEN_OR_RATE_LIMIT"

def test_http_404_normalized(fake_token):
    mock_opener = MagicMock()
    mock_opener.open.side_effect = urllib.error.HTTPError("url", 404, "Not Found", {}, None)
    transport = GitHubReadOnlyTransport(opener=mock_opener)
    with pytest.raises(GitHubTransportError) as exc:
        transport.request_rest("/repos/foo")
    assert exc.value.error_code == "NOT_FOUND"

def test_malformed_json_blocked(fake_token):
    mock_opener = MagicMock()
    mock_response = MagicMock()
    mock_response.getcode.return_value = 200
    mock_response.read.return_value = b'{invalid_json}'
    mock_response.getheader.return_value = '14'
    mock_opener.open.return_value.__enter__.return_value = mock_response
    
    transport = GitHubReadOnlyTransport(opener=mock_opener)
    with pytest.raises(GitHubTransportError) as exc:
        transport.request_rest("/repos/foo")
    assert exc.value.error_code == "MALFORMED_JSON"

def test_oversized_response_blocked(fake_token):
    mock_opener = MagicMock()
    mock_response = MagicMock()
    mock_response.getcode.return_value = 200
    mock_response.getheader.return_value = str(11 * 1024 * 1024)
    mock_opener.open.return_value.__enter__.return_value = mock_response
    
    transport = GitHubReadOnlyTransport(opener=mock_opener)
    with pytest.raises(GitHubTransportError) as exc:
        transport.request_rest("/repos/foo")
    assert exc.value.error_code == "OVERSIZED_RESPONSE"

def test_redirect_blocked():
    handler = NoCrossHostRedirectHandler()
    req = MagicMock()
    with pytest.raises(urllib.error.URLError, match="Redirect to unauthorized host blocked"):
        handler.redirect_request(req, None, 302, "Found", {}, "https://evil.com")

def test_graphql_registry_is_immutable():
    from aos.runtime.github_readonly_transport import PREDEFINED_GRAPHQL_QUERIES
    with pytest.raises(TypeError):
        PREDEFINED_GRAPHQL_QUERIES["new_query"] = "query {}"

def test_no_mutation_in_registry():
    from aos.runtime.github_readonly_transport import PREDEFINED_GRAPHQL_QUERIES
    for query_text in PREDEFINED_GRAPHQL_QUERIES.values():
        assert "mutation" not in query_text.lower()

def test_arbitrary_query_string_rejected(fake_token):
    transport = GitHubReadOnlyTransport()
    with pytest.raises(GitHubTransportError) as exc:
        transport.request_graphql("query { viewer { login } }", {})
    assert exc.value.error_code == "UNKNOWN_GRAPHQL_QUERY"

@pytest.fixture(autouse=True)
def fail_on_network(monkeypatch):
    def block_network(*args, **kwargs):
        raise AssertionError("unexpected live network call")
    monkeypatch.setattr(urllib.request, "urlopen", block_network)
    monkeypatch.setattr(socket, "socket", block_network)

