from backend.app.response import (
    execute_response_action,
)


def test_block_ip_response():
    result = execute_response_action(
        "block_ip",
        "192.168.1.50"
    )

    assert result["status"] == "completed"

    assert "192.168.1.50" in result["result"]


def test_isolate_host_response():
    result = execute_response_action(
        "isolate_host",
        "workstation-01"
    )

    assert result["status"] == "completed"

    assert "workstation-01" in result["result"]


def test_disable_account_response():
    result = execute_response_action(
        "disable_account",
        "testuser"
    )

    assert result["status"] == "completed"

    assert "testuser" in result["result"]


def test_unsupported_response():
    result = execute_response_action(
        "something_invalid",
        "target"
    )

    assert result["status"] == "failed"