import subprocess
import signal
import sys
import os

VALID_SERVICE_TYPES = {"http", "tcp", "ssh"}

BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def start_honeypot_process(honeypot_id: str, service_type: str, port: int) -> int:
    if service_type not in VALID_SERVICE_TYPES:
        raise ValueError(f"Unknown service_type: {service_type}")
    if not (1 <= port <= 65535):
        raise ValueError(f"Invalid port: {port}")

    process = subprocess.Popen(
        [sys.executable, "-m", "app.services.honeypot_runner", service_type, str(port), honeypot_id],
        cwd=BACKEND_ROOT,
    )
    return process.pid


def stop_honeypot_process(pid: int):
    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
