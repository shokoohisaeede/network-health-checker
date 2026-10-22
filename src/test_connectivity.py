from connectivity import ping_device


def main():
    result = ping_device("127.0.0.1")

    print("Connectivity test")
    print("-" * 30)
    print(f"Host: {result['host']}")
    print(f"Status: {result['status']}")


if __name__ == "__main__":
    main()
