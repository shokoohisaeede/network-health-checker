from prometheus_client import Gauge, start_http_server

# Device availability: 1 = UP, 0 = DOWN
DEVICE_UP = Gauge(
    "network_device_up",
    "Whether a network device is reachable (1=UP, 0=DOWN)",
    ["device", "host"],
)

# Ping round-trip time in milliseconds
DEVICE_LATENCY = Gauge(
    "network_device_latency_ms",
    "Latest average ping round-trip time in milliseconds",
    ["device", "host"],
)

# Packet loss percentage from the latest check
DEVICE_PACKET_LOSS = Gauge(
    "network_device_packet_loss_percent",
    "Packet loss percentage from the latest ping check",
    ["device", "host"],
)

def update_metrics(device_name, result):
    """Update Prometheus metrics from one ping result."""
    labels = {
        "device": device_name,
        "host": result["host"],
    }

    DEVICE_UP.labels(**labels).set(1 if result["reachable"] else 0)
    DEVICE_PACKET_LOSS.labels(**labels).set(result["packet_loss_percent"])

    latency = result["avg_rtt_ms"]
    if latency is not None:
        DEVICE_LATENCY.labels(**labels).set(latency)


def start_metrics_server(port=8000):
    """Expose metrics for Prometheus to scrape."""
    start_http_server(port)
    print(f"Prometheus metrics available on port {port}")
