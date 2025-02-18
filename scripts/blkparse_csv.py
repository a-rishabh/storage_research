import sys
import csv

class EventEntry:
    def __init__(self, event_type=None, timestamp=None, duration=None, opcode=None, lba=None, xfr_len=None, pid=None):
        self.event_type = event_type
        self.timestamp = timestamp
        self.duration = duration
        self.opcode = opcode
        self.lba = lba
        self.xfr_len = xfr_len
        self.pid = pid

def calculate_completion_times(file_name, output_csv):
    try:
        with open(file_name, "r", encoding='utf-8', errors='ignore') as input_file_ptr:
            lines = input_file_ptr.readlines()
        print("File read!!")

    except Exception as e:
        sys.stderr.write(f"Error opening file: {e}\n")
        sys.exit(1)

    indices = {
        'target': 0,
        'time': 3,
        'type': 5,
        'opcode': 6,
        'lba': 7,
        'xfr_len': 9,
        'pid': 4,
    }

    pending_events = {}
    completion_times = []
    number = 0  # Initialize a counter for each row

    for line in lines:
        parts = line.split()
        
        if len(parts) < 10:  # Adjusted to ensure all necessary fields are present
            continue

        try:
            event_type = parts[indices['type']]
            timestamp = float(parts[indices['time']]) * 1e6  # Convert to microseconds
            pid = int(parts[indices['pid']])
            original_opcode = parts[indices['opcode']]  # Store the original opcode
            opcode = original_opcode  # Use opcode instead of command
            
            if 'W' in opcode:
                opcode = '0x8A'
            elif 'R' in opcode:
                opcode = '0x88'
            lba = parts[indices['lba']]
            xfr_len = parts[indices['xfr_len']]

            if event_type == "D":
                if pid not in pending_events:
                    pending_events[pid] = {}
                pending_events[pid][(opcode, lba, xfr_len)] = timestamp
            elif event_type == 'C':
                for pending_pid, events in pending_events.items():
                    for key in list(events.keys()):
                        if key[:3] == (opcode, lba, xfr_len):
                            issued_time = events[key]
                            duration = int(timestamp - issued_time)  # Convert to int
                            tag = f"{original_opcode}_{lba}_{xfr_len}"  # Use original opcode for tag
                            completion_times.append((number, opcode, tag, hex(int(lba)), hex(int(xfr_len)), int(issued_time), duration))
                            del events[key]
                            number += 1  # Increment the counter
                            break

        except (ValueError, IndexError, KeyError) as e:
            sys.stderr.write(f"Skipping malformed line: {e}\n")
            continue

    with open(output_csv, "w", newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["number", "opcode", "tag", "lba", "xfrlen", "Completion time", "response"])
        for number, opcode, tag, lba, xfr_len, completion_time, response in completion_times:
            csv_writer.writerow([number, opcode, tag, lba, xfr_len, completion_time, response])

    print(f"Completion times written to {output_csv}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 script.py <input_file> <output_csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_csv = sys.argv[2]
    calculate_completion_times(input_file, output_csv)