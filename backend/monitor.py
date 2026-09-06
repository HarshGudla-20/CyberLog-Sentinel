
import time

from parser import parse_log_line
from detector import detect_brute_force
from database import create_database, insert_event


LOG_FILE = "sample_logs/auth.log"


def monitor_logs():

    print("=" * 60)
    print("        CyberLog-Sentinel Real-Time Monitor")
    print("=" * 60)

    print(f"Monitoring: {LOG_FILE}")
    print("Waiting for new log entries...")
    print("Press CTRL+C to stop.")
    print("=" * 60)

    # Current position in log file
    position = 0

    # Store IPs that have already generated an alert
    alerted_ips = set()

    while True:

        # Open and close the file every cycle
        # This allows PowerShell to write new logs
        with open(LOG_FILE, "r", encoding="utf-8") as file:

            file.seek(position)

            new_lines = file.readlines()

            position = file.tell()

        # Process only newly added logs
        for line in new_lines:

            line = line.strip()

            if not line:
                continue

            # Parse log
            event = parse_log_line(line)

            print("\n[NEW LOG]")
            print(f"Timestamp   : {event['timestamp']}")
            print(f"IP Address  : {event['ip_address']}")
            print(f"Event Type  : {event['event_type']}")

        # Read complete log file for detection
        with open(LOG_FILE, "r", encoding="utf-8") as log_file:

            all_lines = log_file.readlines()

        # Parse all logs
        parsed_events = []

        for log in all_lines:

            log = log.strip()

            if log:
                parsed_events.append(parse_log_line(log))

        # Detect brute-force attacks
        threats = detect_brute_force(parsed_events)

        # Process detected threats
        for threat in threats:

            ip = threat["ip_address"]

            # Only generate alert once per IP
            if ip not in alerted_ips:

                print("\n" + "!" * 60)
                print("[ALERT] BRUTE FORCE ATTACK DETECTED")
                print("!" * 60)

                print(f"IP Address   : {threat['ip_address']}")
                print(f"Failed Login : {threat['failed_attempts']}")
                print(f"Risk Level   : {threat['risk_level']}")
                print(f"Timestamp    : {threat['timestamp']}")

                print("!" * 60)

                # Save threat to database
                insert_event(threat)

                # Remember this IP
                alerted_ips.add(ip)

        # Wait before checking again
        time.sleep(1)


if __name__ == "__main__":

    # Create database if it doesn't exist
    create_database()

    try:

        monitor_logs()

    except KeyboardInterrupt:

        print("\n")
        print("=" * 60)
        print("Monitoring stopped.")
        print("=" * 60)
