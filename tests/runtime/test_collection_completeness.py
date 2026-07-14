from aos.runtime.collection_completeness import CollectionCompleteness, CollectionSection

def test_all_required_complete():
    comp = CollectionCompleteness(
        repository_identity=CollectionSection("PASS", 1, True, False, True),
        pull_request_core=CollectionSection("PASS", 1, True, False, True),
        commits=CollectionSection("PASS", 1, True, False, True),
        changed_paths=CollectionSection("PASS", 1, True, False, True),
        checks=CollectionSection("PASS", 1, True, False, True),
        reviews=CollectionSection("PASS", 1, True, False, True),
        review_threads=CollectionSection("PASS", 1, True, False, True),
        rulesets=CollectionSection("PASS", 1, True, False, True),
        branch_protection=CollectionSection("PASS", 1, True, False, True),
        merge_queue=CollectionSection("PASS", 1, True, False, True),
        deployments=CollectionSection("PASS", 1, True, False, True),
    )
    assert comp.is_complete is True

def test_optional_section_unavailable():
    comp = CollectionCompleteness(
        repository_identity=CollectionSection("PASS", 1, True, False, True),
        pull_request_core=CollectionSection("PASS", 1, True, False, True),
        commits=CollectionSection("PASS", 1, True, False, True),
        changed_paths=CollectionSection("PASS", 1, True, False, True),
        checks=CollectionSection("PASS", 1, True, False, True),
        reviews=CollectionSection("PASS", 1, True, False, True),
        review_threads=CollectionSection("PASS", 1, True, False, True),
        rulesets=CollectionSection("PASS", 1, True, False, True),
        branch_protection=CollectionSection("PASS", 1, True, False, True),
        merge_queue=CollectionSection("UNKNOWN", 1, False, False, False, "UNAVAILABLE"),
        deployments=CollectionSection("PASS", 1, True, False, True),
    )
    assert comp.is_complete is True

def test_required_section_unavailable():
    comp = CollectionCompleteness(
        repository_identity=CollectionSection("PASS", 1, True, False, True),
        pull_request_core=CollectionSection("PASS", 1, True, False, True),
        commits=CollectionSection("PASS", 1, True, False, True),
        changed_paths=CollectionSection("PASS", 1, True, False, True),
        checks=CollectionSection("PASS", 1, True, False, True),
        reviews=CollectionSection("UNKNOWN", 1, False, False, True, "UNAVAILABLE"),
        review_threads=CollectionSection("PASS", 1, True, False, True),
        rulesets=CollectionSection("PASS", 1, True, False, True),
        branch_protection=CollectionSection("PASS", 1, True, False, True),
        merge_queue=CollectionSection("PASS", 1, True, False, True),
        deployments=CollectionSection("PASS", 1, True, False, True),
    )
    assert comp.is_complete is False
