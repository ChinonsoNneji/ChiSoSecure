from types import SimpleNamespace

from backend.app.detection import analyze_event


class FakeQuery:
    def filter(self, *args, **kwargs):
        return self

    def count(self):
        return 0


class FakeDatabase:
    def query(self, *args, **kwargs):
        return FakeQuery()


def test_high_severity_detection():
    event = SimpleNamespace(
        source_ip="10.0.0.10",
        event_type="network_activity",
        severity="high"
    )

    alerts = analyze_event(
        event,
        FakeDatabase()
    )

    rule_names = [
        alert["rule_name"]
        for alert in alerts
    ]

    assert "High Severity Event" in rule_names


def test_malware_detection():
    event = SimpleNamespace(
        source_ip="10.0.0.20",
        event_type="malware",
        severity="medium"
    )

    alerts = analyze_event(
        event,
        FakeDatabase()
    )

    rule_names = [
        alert["rule_name"]
        for alert in alerts
    ]

    assert "Malware Detection" in rule_names


def test_privilege_escalation_detection():
    event = SimpleNamespace(
        source_ip="10.0.0.30",
        event_type="privilege_escalation",
        severity="medium"
    )

    alerts = analyze_event(
        event,
        FakeDatabase()
    )

    rule_names = [
        alert["rule_name"]
        for alert in alerts
    ]

    assert (
        "Privilege Escalation Detection"
        in rule_names
    )