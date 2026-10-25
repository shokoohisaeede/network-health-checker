import csv

from availability import calculate_availability


def test_availability_with_up_and_down_checks(tmp_path):
    """Availability should reflect successful and failed checks."""
    history_file = tmp_path / "history.csv"

    rows = [
        {
            "name": "PC1",
            "reachable": "True",
        },
        {
            "name": "PC1",
            "reachable": "True",
        },
        {
            "name": "PC1",
            "reachable": "False",
        },
        {
            "name": "PC1",
            "reachable": "True",
        },
    ]

    with history_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["name", "reachable"],
        )
        writer.writeheader()
        writer.writerows(rows)

    result = calculate_availability(history_file)

    assert result["PC1"]["total_checks"] == 4
    assert result["PC1"]["successful_checks"] == 3
    assert result["PC1"]["availability_percent"] == 75.0


def test_empty_history(tmp_path):
    """An empty history should return no device results."""
    history_file = tmp_path / "history.csv"
    history_file.write_text("name,reachable\n", encoding="utf-8")

    result = calculate_availability(history_file)

    assert result == {}
def test_missing_history_file(tmp_path):
    """A missing history file should return no device results."""
    history_file = tmp_path / "missing_history.csv"

    result = calculate_availability(history_file)

    assert result == {}
