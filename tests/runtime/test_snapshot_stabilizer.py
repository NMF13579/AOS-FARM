import pytest
from aos.runtime.snapshot_stabilizer import SnapshotStabilizer

class MockCollector:
    def __init__(self, scenario):
        self.scenario = scenario
        self.call_log = []
        self.anchor_index = 0
        self.snapshot_index = 0

    def collect_anchor(self):
        self.call_log.append("collect_anchor")
        if self.scenario == "collector_error":
            raise ValueError("Some API error with token secret_xyz_123")
        elif self.scenario == "error_on_second":
            if self.anchor_index >= 2:
                raise RuntimeError("API error 2")
                
        anchor = {"data": 1}
        if self.scenario == "stable":
            pass
        elif self.scenario == "unstable_twice":
            anchor = {"data": self.anchor_index}
        elif self.scenario == "unstable_then_stable":
            if self.anchor_index < 2:
                anchor = {"data": self.anchor_index}
            else:
                anchor = {"data": 99}
        elif self.scenario == "incomplete_anchor":
            anchor = {}
        
        self.anchor_index += 1
        return anchor

    def collect_full_snapshot(self):
        self.call_log.append("collect_full_snapshot")
        if self.scenario == "collector_error":
            raise ValueError("Error")
        self.snapshot_index += 1
        return {"snapshot_data": f"snap_{self.snapshot_index}"}

def mock_compare(a1, a2):
    if not a1 or not a2:
        return {"stable": False, "technical_status": "UNKNOWN", "reason_code": "SNAPSHOT_ANCHOR_INCOMPLETE"}
    if a1 != a2:
        return {"stable": False, "technical_status": "FAIL", "reason_code": "SNAPSHOT_ANCHOR_CHANGED", "changed_fields": ["data"]}
    return {"stable": True, "technical_status": "PASS", "reason_code": None}

def test_stable_first_attempt():
    col = MockCollector("stable")
    stab = SnapshotStabilizer(col, mock_compare)
    res = stab.stabilize()
    assert res["snapshot_status"] == "STABLE"
    assert res["technical_status"] == "PASS"
    assert res["attempts_used"] == 1
    assert "stable_snapshot" in res
    assert col.call_log == ["collect_anchor", "collect_full_snapshot", "collect_anchor"]

def test_unstable_then_stable():
    col = MockCollector("unstable_then_stable")
    stab = SnapshotStabilizer(col, mock_compare)
    res = stab.stabilize()
    assert res["snapshot_status"] == "STABLE_AFTER_RETRY"
    assert res["technical_status"] == "PASS"
    assert res["attempts_used"] == 2
    assert "stable_snapshot" in res
    assert res["stable_snapshot"] == {"snapshot_data": "snap_2"}
    assert col.call_log == ["collect_anchor", "collect_full_snapshot", "collect_anchor", "collect_anchor", "collect_full_snapshot", "collect_anchor"]

def test_unstable_both_attempts():
    col = MockCollector("unstable_twice")
    stab = SnapshotStabilizer(col, mock_compare)
    res = stab.stabilize()
    assert res["snapshot_status"] == "UNSTABLE"
    assert res["technical_status"] == "FAIL"
    assert res["control_status"] == "BLOCKED"
    assert res["reason_code"] == "LIVE_STATE_UNSTABLE"
    assert "stable_snapshot" not in res
    assert res["attempts_used"] == 2

def test_collector_error():
    col = MockCollector("collector_error")
    stab = SnapshotStabilizer(col, mock_compare)
    res = stab.stabilize()
    assert res["technical_status"] == "UNKNOWN"
    assert res["control_status"] == "UNKNOWN_BLOCKED"
    assert res["reason_code"] == "SNAPSHOT_COLLECTION_UNAVAILABLE"
    assert "secret_xyz" not in str(res)
    assert "ValueError" not in str(res)

def test_collector_error_on_second():
    class MixedCollector(MockCollector):
        def collect_anchor(self):
            if self.anchor_index == 2:
                raise ValueError("secret")
            return super().collect_anchor()
    col = MixedCollector("unstable_then_stable")
    stab = SnapshotStabilizer(col, mock_compare)
    res = stab.stabilize()
    assert res["attempts_used"] == 2
    assert res["technical_status"] == "UNKNOWN"
    assert res["control_status"] == "UNKNOWN_BLOCKED"

def test_incomplete_anchor():
    col = MockCollector("incomplete_anchor")
    stab = SnapshotStabilizer(col, mock_compare)
    res = stab.stabilize()
    assert res["technical_status"] == "UNKNOWN"
    assert res["control_status"] == "UNKNOWN_BLOCKED"
    assert res["reason_code"] == "SNAPSHOT_ANCHOR_INCOMPLETE"
    assert res["attempts_used"] == 1

def test_input_snapshots_not_mutated():
    col = MockCollector("stable")
    stab = SnapshotStabilizer(col, mock_compare)
    res = stab.stabilize()
    assert res["stable_snapshot"] == {"snapshot_data": "snap_1"}

def test_max_attempts_fixed_at_2():
    col = MockCollector("unstable_twice")
    stab = SnapshotStabilizer(col, mock_compare)
    assert stab.maximum_attempts == 2

def test_third_attempt_never_executed():
    col = MockCollector("unstable_twice")
    stab = SnapshotStabilizer(col, mock_compare)
    stab.stabilize()
    assert col.call_log.count("collect_full_snapshot") == 2

def test_first_unstable_snapshot_discarded():
    col = MockCollector("unstable_then_stable")
    stab = SnapshotStabilizer(col, mock_compare)
    res = stab.stabilize()
    assert res["stable_snapshot"] == {"snapshot_data": "snap_2"}

def test_unknown_does_not_become_pass():
    col = MockCollector("incomplete_anchor")
    stab = SnapshotStabilizer(col, mock_compare)
    res = stab.stabilize()
    assert res["technical_status"] == "UNKNOWN"

def test_stable_snapshot_returned_only_on_success():
    col = MockCollector("unstable_twice")
    stab = SnapshotStabilizer(col, mock_compare)
    res = stab.stabilize()
    assert "stable_snapshot" not in res
