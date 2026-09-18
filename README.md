# 🎯 HoneyForge

**Forge deception. Observe attackers. Zero containers required.**

HoneyForge lightweight, standalone honeypot platform. Spawns deceptive HTTP, TCP, SSH services as bare-metal Linux processes. Log attacker interactions, reconstruct session timelines, view dynamic metrics.

---

## 📸 Overview

<img width="1917" height="777" alt="Screenshot 2026-09-18 153820" src="https://github.com/user-attachments/assets/106f5333-c0f2-45f6-bc62-837c10aee2c1" />
*Live dashboard monitoring attacker sessions and incoming events.*

---

## ⚡ Core Features

* 🍯 **Multi-Protocol Deception**: HTTP, raw TCP, interactive SSH fake shells (`asyncssh`).
* ⏱️ **Session Timeline**: Groups scattered interactions into cohesive attack sessions.
* ⚡ **Zero-Docker Overhead**: Lightweight Python subprocesses. No heavy containers.
* 📊 **Real-time Monitoring**: Next.js dashboard + FastAPI event collector.

---

## 🏗️ How It Works

```text
 Attacker Traffic ──> [ Honeypot Process ] ──> [ Event Collector ] ──> [ SQLite ]
                                                                            │
 Dashboard <── FastAPI REST <───────────────────────────────────────────────┘
```

---

## 🚀 Quickstart

### 1. Backend

```bash
git clone https://github.com/anshnarsale/honeyforge.git
cd honeyforge/backend

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python3 -m app.init_db
uvicorn app.main:app --reload
```
> API runs at `http://127.0.0.1:8000` | Docs at `/docs`

### 2. Frontend

```bash
cd ../frontend
npm install
npm run dev
```
> Dashboard runs at `http://localhost:3000`

---

## 📸 Attack Simulations

### SSH Fake Shell

```bash
ssh admin@127.0.0.1 -p 2222
# Password: admin123

# Canned fake shell responds safely — commands never touch host:
whoami
cat /etc/passwd
```

### HTTP & TCP Probing

```bash
# HTTP Probe
curl -X POST http://127.0.0.1:8080/admin/login

# TCP Payload
nc 127.0.0.1 9000
```

---

## ⚠️ Security Notice

* **No Real Secrets**: Never put production keys in honeypot configs.
* **Local MVP**: No API auth currently. Keep inside isolated LAN or loopback (`127.0.0.1`).

---

## 📂 Project Structure

```text
HoneyForge/
├── backend/       # FastAPI, SQLAlchemy, asyncssh honeypots
├── frontend/      # Next.js, React, Tailwind CSS
└── docs/images/   # Screenshots
```

---

## 📜 License & Author

**Author:** Ansh Narsale ([GitHub](https://github.com/anshnarsale) | [Portfolio](https://anshnarsale.netlify.app/))  
**License:** MIT
