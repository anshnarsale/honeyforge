<div align="center">

```
   _   _                        ______                    
  | | | | ___  _ __   ___ _   _|  ____|__  _ __ __ _  ___ 
  | |_| |/ _ \| '_ \ / _ \ | | | |__ / _ \| '__/ _` |/ _ \
  |  _  | (_) | | | |  __/ |_| |  __| (_) | | | (_| |  __/
  |_| |_|\___/|_| |_|\___|\__, |_|   \___/|_|  \__, |\___|
                           __/ |                __/ |     
                          |___/                |___/      
```

### 🍯 Forge deception. Observe attackers. Zero containers required.

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![No Docker](https://img.shields.io/badge/Docker-Not%20Required-red?style=for-the-badge&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

</div>

---

A lightweight, no-Docker honeypot platform that spins up **real** HTTP, TCP, and SSH decoys as plain Linux processes — no containers, no orchestration, just Python and sockets. Watch attackers walk straight into the trap, replay every command they typed, and never let a single one of them touch your real system.

<div align="center">

### 📸 See it in action

<img width="935" height="777" alt="Screenshot 2026-09-21 123604" src="https://github.com/user-attachments/assets/b91ed48b-0574-4513-8838-3a513de77096" />

*Live stats · one-click control · real-time event feed*

</div>

---

## ⚡ Why HoneyForge

> 🎭 **It's not a simulation of a honeypot. It's a real one.**  
> Real SSH handshakes. Real HTTP responses. Real attacker tools get fully fooled — while every "command" they run dead-ends into a canned response, never a real shell.

<table>
<tr>
<td width="33%" valign="top">

### 🌐 HTTP Trap
Configurable port, banner & hostname. Logs method, path, headers, source — every request, every time.

</td>
<td width="33%" valign="top">

### 🔌 TCP Trap
Raw socket listener with custom banner. Tracks bytes received and connection duration, with hard size limits.

</td>
<td width="33%" valign="top">

### 🐚 SSH Trap
Genuine SSH protocol via `asyncssh`. Fake login, fake shell, zero real execution — attackers type `cat /etc/passwd`, they get fiction.

</td>
</tr>
</table>

**Plus:** a live dashboard with auto-refreshing stats, one-click create/start/stop/delete, and fully configurable bait — set your own fake usernames, passwords, banners, and hostnames per trap.

---

## 🏗️ Architecture

```text
                    Attacker Traffic
                          │
                          ▼
              ┌───────────────────────┐
              │   Honeypot Process    │  ← spawned via validated
              │  (HTTP / TCP / SSH)   │     subprocess, never shell-injected
              └───────────┬───────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │    Event Collector    │──────┐
              └───────────┬───────────┘      │
                          │                  ▼
                          ▼            ┌───────────┐
              ┌───────────────────────┐│  SQLite   │
              │   Session Tracker     ││           │
              └───────────────────────┘└─────┬─────┘
                                              │
                                              ▼
                                   ┌─────────────────────┐
                                   │   FastAPI REST API   │
                                   └──────────┬───────────┘
                                              │
                                              ▼
                                   ┌─────────────────────┐
                                   │   Next.js Dashboard  │
                                   └─────────────────────┘
```

---

## 🚀 Quickstart

<details>
<summary><b>🐍 Backend Setup</b></summary>

```bash
git clone https://github.com/anshnarsale/honeyforge.git
cd honeyforge/backend

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python3 -m app.init_db
uvicorn app.main:app --reload
```
API live at `http://127.0.0.1:8000` · Interactive docs at `/docs`

</details>

<details>
<summary><b>⚛️ Frontend Setup</b></summary>

```bash
cd ../frontend
npm install
npm run dev
```
Dashboard live at `http://localhost:3000`

</details>

---

## 🎯 Deploy Your First Trap

**1.** Open the dashboard → fill in **Create Honeypot**: name, type, port, optional banner/hostname/fake creds.
**2.** Hit **Create** → **Start**. It's now a live process on your chosen port.
**3.** Go attack it yourself and watch the dashboard light up:

<table>
<tr><th>Type</th><th>Command</th></tr>
<tr>
<td>🌐 HTTP</td>
<td>

```bash
curl -i http://127.0.0.1:<port>/admin
```

</td>
</tr>
<tr>
<td>🔌 TCP</td>
<td>

```bash
nc 127.0.0.1 <port>
```

</td>
</tr>
<tr>
<td>🐚 SSH</td>
<td>

```bash
ssh <fake_username>@127.0.0.1 -p <port>
# default: admin / admin123
```

</td>
</tr>
</table>

Once inside the SSH shell, try `whoami`, `hostname`, `ls`, `cat configs/app.conf` — every keystroke logged, nothing real ever runs.

**4.** Watch it land in **Recent Events**, live, no refresh needed.

---

## ⚠️ Security Ground Rules

- 🚫 **No real secrets, ever.** Bait credentials, keys, and files must always be synthetic.
- 🔒 **The SSH shell cannot break out.** Commands are pattern-matched against canned responses — there is no code path to a real shell.
- 🌐 **This is MVP stage — no dashboard auth yet.** Keep it on `127.0.0.1` or an isolated lab network. Do not expose it to the public internet.

---

## 🗺️ Roadmap

- [ ] Per-path fake content (realistic `/login`, `/admin` HTML pages)
- [ ] Dedicated low-privilege Linux user + systemd sandboxing
- [ ] Dashboard authentication + rate limiting
- [ ] FTP / Telnet / SMTP traps
- [ ] CLI tool (`honeyforge create`, `honeyforge start <id>`, ...)
- [ ] JSON / CSV / HTML incident reports
- [ ] Attacker analytics — top paths, top commands, session duration, ASN lookup

---

## 📂 Project Structure

```text
honeyforge/
├── backend/     FastAPI · SQLAlchemy · asyncssh honeypots
└── frontend/    Next.js · React · Tailwind CSS
```

---

<div align="center">

**Built by [Ansh Narsale](https://github.com/anshnarsale)** · [Portfolio](https://anshnarsale.netlify.app/)

MIT Licensed · ⭐ Star this repo if HoneyForge caught you an attacker

</div>
