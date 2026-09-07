def analyze_event(event):
    alerts = []

    # Rule 1: Failed login activity
    if event.event_type == "failed_login":
        alerts.append({
            "rule_name": "Failed Login Detection",
            "severity": "medium",
            "message": f"Failed login activity detected from {event.source_ip}"
        })

    # Rule 2: High severity event
    if event.severity == "high":
        alerts.append({
            "rule_name": "High Severity Event",
            "severity": "high",
            "message": f"High severity security event detected from {event.source_ip}"
        })

    # Rule 3: Malware activity
    if event.event_type == "malware":
        alerts.append({
            "rule_name": "Malware Detection",
            "severity": "critical",
            "message": f"Potential malware activity detected from {event.source_ip}"
        })

    # Rule 4: Privilege escalation
    if event.event_type == "privilege_escalation":
        alerts.append({
            "rule_name": "Privilege Escalation Detection",
            "severity": "critical",
            "message": f"Privilege escalation activity detected from {event.source_ip}"
        })

    return alerts