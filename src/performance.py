DEFAULT_LATENCY_THRESHOLD_MS = 50.0


def check_latency(name, avg_rtt_ms, threshold=DEFAULT_LATENCY_THRESHOLD_MS):
    """Warn when a device's average latency exceeds the threshold."""
    if avg_rtt_ms is None:
        return False

    if avg_rtt_ms > threshold:
        print(
            f"PERFORMANCE ALERT: {name} average latency is "
            f"{avg_rtt_ms:.2f} ms "
            f"(threshold: {threshold:.2f} ms)."
        )
        return True

    return False
