import csv
from collections import defaultdict
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
HISTORY_FILE = PROJECT_DIR / "reports" / "network_health_history.csv"


def calculate_availability(history_file=HISTORY_FILE):
    """Calculate availability percentage for each device."""
    checks = defaultdict(lambda: {"total": 0, "up": 0})

    with Path(history_file).open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = row["name"]
            checks[name]["total"] += 1

            if row["reachable"].strip().lower() == "true":
                checks[name]["up"] += 1

    availability = {}

    for name, counts in checks.items():
        total = counts["total"]
        up = counts["up"]

        availability[name] = {
            "total_checks": total,
            "successful_checks": up,
            "availability_percent": round((up / total) * 100, 2),
        }

    return availability


if __name__ == "__main__":
    results = calculate_availability()

    print("\nNetwork Availability Report")
    print("-" * 55)

    for name, stats in results.items():
        print(
            f"{name:<10} | "
            f"Availability: {stats['availability_percent']:>6.2f}% | "
            f"Successful checks: {stats['successful_checks']}/"
            f"{stats['total_checks']}"
        )
