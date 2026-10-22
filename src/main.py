
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

from connectivity import ping_device

PROJECT_DIR = Path(__file__).resolve().parent.parent
DEVICES_FILE = PROJECT_DIR / "devices.json"
REPORTS_DIR = PROJECT_DIR / "reports"


def load_devices():
    """Load the device inventory from JSON."""
    with DEVICES_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)["devices"]


def save_reports(results):
    """Save network health results as JSON and CSV."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    json_file = REPORTS_DIR / "network_health.json"
    csv_file = REPORTS_DIR / "network_health.csv"
    history_file = REPORTS_DIR / "network_health_history.csv"
    with json_file.open("w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)

    fieldnames = [
        "checked_at",
        "name",
        "host",
        "reachable",
        "status",
        "sent",
        "received",
        "packet_loss_percent",
        "min_rtt_ms",
        "avg_rtt_ms",
        "max_rtt_ms",
    ]

    with csv_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
        history_exists = history_file.exists()

    with history_file.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not history_exists:
            writer.writeheader()

        writer.writerows(results)
    print("\nReports saved:")
    print(f"JSON: {json_file}")
    print(f"CSV:  {csv_file}")


def main():
    devices = load_devices()
    results = []

    print(f"Devices configured: {len(devices)}")
    print("=" * 100)

    for device in devices:
        ping_result = ping_device(device["host"])

        record = {
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "name": device["name"],
            **ping_result,
        }

        results.append(record)

        print(
            f"{record['name']:<8} | "
            f"{record['host']:<15} | "
            f"Status: {record['status']:<18} | "
            f"Loss: {record['packet_loss_percent']:>5.1f}% | "
            f"Avg RTT: {record['avg_rtt_ms']} ms"
        )

    save_reports(results)
    total_devices = len(results)
    devices_up = sum(1 for device in results if device["reachable"])
    devices_down = total_devices - devices_up

    overall_status = "HEALTHY" if devices_down == 0 else "ISSUES DETECTED"

    print("\n" + "=" * 40)
    print("NETWORK HEALTH SUMMARY")
    print("=" * 40)
    print(f"Total devices: {total_devices}")
    print(f"Devices UP: {devices_up}")
    print(f"Devices DOWN: {devices_down}")
    print(f"Overall status: {overall_status}")

if __name__ == "__main__":
    main()
