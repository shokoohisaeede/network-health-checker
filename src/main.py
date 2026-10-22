import argparse
import csv
import json
import time
from datetime import datetime, timezone
from pathlib import Path

from connectivity import ping_device

PROJECT_DIR = Path(__file__).resolve().parent.parent
DEVICES_FILE = PROJECT_DIR / "devices.json"
REPORTS_DIR = PROJECT_DIR / "reports"
previous_states = {}

def load_devices():
    """Load the device inventory from JSON."""
    with DEVICES_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)["devices"]

def check_status_change(name, reachable):
    """Print an alert when a device changes its availability."""
    current_state = "UP" if reachable else "DOWN"
    previous_state = previous_states.get(name)

    if previous_state == "UP" and current_state == "DOWN":
        print(f"\nALERT: {name} is DOWN!")

    elif previous_state == "DOWN" and current_state == "UP":
        print(f"\nRECOVERY: {name} is UP again.")

    previous_states[name] = current_state

def save_reports(results):
    """Save the latest results and append them to history."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    json_file = REPORTS_DIR / "network_health.json"
    csv_file = REPORTS_DIR / "network_health.csv"
    history_file = REPORTS_DIR / "network_health_history.csv"

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

    with json_file.open("w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)

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

    print(f"Reports saved: {json_file}, {csv_file}")


def check_network(devices):
    """Check all configured devices and save one monitoring cycle."""
    results = []

    print(f"\nCheck time: {datetime.now(timezone.utc).isoformat()}")
    print("-" * 80)

    for device in devices:
        ping_result = ping_device(device["host"])
        ping_result = ping_device(device["host"])
        check_status_change(device["name"], ping_result["reachable"])

        
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

    total = len(results)
    up = sum(1 for device in results if device["reachable"])
    down = total - up
    overall = "HEALTHY" if down == 0 else "ISSUES DETECTED"

    print("-" * 40)
    print(f"Total devices: {total}")
    print(f"Devices UP: {up}")
    print(f"Devices DOWN: {down}")
    print(f"Overall status: {overall}")


def main():
    parser = argparse.ArgumentParser(description="Network Health Checker")
    parser.add_argument(
        "--interval",
        type=int,
        default=0,
        help="Seconds between checks; 0 runs once",
    )
    args = parser.parse_args()

    if args.interval < 0:
        parser.error("--interval must be 0 or a positive number")

    devices = load_devices()
    print(f"Devices configured: {len(devices)}")

    try:
        while True:
            check_network(devices)

            if args.interval == 0:
                break

            print(f"\nNext check in {args.interval} seconds. Press Ctrl+C to stop.")
            time.sleep(args.interval)

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")


if __name__ == "__main__":
    main()

