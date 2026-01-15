import csv
import json
from datetime import datetime
from websockets.sync.client import connect

def log_data():
    # Creating a filename based on the start time of the script
    filename = f"telemetry_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    message_count = 0

    print(f"Connecting to stream... saving to {filename}")

    try:
        with connect("ws://10.12.123.45:3333/data", open_timeout=10) as websocket:
            with open(filename, mode='w', newline='') as csv_file:
                writer = None

                for message in websocket:
                    try:
                        data = json.loads(message)
                    
                        # Skip heartbeat/idle states if state is 0
                        '''
                        if data.get('state') == 0:
                            continue
'''
                        # 1. Flatten the data structure
                        # Timestamps are now expected to be inside the 'data' dict from the WS
                        row = {}
                        for key, value in data.items():
                            if isinstance(value, list):
                                # Flatten lists into individual columns (e.g., acc_0, acc_1)
                                for i, val in enumerate(value):
                                    row[f"{key}_{i}"] = val
                            else:
                                row[key] = value

                        # 2. Initialize headers on the first valid message received
                        if writer is None:
                            writer = csv.DictWriter(csv_file, fieldnames=row.keys())
                            writer.writeheader()

                        # 3. Write data
                        writer.writerow(row)
                        message_count += 1
                        
                        # Optional: flush periodically or print status
                        if message_count % 100 == 0:
                            print(f"Logged {message_count} rows...")

                    except json.JSONDecodeError:
                        continue 
                    except Exception as e:
                        print(f"Error processing message: {e}")
                        continue

    except Exception as e:
        print(f"Connection error: {e}")

    print(f"Logging complete. Captured {message_count} messages in {filename}")

if __name__ == "__main__":
    try:
        log_data()
    except KeyboardInterrupt:
        print("\nManual stop. Data saved.") 