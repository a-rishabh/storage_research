# **README for Using `blktrace` on SSD and HDD for Benchmarking**

## Overview
Here are instructions for using the `blktrace` utility to monitor and analyze the block-level I/O behavior of SSDs and HDDs during benchmarking. By using `blktrace`, we can capture and parse block I/O traces to gain insight into storage performance, latency, and other relevant metrics.

### Prerequisites
- **Linux OS** (preferably Ubuntu or similar)
- **`blktrace`** and **`blkparse`** tools installed
- A benchmarking tool (such as `MLPerf`) that we're using to test your storage device performance
- **SSH** access if you're working with remote machines for file transfer (`scp` command)

---

## Steps for Running `blktrace` on SSD and HDD

### 1. **Identify the Correct Storage Device**
Before running `blktrace`, you need to identify the correct disk or partition for monitoring. In Linux, storage devices are typically named `/dev/sdX` (for traditional SATA SSDs and HDDs), where `X` is a letter (e.g., `a`, `b`, `c`). Each device may have partitions like `/dev/sda1`, `/dev/sda2`, etc.

#### Difference Between `sda`, `sda1`, `sda2`, etc.:
- **`/dev/sda`**: The **entire first disk** (either SSD or HDD).
- **`/dev/sda1`, `sda2`, `sda3`, etc.**: Individual **partitions** on the disk. You will typically trace the entire disk (`/dev/sda`), not just a partition.

#### How to List All Storage Devices:
To list all connected storage devices, both SSDs and HDDs, and their partitions, use the following commands:

```bash
lsblk -o NAME,SIZE,TYPE,ROTA
```

- **ROTA = 0**: Non-rotational (SSD)
- **ROTA = 1**: Rotational (HDD)

Alternatively, for a more detailed view, use:

```bash
lsblk -f
```

This shows additional information like the filesystem type (e.g., `ext4`, `ntfs`).

To list the entire disk (without partitions):

```bash
lsblk -d -o NAME,SIZE,ROTA
```

You can also use `smartctl` to check whether a disk is an SSD or HDD:

```bash
sudo smartctl -i /dev/sda
```

This command will output details about the disk, including whether it’s an SSD or HDD.

---

### 2. **Start Benchmarking Your Storage Device**
Run your chosen benchmarking tool (e.g., `MLPerf`, or others) to generate I/O load on the target storage device. This load will be used for tracing.

Example for starting a benchmark using `MLPerf`:
```bash
./benchmark.sh run --hosts mlperf-node1 --workload resnet50 --accelerator-type h100 --num-accelerators 1 --results-dir resnet50_h100_results --param dataset.num_files_train=187 --param dataset.data_folder=resnet50
```
*Replace this with your own benchmark command based on your setup.*

---

### 3. **Run `blktrace` to Trace Block I/O**
Once your benchmark is running, start `blktrace` to capture the block-level I/O activities for the target storage device (SSD or HDD).

#### For HDD (e.g., `/dev/sdb`):
```bash
sudo blktrace -d /dev/sdb -o trace_output_hdd
```

#### For SSD (e.g., `/dev/sda`):
```bash
sudo blktrace -d /dev/sda -o trace_output_ssd
```

- **`-d /dev/sda`**: Specifies the storage device you want to trace (SSD or HDD).
- **`-o trace_output_ssd`**: The `-o` option defines the output file prefix where the trace data will be saved. This will generate files with the prefix `trace_output_ssd.blktrace.*`.

> **Important:** You should start the trace as soon as the benchmark begins to ensure you capture the full I/O activity during the test.

---

### 4. **Stop the Trace After Benchmark Completes**
Once your benchmark finishes running (after a specified duration or when you manually stop it), stop the `blktrace` command by pressing `CTRL + C` in your terminal.

> **Note:** Be cautious not to interrupt the benchmark too early, as you need sufficient data for analysis.

---

### 5. **Parse the Trace Data**
After stopping `blktrace`, use `blkparse` to generate a human-readable report from the trace output. This step is essential for analyzing the raw trace data captured during the benchmark.

```bash
sudo blkparse trace_output_ssd.blktrace.* -o parsed_output_ssd.txt
```

- **`trace_output_ssd.blktrace.*`**: The input file pattern, which matches all the trace files created by `blktrace`.
- **`-o parsed_output_ssd.txt`**: Specifies the output file where the parsed data will be saved.

---

### 6. **Transfer the Parsed Report to Your Local Machine**
For easier access and analysis, transfer the parsed output file to your local machine using `scp` (Secure Copy Protocol). This allows you to process the data using Python or other analysis tools.

```bash
scp -r cs-geeta@cs-u-geeta.cs.umn.edu:/home/cs-geeta/agarw266/Benchmarking/parsed_output_ssd.txt .
```

- Replace `cs-geeta@cs-u-geeta.cs.umn.edu:/home/cs-geeta/agarw266/Benchmarking` with the actual path where your parsed file is stored on the remote machine.

---

### 7. **Analyze the Data (Histograms and Performance Metrics)**
Once you have the parsed output on your local machine, you can use Python or other tools to analyze the trace data. A common analysis is to create histograms showing I/O patterns, latency distributions, and throughput during the benchmark.

Example Python code for generating histograms:
```python
import matplotlib.pyplot as plt

# Read the parsed output file
with open('parsed_output_ssd.txt', 'r') as f:
    data = f.readlines()

# Extract latency and I/O data from parsed output (depends on format)
latencies = [float(line.split()[3]) for line in data if 'latency' in line]  # Adjust based on actual data format

# Plot a histogram of latencies
plt.hist(latencies, bins=50, edgecolor='black')
plt.title('I/O Latency Distribution (SSD)')
plt.xlabel('Latency (ms)')
plt.ylabel('Frequency')
plt.show()
```

> You may need to modify the script to match the format of your parsed data, but the general idea is to extract the relevant metrics (e.g., latencies, throughput) and visualize them.

---

## Housekeeping and Cleanup

### 1. **Flush Filesystem Buffers**
To ensure that all I/O operations are flushed to the disk, run the following command before starting or after finishing the benchmark:
```bash
sudo sync
```

### 2. **Clear Cache to Ensure Clean Results**
It’s important to clear the filesystem cache to prevent caching effects from distorting the results. This step is essential for performance consistency between runs.

```bash
sudo sysctl -w vm.drop_caches=3
```

- **`vm.drop_caches=3`**: Clears page cache, dentries, and inodes, ensuring that no cached data from previous tests interferes with your results.

### 3. **Delete Old Trace Files**
After each benchmark session, it’s a good practice to delete old trace files to avoid clutter and ensure you're working with fresh data.

```bash
sudo rm trace_output*.blktrace.*
```

### 4. **Confirm Cache Clearance**
You can confirm that the cache has been cleared by checking the available system memory and cache:

```bash
free -h
```

This will give you a quick summary of memory usage, including whether the caches were successfully cleared.

---

## Troubleshooting Tips

1. **Permission Issues:**
   - If you encounter permission errors when running `blktrace`, ensure that you're using `sudo` since tracing block devices requires elevated privileges.

2. **Missing `blktrace` or `blkparse`:**
   - Install the tools if they're not available on your system:
     ```bash
     sudo apt-get install blktrace
     ```

3. **Incomplete Trace Data:**
   - If you stop the `blktrace` command too early, you may miss key data. Always ensure the benchmark completes before halting the trace.

4. **System Performance:**
   - Tracing and benchmarking can put a heavy load on your system. Monitor system resources (CPU, memory, disk I/O) to ensure that neither `blktrace` nor the benchmark tool itself affects the results.

---

## Conclusion

By following the steps outlined in this README, you will be able to effectively trace, parse, and analyze block I/O data for both SSDs and HDDs during storage benchmarking. Understanding the I/O patterns and performance characteristics of your storage devices can provide valuable insights into their capabilities and help identify potential bottlenecks.