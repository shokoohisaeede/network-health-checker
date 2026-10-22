
import platform
import re
import subprocess
from typing import Any


def ping_device(host: str, count: int = 4, timeout: int = 2) -> dict[str, Any]:
    """Check reachability and collect packet-loss and latency metrics."""

    system = platform.system().lower()

    if system == "windows":
        command = [
            "ping", "-n", str(count),
            "-w", str(timeout * 1000), host
        ]
    else:
        command = [
            "ping", "-c", str(count),
            "-W", str(timeout), host
        ]

    result_data: dict[str, Any] = {
        "host": host,
        "reachable": False,
        "status": "NO PING RESPONSE",
        "sent": count,
        "received": 0,
        "packet_loss_percent": 100.0,
        "min_rtt_ms": None,
        "avg_rtt_ms": None,
        "max_rtt_ms": None,
    }

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=(count * (timeout + 1)) + 2,
            check=False,
        )

        output = result.stdout + "\n" + result.stderr

        # Extract transmitted and received packet counts.
        if system == "windows":
            sent_match = re.search(r"Sent\s*=\s*(\d+)", output, re.I)
            received_match = re.search(r"Received\s*=\s*(\d+)", output, re.I)
            if sent_match:
                result_data["sent"] = int(sent_match.group(1))
            if received_match:
                result_data["received"] = int(received_match.group(1))
        else:
            packet_match = re.search(
                r"(\d+)\s+packets transmitted,\s+(\d+)\s+"
                r"(?:packets )?received",
                output,
                re.I,
            )
            if packet_match:
                result_data["sent"] = int(packet_match.group(1))
                result_data["received"] = int(packet_match.group(2))

        sent = result_data["sent"]
        received = result_data["received"]

        if sent > 0:
            result_data["packet_loss_percent"] = round(
                ((sent - received) / sent) * 100, 2
            )

        result_data["reachable"] = received > 0
        result_data["status"] = "UP" if received > 0 else "NO PING RESPONSE"

        # Extract latency statistics from ping output.
        if system == "windows":
            rtt_match = re.search(
                r"Minimum\s*=\s*(\d+)\s*ms.*?"
                r"Maximum\s*=\s*(\d+)\s*ms.*?"
                r"Average\s*=\s*(\d+)\s*ms",
                output,
                re.I | re.S,
            )
            if rtt_match:
                result_data["min_rtt_ms"] = float(rtt_match.group(1))
                result_data["max_rtt_ms"] = float(rtt_match.group(2))
                result_data["avg_rtt_ms"] = float(rtt_match.group(3))
        else:
            rtt_match = re.search(
                r"rtt min/avg/max/(?:mdev|stddev)\s*=\s*"
                r"([\d.]+)/([\d.]+)/([\d.]+)",
                output,
            )
            if rtt_match:
                result_data["min_rtt_ms"] = float(rtt_match.group(1))
                result_data["avg_rtt_ms"] = float(rtt_match.group(2))
                result_data["max_rtt_ms"] = float(rtt_match.group(3))

        return result_data

    except subprocess.TimeoutExpired:
        result_data["status"] = "TIMEOUT"
        return result_data

    except OSError as exc:
        result_data["status"] = f"ERROR: {exc}"
        return result_data

