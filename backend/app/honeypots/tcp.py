import asyncio
import time
from datetime import datetime, timezone

from app.services.event_logger import log_event

MAX_RECEIVE_SIZE = 4096  # bytes, prevent memory abuse
READ_TIMEOUT = 10  # seconds


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, banner: str, honeypot_id: str):
    addr = writer.get_extra_info("peername")
    source_ip, source_port = addr[0], addr[1]
    start_time = time.monotonic()

    timestamp = datetime.now(timezone.utc).isoformat()
    print(f"[{timestamp}] CONNECT {source_ip}:{source_port}")

    log_event(
        honeypot_id=honeypot_id,
        service="tcp",
        source_ip=source_ip,
        source_port=source_port,
        event_type="tcp_connect",
    )

    if banner:
        writer.write((banner + "\r\n").encode())
        await writer.drain()

    received = b""
    try:
        while len(received) < MAX_RECEIVE_SIZE:
            chunk = await asyncio.wait_for(reader.read(1024), timeout=READ_TIMEOUT)
            if not chunk:
                break
            received += chunk
    except asyncio.TimeoutError:
        pass

    duration = round(time.monotonic() - start_time, 2)
    timestamp = datetime.now(timezone.utc).isoformat()
    print(f"[{timestamp}] DISCONNECT {source_ip}:{source_port} bytes_received={len(received)} duration={duration}s")

    log_event(
        honeypot_id=honeypot_id,
        service="tcp",
        source_ip=source_ip,
        source_port=source_port,
        event_type="tcp_disconnect",
        metadata={"bytes_received": len(received), "duration_seconds": duration},
    )

    writer.close()


async def run_tcp_honeypot(port: int, banner: str = "Welcome to legacy management service.", honeypot_id: str = "manual-test"):
    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, banner, honeypot_id), "0.0.0.0", port
    )
    print(f"TCP honeypot listening on port {port}")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(run_tcp_honeypot(2323))
