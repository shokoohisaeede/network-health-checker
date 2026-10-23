from performance import check_latency


def test_latency_above_threshold_triggers_alert(capsys):
    """Latency above the threshold should trigger an alert."""
    result = check_latency("PC1", 75.0, threshold=50.0)

    captured = capsys.readouterr()

    assert result is True
    assert "PERFORMANCE ALERT: PC1" in captured.out
    assert "75.00 ms" in captured.out


def test_latency_below_threshold_no_alert(capsys):
    """Latency below the threshold should not trigger an alert."""
    result = check_latency("PC1", 20.0, threshold=50.0)

    captured = capsys.readouterr()

    assert result is False
    assert "PERFORMANCE ALERT" not in captured.out


def test_missing_latency_no_alert(capsys):
    """Missing latency data should not trigger an alert."""
    result = check_latency("PC1", None, threshold=50.0)

    captured = capsys.readouterr()

    assert result is False
    assert captured.out == ""
