# 🛡️ CyberLog-Sentinel

**CyberLog-Sentinel** is a beginner-friendly Mini SIEM (Security Information and Event Management) system developed using Python.

It monitors authentication logs, parses security events, detects possible brute-force attacks, generates security alerts, and stores detected threats in an SQLite database.

The project also provides a FastAPI backend for accessing security events through REST APIs and Swagger documentation.

---

## 📌 Features

* 🔍 Security log parsing
* 🌐 IP address extraction
* 🕐 Timestamp extraction
* 🔐 Failed Login detection
* ✅ Successful Login detection
* 🚨 Brute Force Attack detection
* ⚠️ HIGH risk alert generation
* 💾 SQLite database storage
* 🔄 Real-time log monitoring
* 🚀 FastAPI REST API
* 📖 Swagger API documentation
* 🖥️ Command-line monitoring

---

## 🏗️ Project Architecture

```text
                 ┌─────────────────┐
                 │    auth.log     │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │    parser.py    │
                 │  Log Parser     │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │   detector.py   │
                 │ Detection Engine│
                 └────────┬────────┘
                          │
                          ▼
                Brute Force Detected
                          │
                          ▼
                 ┌─────────────────┐
                 │   database.py   │
                 │     SQLite      │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │     FastAPI     │
                 │      app.py     │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Swagger / REST  │
                 └─────────────────┘
```

---

## 📂 Project Structure

```text
CyberLog-Sentinel/
│
├── backend/
│   ├── app.py
│   ├── parser.py
│   ├── detector.py
│   ├── database.py
│   ├── monitor.py
│   ├── cyberlog.db
│   │
│   └── sample_logs/
│       └── auth.log
│
├── tests/
│   └── test_detector.py
│
├── screenshots/
│   ├── realtime-monitor.png
│   ├── swagger-api.png
│   └── events-api.png
│
├── README.md
├── LICENSE
└── requirements.txt
```

---

## 🛠️ Technologies Used

| Technology          | Purpose                   |
| ------------------- | ------------------------- |
| Python              | Core programming language |
| FastAPI             | REST API backend          |
| Uvicorn             | FastAPI server            |
| SQLite              | Security event database   |
| Regular Expressions | Log parsing               |
| PowerShell / CMD    | Testing and monitoring    |

---

## 🔍 How It Works

### 1. Log Collection

The system reads authentication logs from:

```text
backend/sample_logs/auth.log
```

Example:

```text
2026-09-06 10:15:21 Failed login from 192.168.1.10
```

---

### 2. Log Parsing

`parser.py` extracts important information from every log.

Example:

```text
Timestamp  → 2026-09-06 10:15:21
IP Address → 192.168.1.10
Event Type → Failed Login
```

The log is converted into a structured event.

---

### 3. Threat Detection

`detector.py` counts failed login attempts for each IP address.

Current detection rule:

```text
5 or more failed logins
        ↓
Brute Force Attack
        ↓
Risk Level: HIGH
```

---

### 4. Alert Generation

When an IP crosses the threshold, the system generates an alert.

Example:

```text
[ALERT] BRUTE FORCE ATTACK DETECTED

IP Address   : 192.168.1.10
Failed Login : 5
Risk Level   : HIGH
Timestamp    : 2026-09-06 10:15:37
```

---

### 5. Database Storage

Detected threats are stored in the SQLite database:

```text
cyberlog.db
```

The database stores information such as:

* Timestamp
* IP Address
* Event Type
* Failed Attempts
* Risk Level
* Raw Log

---

## 🔄 Real-Time Monitoring

The `monitor.py` script continuously watches the authentication log for new entries.

Run:

```powershell
cd backend
python monitor.py
```

The monitor waits for new log entries.

Example:

```text
CyberLog-Sentinel Real-Time Monitor

Monitoring: sample_logs/auth.log
Waiting for new log entries...
```

When a new log appears:

```text
[NEW LOG]
Timestamp   : 2026-09-06 20:30:01
IP Address  : 192.168.1.20
Event Type  : Failed Login
```

If the threshold is crossed:

```text
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
[ALERT] BRUTE FORCE ATTACK DETECTED
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
IP Address   : 192.168.1.20
Failed Login : 5
Risk Level   : HIGH
Timestamp    : 2026-09-06 20:35:05
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```

---

## 🚀 FastAPI

The project also provides a FastAPI backend.

Start the API:

```powershell
cd backend
uvicorn app:app --reload --port 8001
```

The API runs on:

```text
http://127.0.0.1:8001
```

### Available Endpoints

#### Home

```text
GET /
```

Returns the API status.

#### Events

```text
GET /events
```

Returns stored security events.

Example response:

```json
{
    "total_events": 1,
    "events": [
        {
            "id": 1,
            "timestamp": "2026-09-06 10:15:37",
            "ip_address": "192.168.1.10",
            "event_type": "Brute Force Attack",
            "failed_attempts": 5,
            "risk_level": "HIGH",
            "raw_log": "..."
        }
    ]
}
```

---

## 📖 Swagger Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8001/docs
```

From Swagger UI, available API endpoints can be tested directly from the browser.

---

## 🧪 Testing

The project includes basic automated tests for the detection engine.

Run:

```powershell
pytest
```

The tests verify that the brute-force detection logic correctly identifies suspicious login activity.

---

## 📸 Screenshots

### Real-Time Monitoring

![Real-Time Monitor](screenshots/realtime-monitor.png)

### FastAPI Swagger

![Swagger API](screenshots/swagger-api.png)

### Security Events API

![Events API](screenshots/events-api.png)

---

## 🎯 Current Detection Logic

Currently, CyberLog-Sentinel focuses on detecting brute-force login attempts.

```text
Failed Login Attempts

       1
       ↓
    Normal

       2
       ↓
    Normal

       3
       ↓
    Normal

       4
       ↓
    Suspicious

       5+
       ↓
🚨 Brute Force Attack
       ↓
    HIGH Risk
```

---

## 🔐 Security Purpose

The purpose of this project is to demonstrate the basic working principles of a SIEM system:

```text
Log Collection
      ↓
Log Parsing
      ↓
Event Analysis
      ↓
Threat Detection
      ↓
Alert Generation
      ↓
Event Storage
      ↓
API Access
```

---

## 🚧 Future Improvements

Possible future improvements include:

* Port Scan Detection
* Suspicious Login Detection
* Multiple risk levels
* Advanced risk scoring
* IP reputation checking
* Authentication dashboards
* More log formats
* Email/notification alerts
* Advanced correlation rules
* Web-based security dashboard

---

## 👨‍💻 Project Status

**Current Status:** Working Prototype

CyberLog-Sentinel currently demonstrates real-time authentication log monitoring, brute-force detection, alert generation, database storage, and API access.

---

## 📚 Learning Objectives

This project was created to understand practical concepts related to:

* Cybersecurity monitoring
* SIEM fundamentals
* Log analysis
* Threat detection
* Python programming
* REST APIs
* SQLite databases
* Real-time monitoring
* Security event analysis

---

## ⚠️ Disclaimer

This project is developed for educational and cybersecurity learning purposes.

It should only be used with logs and systems that you are authorized to monitor.
