import pandas as pd
import matplotlib.pyplot as plt

# File path
file_path = "/Users/aragorn/Documents/chandra_research/Benchmarking/hdd_01_30_1e/parsed_output_hdd.txt"
columns = ["major", "minor", "cpu", "seq", "timestamp", "pid", "event_type", "rwbs", "sector", "process"]
data = []

# Keywords indicating the start of the summary (look at the bottom of the parsed.txt file)
summary_keywords = ["Reads Queued", "Throughput", "Events"]

line_count = 0

with open(file_path, "r") as f:
    for line in f:
        parts = line.strip().split()

        # if line_count > 2000:
        #     break

        if any(keyword in line for keyword in summary_keywords):
            break

        if len(parts) >= 9:
            try:
                timestamp = float(parts[3])  #  timestamp
                event_type = parts[5]  # Event type
                data.append([timestamp, event_type])
                line_count += 1
            except ValueError:
                continue  # Skip invalid lines

df = pd.DataFrame(data, columns=["timestamp", "event_type"])

if df.empty:
    print("DataFrame is empty. No data to process.")
    exit()

# Group directly by timestamp && event type
# Bin timestamps into intervals (e.g., 1-second bins)
df["timestamp_binned"] = pd.cut(df["timestamp"], bins=100)  # Adjust bins as needed
grouped = df.groupby(["timestamp_binned", "event_type"]).size().unstack(fill_value=0)

# Debugging: Check grouped DataFrame size
print("Grouped DataFrame shape:", grouped.shape)

# Plot aggregated data
fig, ax = plt.subplots(figsize=(12, 6))
grouped.plot(kind="line", ax=ax, title="I/O Burstiness by Event Type")
plt.xlabel("Binned Timestamp Intervals")
plt.ylabel("Number of Events")
plt.legend(title="Event Type")
plt.grid(True)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
