# README for `script.py`

## Overview

`script.py` is a Python script designed to process a log file containing blkparse output (I/O event data) and calculate the completion times for each I/O operation. The script reads the input file, extracts relevant information, and writes the results to an output CSV file. The output includes details such as the operation number, opcode, tag, logical block address (LBA), transfer length, completion time, and response time.

## Features

- Reads an input file containing I/O event data.
- Parses the data to extract relevant fields.
- Calculates the completion time for each I/O operation.
- Outputs the results to a specified CSV file.
- Handles errors gracefully, providing feedback on malformed lines.

## Requirements

- Python 3.x
- Standard libraries: `sys`, `csv`

## Input Format

The input file should contain lines of text where each line represents an I/O event. The expected format is as follows:

```
<target> <time> <type> <opcode> <pid> <lba> <xfr_len> ...
```

### Field Descriptions

- **target**: The target device for the I/O operation.
- **time**: The timestamp of the event (in seconds).
- **type**: The type of event (e.g., "D" for dispatch, "C" for completion).
- **opcode**: The operation code indicating the type of operation (e.g., read or write).
- **pid**: The process ID associated with the I/O operation.
- **lba**: The logical block address where the data is located.
- **xfr_len**: The length of the data transfer (in bytes).

## Output Format

The output CSV file will contain the following columns:

- **number**: A sequential identifier for each I/O operation.
- **opcode**: The operation code (hexadecimal) for the I/O operation.
- **tag**: A unique identifier for the I/O operation, formatted as `<original_opcode>_<lba>_<xfr_len>`.
- **lba**: The logical block address (hexadecimal) for the I/O operation.
- **xfrlen**: The transfer length (hexadecimal) for the I/O operation.
- **Completion time**: The time taken to complete the I/O operation (in microseconds).
- **response**: The response time for the I/O operation (in microseconds).

## Usage

To run the script, use the following command in the terminal:

```bash
python3 script.py <input_file> <output_csv>
```

### Parameters

- `<input_file>`: The path to the input file containing the I/O event data.
- `<output_csv>`: The path where the output CSV file will be saved.

### Example

```bash
python3 script.py input.txt output.csv
```

## Error Handling

The script includes error handling for the following scenarios:

- **File Not Found**: If the input file cannot be opened, an error message will be printed, and the script will exit.
- **Malformed Lines**: If a line in the input file does not contain the expected number of fields, it will be skipped, and a warning will be printed to the standard error.

## Code Structure

### Classes

- **EventEntry**: A class representing an I/O event entry. It contains the following attributes:
  - `event_type`: The type of event (e.g., "D" or "C").
  - `timestamp`: The timestamp of the event.
  - `duration`: The duration of the event.
  - `opcode`: The operation code for the event.
  - `lba`: The logical block address for the event.
  - `xfr_len`: The transfer length for the event.
  - `pid`: The process ID associated with the event.

### Functions

- **calculate_completion_times(file_name, output_csv)**: The main function that processes the input file and writes the output CSV. It performs the following tasks:
  - Reads the input file and stores the lines.
  - Parses each line to extract relevant fields.
  - Calculates the completion time for each I/O operation.
  - Writes the results to the output CSV file.

## Conclusion

This script is useful for analyzing I/O operations in storage systems, allowing users to track performance metrics and understand the behavior of I/O requests. By processing the input data and generating a structured output, users can gain insights into the efficiency and effectiveness of their storage systems.
