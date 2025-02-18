# README for `storage.ipynb`

## Overview

`storage.ipynb` is a Jupyter Notebook designed for visualizing and analyzing I/O performance data from Solid State Drives (SSD) and Hard Disk Drives (HDD). The notebook loads CSV files containing performance metrics, processes the data, and generates various visualizations to compare the performance characteristics of SSDs and HDDs.

## Features

- Loads and processes CSV files containing I/O performance data.
- Converts hexadecimal values to integers for analysis.
- Normalizes response and completion times for better readability.
- Generates visualizations to compare response time distributions, LBA distributions, and access patterns over time.
- Utilizes libraries such as Pandas, Matplotlib, and Seaborn for data manipulation and visualization.

## Requirements

To run this notebook, you need the following Python libraries:

- `pandas`
- `matplotlib`
- `seaborn`
- `numpy`

You can install these libraries using pip:

```bash
pip install pandas matplotlib seaborn numpy
```

## Input Data

The notebook expects two CSV files as input:

1. **`ssd.csv`**: Contains performance metrics for SSDs.
2. **`hdd.csv`**: Contains performance metrics for HDDs.

### Expected CSV Format

Each CSV file should contain the following columns:

- **number**: A sequential identifier for each I/O operation.
- **opcode**: The operation code (hexadecimal) for the I/O operation.
- **tag**: A unique identifier for the I/O operation.
- **lba**: The logical block address (hexadecimal) for the I/O operation.
- **xfrlen**: The transfer length (hexadecimal) for the I/O operation.
- **Completion time**: The time taken to complete the I/O operation (in microseconds).
- **response**: The response time for the I/O operation (in microseconds).

## Usage

To use the notebook, follow these steps:

1. Open the notebook in Jupyter Notebook or Google Colab.
2. Ensure that the `ssd.csv` and `hdd.csv` files are in the same directory as the notebook or provide the correct path to the files.
3. Run each cell sequentially to load the data, process it, and generate visualizations.

### Example Workflow

1. Load the necessary libraries.
2. Load the CSV files:
   ```python
   ssd_data = pd.read_csv('ssd.csv')
   hdd_data = pd.read_csv('hdd.csv')
   ```
3. Convert hexadecimal transfer lengths to integers:
   ```python
   ssd_data['xfrlen'] = ssd_data['xfrlen'].apply(lambda x: int(x, 16))
   hdd_data['xfrlen'] = hdd_data['xfrlen'].apply(lambda x: int(x, 16))
   ```
4. Normalize response and completion times to milliseconds:
   ```python
   ssd_data['response_ms'] = ssd_data['response'] / 1000
   hdd_data['response_ms'] = hdd_data['response'] / 1000
   ```
5. Generate visualizations to compare SSD and HDD performance.

## Visualizations

The notebook generates several key visualizations:

1. **Response Time Distribution**:
   - A histogram comparing the response time distributions of SSDs and HDDs.
   - Uses a logarithmic scale for better visibility of data distribution.

   ```python
   sns.histplot(ssd_data["response_ms"], bins=100, color="blue", label="SSD", kde=True, log_scale=True)
   sns.histplot(hdd_data["response_ms"], bins=100, color="red", label="HDD", kde=True, log_scale=True)
   ```

2. **LBA Distribution**:
   - A histogram comparing the LBA distributions of SSDs and HDDs.
   - Also uses a logarithmic scale for the LBA values.

   ```python
   sns.histplot(ssd_data["lba"], bins=100, color="blue", label="SSD", kde=True, alpha=0.6, log_scale=(True, False))
   sns.histplot(hdd_data["lba"], bins=100, color="red", label="HDD", kde=True, alpha=0.6, log_scale=(True, False))
   ```

3. **LBA Access Pattern Over Time**:
   - A scatter plot showing the relationship between completion time and LBA for both SSDs and HDDs.

   ```python
   plt.scatter(ssd_data["Completion time"], ssd_data["lba"], color="blue", s=1, label="SSD")
   plt.scatter(hdd_data["Completion time"], hdd_data["lba"], color="red", s=1, label="HDD")
   ```

## Conclusion

The `storage.ipynb` notebook provides a comprehensive analysis of I/O performance data for SSDs and HDDs. By visualizing the data, users can gain insights into the performance characteristics of different storage technologies, helping to inform decisions regarding storage solutions and optimizations.
