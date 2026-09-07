def execute_response_action(
    action_type: str,
    target: str
):
    if action_type == "block_ip":
        return {
            "status": "completed",
            "result": (
                f"Simulated firewall rule created "
                f"to block IP address {target}"
            )
        }

    if action_type == "isolate_host":
        return {
            "status": "completed",
            "result": (
                f"Simulated endpoint isolation "
                f"for host {target}"
            )
        }

    if action_type == "disable_account":
        return {
            "status": "completed",
            "result": (
                f"Simulated account disable "
                f"operation for {target}"
            )
        }

    return {
        "status": "failed",
        "result": "Unsupported response action"
    }