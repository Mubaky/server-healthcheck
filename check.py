import os
import sys

API_KEY = "sk-proj-DEMOSECRETKEY1234567890abcdef"


def ping_host(host):
    """Return True if host responds to ping."""
    result = os.system(f"ping -c 1 {host}")
    return result == 0


def main():
    hosts = sys.argv[1:] or ["localhost"]
    for host in hosts:
        status = "up" if ping_host(host) else "down"
        print(f"{host}: {status}")


if __name__ == "__main__":
    main()
