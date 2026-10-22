# Network Health Checker

A Python-based network monitoring tool designed to check device connectivity, measure network performance, and generate health reports.

This project was developed as a practical networking project using Python and a GNS3 lab environment.

## Features

- **Device Connectivity Monitoring:** Checks whether configured network devices are reachable.
- **Packet Loss Measurement:** Reports packet loss for each device.
- **Response Time Analysis:** Collects minimum, average, and maximum round-trip times (RTT).
- **Automated Health Reports:** Generates JSON and CSV reports.
- **Historical Monitoring:** Records results over multiple monitoring runs.
- **Network Health Summary:** Displays the number of reachable and unreachable devices and an overall health status.
- **Configurable Devices:** Uses a JSON configuration file to define devices and IP addresses.

## Technologies Used

- Python 3
- Linux (Ubuntu)
- Git and GitHub
- GNS3
- JSON and CSV
- Linux `ping` utility

## Project Structure

```text
network-health-checker/
├── devices.json
├── src/
│   ├── connectivity.py
│   ├── main.py
│   └── test_connectivity.py
├── reports/
└── .gitignore
```

## Configuration

Configure the devices to monitor in `devices.json`:

```json
{
  "devices": [
    {
      "name": "PC1",
      "host": "10.10.10.2",
      "device_type": "vpcs"
    },
    {
      "name": "PC2",
      "host": "10.10.10.3",
      "device_type": "vpcs"
    }
  ]
}
```

Replace the example IP addresses with the addresses used in your own lab or network.

## Installation

Clone the repository:

```bash
git clone https://github.com/shokoohisaeede/network-health-checker.git
cd network-health-checker
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Usage

Run the monitoring script from the project root:

```bash
python src/main.py
```

The script checks the configured devices and generates health reports in the `reports/` directory.

## Lab Environment

The project is tested in a GNS3 lab with virtual PCs connected through a virtual switch. This environment provides a controlled way to test connectivity and monitor network health.

## Future Improvements

- Support for additional network devices and monitoring methods.
- Graphical dashboard for network health and performance.
- Configurable monitoring intervals.
- Historical performance visualisation.
- Automated testing and continuous integration.

## Author

**Network Engineering and Python Networking Project**

GitHub: [shokoohisaeede](https://github.com/shokoohisaeede)
