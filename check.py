import os
import sys
import subprocess
import re
import logging

# API Key: set the environment variable API_KEY to your secret key.
# Do not hardcode secrets in source code.
API_KEY = os.getenv("API_KEY", "")


def is_valid_host(host: str) -> bool:
    """
    Validate a hostname or IP address for ping.
    Only allow alphanumeric characters, dots, hyphens, and ensure
    length is between 1 and 253 characters. Reject any shell
    metacharacters.
    """
    if not host or len(host) > 253:
        return False
    # Allow only letters, digits, dots, hyphens
    pattern = r'^[a-zA-Z0-9.-]+$'
    return re.match(pattern, host) is not None


def ping_host(host: str) -> str:
    """
    Ping a single host. Returns 'up', 'down', or 'error'.
    Uses subprocess.run with a command list to prevent injection.
    """
    try:
        result = subprocess.run(
            ['ping', '-c', '1', host],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=10
        )
        if result.returncode == 0:
            return 'up'
        else:
            return 'down'
    except (subprocess.TimeoutExpired, OSError) as e:
        logging.warning("Ping failed for %s: %s", host, e)
        return 'error'


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(message)s',
        stream=sys.stdout
    )

    hosts = sys.argv[1:] if len(sys.argv) > 1 else ["localhost"]

    for host in hosts:
        if not is_valid_host(host):
            logging.warning("Skipping invalid host: %s", host)
            continue

        status = ping_host(host)
        if status == 'error':
            logging.error("Host %s: error (ping failed)", host)
        elif status == 'up':
            logging.info("Host %s: up", host)
        else:
            logging.info("Host %s: down", host)


if __name__ == "__main__":
    main()