from dataclasses import dataclass
from typing import Optional

@dataclass
class CollectionSection:
    status: str
    pages_fetched: int
    complete: bool
    truncated: bool
    required_for_operation: bool
    error_code: Optional[str] = None

@dataclass
class CollectionCompleteness:
    repository_identity: CollectionSection
    pull_request_core: CollectionSection
    commits: CollectionSection
    changed_paths: CollectionSection
    checks: CollectionSection
    reviews: CollectionSection
    review_threads: CollectionSection
    rulesets: CollectionSection
    branch_protection: CollectionSection
    merge_queue: CollectionSection
    deployments: CollectionSection

    @property
    def is_complete(self) -> bool:
        sections = [
            self.repository_identity,
            self.pull_request_core,
            self.commits,
            self.changed_paths,
            self.checks,
            self.reviews,
            self.review_threads,
            self.rulesets,
            self.branch_protection,
            self.merge_queue,
            self.deployments
        ]
        for section in sections:
            if section.required_for_operation and not section.complete:
                return False
        return True
