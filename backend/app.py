from fastapi import FastAPI

from parser import parse_log_line
from detector import detect_brute_force
from database import create_database, insert_event, get_all_events


app = FastAPI(
    title="CyberLog-Sentinel",
    description="Mini SIEM Security Monitoring API",
    version="1.0"
)


# Create database when application starts
create_database()


@app.get("/")
def home():

    return {
        "message": "CyberLog-Sentinel API is running",
        "status": "online"
    }


@app.get("/events")
def events():

    events = get_all_events()

    result = []

    for event in events:

        result.append({
            "id": event[0],
            "timestamp": event[1],
            "ip_address": event[2],
            "event_type": event[3],
            "failed_attempts": event[4],
            "risk_level": event[5],
            "raw_log": event[6]
        })

    return {
        "total_events": len(result),
        "events": result
    }


@app.get("/detect")
def detect():

    logs = []

    # Read logs from auth.log
    with open("sample_logs/auth.log", "r") as file:

        for line in file:

            line = line.strip()

            if line:
                logs.append(line)

    # Parse logs
    parsed_events = []

    for log in logs:

        event = parse_log_line(log)

        parsed_events.append(event)

    # Detect threats
    threats = detect_brute_force(parsed_events)

    # Save detected threats
    for threat in threats:

        insert_event(threat)

    return {
        "total_events": len(parsed_events),
        "threats_detected": len(threats),
        "threats": threats
    }