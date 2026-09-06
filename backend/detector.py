FAILED_LOGIN_THRESHOLD = 5


def detect_brute_force(events):

    failed_attempts = {}

    # Count failed logins for each IP
    for event in events:

        if event["event_type"] == "Failed Login":

            ip = event["ip_address"]

            if ip:

                if ip not in failed_attempts:
                    failed_attempts[ip] = []

                failed_attempts[ip].append(event)

    threats = []

    # Check every IP
    for ip in failed_attempts:

        events_list = failed_attempts[ip]

        count = len(events_list)

        if count >= FAILED_LOGIN_THRESHOLD:

            latest_event = events_list[-1]

            threat = {
                "timestamp": latest_event["timestamp"],
                "ip_address": ip,
                "event_type": "Brute Force Attack",
                "failed_attempts": count,
                "risk_level": "HIGH",
                "raw_log": latest_event["raw_log"]
            }

            threats.append(threat)

    return threats