import asyncio
from datetime import datetime, timezone

import asyncssh

FAKE_USERNAME = "admin"
FAKE_PASSWORD = "admin123"
HOSTNAME = "finance-server"

FAKE_FILES = {
    "configs/app.conf": "db_host=localhost\ndb_port=5432\napp_env=production\n",
}

FAKE_LS_OUTPUT = "backup\nconfigs\nlogs\nreports"


def log(msg: str):
    timestamp = datetime.now(timezone.utc).isoformat()
    print(f"[{timestamp}] {msg}")


class HoneypotSSHServer(asyncssh.SSHServer):
    def connection_made(self, conn):
        peer = conn.get_extra_info("peername")
        self.source_ip = peer[0] if peer else "unknown"
        log(f"SSH connection from {self.source_ip}")

    def begin_auth(self, username):
        self.username = username
        return True

    def password_auth_supported(self):
        return True

    def validate_password(self, username, password):
        success = username == FAKE_USERNAME and password == FAKE_PASSWORD
        log(f"AUTH_ATTEMPT source={self.source_ip} username={username} password={password} success={success}")
        return success


async def handle_session(process: asyncssh.SSHServerProcess):
    process.stdout.write(f"Welcome to {HOSTNAME}\r\n")

    while True:
        process.stdout.write("$ ")
        try:
            line = await process.stdin.readline()
        except asyncssh.BreakReceived:
            break

        if not line:
            break

        command = line.strip()
        if not command:
            continue

        log(f"COMMAND {command}")

        if command == "exit":
            break
        elif command == "whoami":
            process.stdout.write(f"{FAKE_USERNAME}\r\n")
        elif command == "hostname":
            process.stdout.write(f"{HOSTNAME}\r\n")
        elif command == "ls":
            process.stdout.write(f"{FAKE_LS_OUTPUT}\r\n")
        elif command.startswith("cat "):
            path = command[4:].strip()
            content = FAKE_FILES.get(path, f"cat: {path}: No such file or directory")
            process.stdout.write(f"{content}\r\n")
        else:
            process.stdout.write(f"{command}: command not found\r\n")

    process.exit(0)


async def run_ssh_honeypot(port: int, host_key_path: str):
    await asyncssh.create_server(
        HoneypotSSHServer,
        "0.0.0.0",
        port,
        server_host_keys=[host_key_path],
        process_factory=handle_session,
    )
    print(f"SSH honeypot listening on port {port}")


async def main():
    await run_ssh_honeypot(2222, "app/honeypots/keys/ssh_host_key")
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
