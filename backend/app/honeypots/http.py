import asyncio
from datetime import datetime, timezone

from app.services.event_logger import log_event

MAX_REQUEST_SIZE = 8192  # bytes, prevent memory abuse


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, banner: str, hostname: str, honeypot_id: str):
    addr = writer.get_extra_info("peername")
    source_ip, source_port = addr[0], addr[1]

    try:
        data = await asyncio.wait_for(reader.read(MAX_REQUEST_SIZE), timeout=5)
    except asyncio.TimeoutError:
        writer.close()
        return

    if not data:
        writer.close()
        return

    request_text = data.decode(errors="replace")
    lines = request_text.split("\r\n")
    request_line = lines[0] if lines else ""

    parts = request_line.split(" ")
    method = parts[0] if len(parts) > 0 else "UNKNOWN"
    path = parts[1] if len(parts) > 1 else "/"

    timestamp = datetime.now(timezone.utc).isoformat()
    print(f"[{timestamp}] {source_ip}:{source_port} {method} {path}")

    log_event(
        honeypot_id=honeypot_id,
        service="http",
        source_ip=source_ip,
        source_port=source_port,
        event_type="http_request",
        metadata={"method": method, "path": path},
    )

    body = f"<html><body><h1>{hostname}</h1></body></html>"
    response = (
        f"HTTP/1.1 200 OK\r\n"
        f"Server: {banner}\r\n"
        f"Content-Type: text/html\r\n"
        f"Content-Length: {len(body)}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
        f"{body}"
    )

    writer.write(response.encode())
    await writer.drain()
    writer.close()


async def run_http_honeypot(port: int, banner: str = "nginx", hostname: str = "server", honeypot_id: str = "manual-test"):
    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, banner, hostname, honeypot_id), "0.0.0.0", port
    )
    print(f"HTTP honeypot listening on port {port}")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(run_http_honeypot(8080))
