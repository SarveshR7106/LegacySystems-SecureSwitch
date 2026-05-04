# 🔐 Universal Secure Switch for Legacy Systems

A socket-based secure communication tunnel that transparently encrypts traffic between legacy systems using **AES-256-GCM** encryption and **ECDH key exchange** — without modifying the legacy systems themselves.

***

## 📐 System Architecture

```
[Legacy A] ──► [Switch A] ══════(Encrypted Tunnel)══════► [Switch B] ──► [Legacy B]
 legacyA.py    switchA.py                                  switchB.py     legacyB.py
               encrypts outgoing                           decrypts incoming
```

> **PC1 (Sender):** `legacyA.py` + `switchA.py`  
> **PC2 (Receiver + Dashboard):** `switchB.py` + `legacyB.py` + `backend/server.py` + `frontend/index.html`

***

## 📁 Project Structure

```
project/
├── backend/
│   └── server.py          # Flask dashboard backend (log receiver)
├── frontend/
│   └── index.html         # Real-time monitoring dashboard
├── switchA.py             # Secure Switch A (encrypts outgoing data)
├── switchB.py             # Secure Switch B (decrypts incoming data)
├── legacyA.py             # Legacy sender (no modification needed)
├── legacyB.py             # Legacy receiver (no modification needed)
└── README.md
```

***

## ⚙️ IP Address Configuration

Three files contain `IP_ADDRESS` as a placeholder. **You must replace it before running.**

| File | What to change | Single PC | Two PCs (LAN) |
|------|----------------|-----------|----------------|
| `switchA.py` | `PC2_IP = "IP_ADDRESS"` | `"127.0.0.1"` | PC2's LAN IP |
| `switchB.py` | `PC2_IP = "IP_ADDRESS"` | `"127.0.0.1"` | PC2's LAN IP |
| `frontend/index.html` | `const IP = "IP_ADDRESS"` | `"127.0.0.1"` | PC2's LAN IP |

> `legacyA.py`, `legacyB.py`, and `backend/server.py` do **not** need any changes.

***

## 📦 Install Dependencies

Run this on **every machine** before starting:

```bash
pip install cryptography pycryptodomex flask
```

***

## 🖥️ Mode 1 — Single Computer (Localhost)

All components run on the **same machine** using `127.0.0.1`.

### Step 1 — Replace `IP_ADDRESS` in all three files

**`switchA.py`** and **`switchB.py`**:
```python
# Before
PC2_IP = "IP_ADDRESS"

# After
PC2_IP = "127.0.0.1"
```

**`frontend/index.html`**:
```javascript
// Before
const IP = "IP_ADDRESS"

// After
const IP = "127.0.0.1"
```

### Step 2 — Open 5 terminals and run in this exact order

> ⚠️ **Order matters!** Always start the B side before the A side.

```bash
# Terminal 1 — Dashboard backend
cd backend
python server.py
```

```bash
# Terminal 2 — Switch B (listens on port 7000)
python switchB.py
```

```bash
# Terminal 3 — Legacy B (listens on port 6000)
python legacyB.py
```

```bash
# Terminal 4 — Switch A (connects to Switch B)
python switchA.py
```

```bash
# Terminal 5 — Legacy A (sends messages)
python legacyA.py
```

### Step 3 — Open the dashboard

Open `frontend/index.html` in your browser.

### Port Map

```
legacyA.py ──► :5000 ──► switchA.py
switchA.py ══► :7000 ══► switchB.py   (encrypted tunnel)
switchB.py ──► :6000 ──► legacyB.py
backend    ──► :8000                  (dashboard log API)
```

***

## 🌐 Mode 2 — Two Computers on the Same Wi-Fi / LAN

Both PCs must be connected to the **same network** (same Wi-Fi router or LAN switch).

### Step 1 — Find PC2's local IP address

Run this on **PC2**:

```bash
# Windows
ipconfig
# Look for "IPv4 Address" under your Wi-Fi adapter

# Linux / macOS
ip a
# or
hostname -I
```

You'll get something like `192.168.1.5` or `172.16.x.x`. Note it down.

### Step 2 — Replace `IP_ADDRESS` in all three files with PC2's LAN IP

**`switchA.py`** (on PC1) and **`switchB.py`** (on PC2):
```python
# Before
PC2_IP = "IP_ADDRESS"

# After — use PC2's actual IP from Step 1
PC2_IP = "192.168.1.5"
```

**`frontend/index.html`** (on PC2):
```javascript
// Before
const IP = "IP_ADDRESS"

// After
const IP = "192.168.1.5"
```

> All three files must use the **same IP** — PC2's address.

### Step 3 — Allow ports through PC2's firewall

```bash
# Windows — run as Administrator
netsh advfirewall firewall add rule name="Switch B" dir=in action=allow protocol=TCP localport=7000
netsh advfirewall firewall add rule name="Dashboard" dir=in action=allow protocol=TCP localport=8000

# Linux
sudo ufw allow 7000/tcp
sudo ufw allow 8000/tcp
```

### Step 4 — Start PC2 first

> ⚠️ **Always start PC2 before PC1.**

```bash
# PC2 — Terminal 1: Dashboard backend
cd backend
python server.py

# PC2 — Terminal 2: Switch B
python switchB.py

# PC2 — Terminal 3: Legacy B
python legacyB.py
```

### Step 5 — Then start PC1

```bash
# PC1 — Terminal 1: Switch A
python switchA.py

# PC1 — Terminal 2: Legacy A
python legacyA.py
```

### Step 6 — Open the dashboard

Open `frontend/index.html` in a browser on PC2 (or any browser that can reach PC2's IP).

***

## 🔒 Security Features

| Feature | Details |
|---------|---------|
| Encryption | AES-256-GCM (authenticated encryption) |
| Key Exchange | ECDH over SECP256R1 curve |
| Key Derivation | HKDF with SHA-256 |
| Integrity | GCM authentication tag (prevents tampering) |

***

## 🐛 Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `TimeoutError: [WinError 10060]` | `IP_ADDRESS` was never replaced, or IP is unreachable | Set correct IP in `switchA.py`, `switchB.py`, and `index.html` |
| `ConnectionRefusedError` on port 7000 | `switchB.py` not started yet | Always start Switch B **before** Switch A |
| `ConnectionRefusedError` on port 6000 | `legacyB.py` not started yet | Start Legacy B before Switch B tries to connect |
| Dashboard shows no logs | Wrong IP in `index.html` or port 8000 blocked | Re-check `const IP` in `index.html` and firewall rules |
| `OSError: [Errno 98] Address already in use` | Port still occupied from a previous run | Wait 30s or run: `fuser -k 7000/tcp` |

***

## 🚀 Technologies Used

- **Python** — Socket programming, threading
- **Cryptography** — AES-256-GCM, ECDH (`cryptography`, `pycryptodomex`)
- **Flask** — Dashboard log API backend
- **HTML / CSS / JavaScript** — Real-time monitoring frontend

***

## 👤 Author

Developed as part of a Computer Networks project to demonstrate transparent security for legacy systems.