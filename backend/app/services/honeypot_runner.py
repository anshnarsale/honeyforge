import asyncio
import sys

from app.core.database import SessionLocal
from app.models.honeypot import Honeypot
from app.honeypots.http import run_http_honeypot
from app.honeypots.tcp import run_tcp_honeypot
from app.honeypots.ssh import run_ssh_honeypot


def get_honeypot_config(honeypot_id: str):
    db = SessionLocal()
    try:
        return db.query(Honeypot).filter(Honeypot.id == honeypot_id).first()
    finally:
        db.close()


async def main():
    service_type = sys.argv[1]
    port = int(sys.argv[2])
    honeypot_id = sys.argv[3]

    config = get_honeypot_config(honeypot_id)
    banner = config.banner if config and config.banner else None
    hostname = config.hostname if config and config.hostname else None
    fake_username = config.fake_username if config and config.fake_username else "admin"
    fake_password = config.fake_password if config and config.fake_password else "admin123"

    if service_type == "http":
        await run_http_honeypot(
            port,
            banner=banner or "nginx",
            hostname=hostname or "server",
            honeypot_id=honeypot_id,
        )
    elif service_type == "tcp":
        await run_tcp_honeypot(
            port,
            banner=banner or "Welcome to legacy management service.",
            honeypot_id=honeypot_id,
        )
    elif service_type == "ssh":
        await run_ssh_honeypot(
            port,
            "app/honeypots/keys/ssh_host_key",
            honeypot_id=honeypot_id,
            fake_username=fake_username,
            fake_password=fake_password,
        )
    else:
        print(f"Unknown service_type: {service_type}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
