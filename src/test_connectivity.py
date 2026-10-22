import main
import subprocess
from unittest.mock import patch, Mock

from connectivity import ping_device


def test_ping_device_success():
    """A reachable device should be reported as UP."""
    fake_result = Mock()
    fake_result.stdout = (
        "4 packets transmitted, 4 received, 0% packet loss\n"
        "rtt min/avg/max/mdev = 1.0/2.0/3.0/0.5 ms"
    )
    fake_result.stderr = ""
    fake_result.returncode = 0

    with patch("connectivity.subprocess.run", return_value=fake_result):
        result = ping_device("192.0.2.1")

    assert result["host"] == "192.0.2.1"
    assert result["reachable"] is True
    assert result["status"] == "UP"
    assert result["sent"] == 4
    assert result["received"] == 4
    assert result["packet_loss_percent"] == 0
    assert result["min_rtt_ms"] == 1.0
    assert result["avg_rtt_ms"] == 2.0
    assert result["max_rtt_ms"] == 3.0


def test_ping_device_no_response():
    """A device with no replies should be reported as unreachable."""
    fake_result = Mock()
    fake_result.stdout = (
        "4 packets transmitted, 0 received, 100% packet loss"
    )
    fake_result.stderr = ""
    fake_result.returncode = 1

    with patch("connectivity.subprocess.run", return_value=fake_result):
        result = ping_device("192.0.2.2")

    assert result["reachable"] is False
    assert result["status"] == "NO PING RESPONSE"
    assert result["received"] == 0
    assert result["packet_loss_percent"] == 100.0


def test_ping_device_timeout():
    """A ping command timeout should return TIMEOUT status."""
    with patch(
        "connectivity.subprocess.run",
        side_effect=subprocess.TimeoutExpired("ping", 10),
    ):
        result = ping_device("192.0.2.3")

    assert result["reachable"] is False
    assert result["status"] == "TIMEOUT"
    assert result["packet_loss_percent"] == 100.0
def test_ping_device_os_error():
    """An OS error should be returned without crashing the program."""
    with patch(
        "connectivity.subprocess.run",
        side_effect=OSError("ping command not found"),
    ):
        result = ping_device("192.0.2.4")

    assert result["reachable"] is False
    assert result["status"] == "ERROR: ping command not found"
    assert result["received"] == 0
    assert result["packet_loss_percent"] == 100.0
def test_status_change_alert(capsys):
    """A transition from UP to DOWN should print an alert."""
    main.previous_states.clear()

    main.check_status_change("PC1", True)
    main.check_status_change("PC1", False)

    captured = capsys.readouterr()
    assert "ALERT: PC1 is DOWN!" in captured.out
def test_status_change_recovery(capsys):
    """A transition from DOWN to UP should print a recovery message."""
    main.previous_states.clear()

    main.check_status_change("PC1", False)
    main.check_status_change("PC1", True)

    captured = capsys.readouterr()
    assert "RECOVERY: PC1 is UP again." in captured.out
