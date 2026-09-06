import re


def parse_log_line(line):

    """
    Parse a single security log line.
    """

    # Extract timestamp
    timestamp_match = re.search(
        r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}",
        line
    )

    # Extract IP address
    ip_match = re.search(
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        line
    )

    # Determine event type
    if "Failed login" in line:
        event_type = "Failed Login"

    elif "Successful login" in line:
        event_type = "Successful Login"

    elif "Port scan" in line:
        event_type = "Port Scan"

    else:
        event_type = "Unknown"

    # Create structured event
    event = {
        "timestamp": timestamp_match.group() if timestamp_match else None,
        "ip_address": ip_match.group() if ip_match else None,
        "event_type": event_type,
        "raw_log": line.strip()
    }

    return event