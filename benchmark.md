# Running the MLPerf Storage Benchmark with ResNet50 Workload

Here are instructions for setting up and running the MLPerf Storage Benchmark using the ResNet50 workload in a Docker environment.

---

## Prerequisites
1. **Update YAML Configuration**: 
   Update the number of threads in your workload's YAML file. For ResNet50 with H100 accelerators, you can find the configuration file [here](https://github.com/mlcommons/storage/blob/main/storage-conf/workload/resnet50_h100.yaml). Adjusting the thread count ensures optimal utilization of system resources.

2. **Supported Models**:
   The MLPerf Storage benchmark supports the following models:
   - **ResNet50** (Image Classification): Uses TensorFlow I/O Library (~150 KB/sample).
   - **3D-UNet** (Medical Image Segmentation): Uses PyTorch I/O Library (~140 MB/sample).
   - **CosmoFlow** (Cosmology Parameter Prediction): Uses TensorFlow I/O Library (~2 MB/sample).

   Each model has its own YAML configuration file available in the [MLPerf Storage GitHub repository](https://github.com/mlcommons/storage). To switch between models, replace references to `resnet50_h100.yaml` with the appropriate YAML file for your model. Ensure that dataset parameters such as `dataset.num_files_train` and `dataset.data_folder` match the requirements of your chosen model.

3. **System Requirements**:
   - Minimum disk space: 50GB.
   - Ensure Docker is installed and running on your system.
   - Verify that you have at least one node available (Node 2 is optional for distributed workloads).

---

## Step 1: Build Docker Images

Build two Docker images for the nodes that will run the benchmark:

```
docker build -t mlperf-node1 -f Dockerfile-node1 .
docker build -t mlperf-node2 -f Dockerfile-node2 . # OPTIONAL
```

- **Parameter Explanation**:
  - `-t mlperf-node1` and `-t mlperf-node2`: Tags assigned to the Docker images for easier identification.
  - `-f Dockerfile-node1` and `-f Dockerfile-node2`: Specify the respective Dockerfiles for each node.

---

## Step 2: Create a Docker Network

Create a custom network for communication between the nodes:

```
docker network create mlperf-network
```

- **Importance**:
  A custom network allows containers to communicate with each other by name, which is essential for distributed workloads like MLPerf.

---

## Step 3: Start Docker Containers

Run the containers for both nodes (Node 2 is optional):

```
docker run -d --name mlperf-node1 --network mlperf-network --cap-add=NET_ADMIN mlperf-node1
docker run -d --name mlperf-node2 --network mlperf-network mlperf-node2 # OPTIONAL
```

- **Parameter Explanation**:
  - `--name`: Assigns a name to each container for easier reference.
  - `--network`: Connects the containers to the custom network created earlier.
  - `--cap-add=NET_ADMIN`: Grants additional network administration capabilities to Node 1 (required for some configurations).

---

## Step 4: Verify Node Communication

Enter Node 1 interactively and test communication with Node 2 (if using multiple nodes):

```
docker exec -it mlperf-node1 bash
ssh root@mlperf-node2 # OPTIONAL
```

- **Importance**:
  This step ensures that both nodes are correctly connected via the custom network. You may need to confirm SSH connectivity by accepting the host key fingerprint.

---

## Step 5: Estimate Dataset Size

Before generating data, estimate the dataset size required for your configuration:

```
./benchmark.sh datasize --workload resnet50 --accelerator-type h100 --num-accelerators 1 --num-client-hosts 2 --client-host-memory-in-gb 5
```

- **Parameter Explanation**:
  - `--workload resnet50`: Specifies the ResNet50 workload. 
    - Replace `--workload resnet50` with your desired model (`unet3d`, `cosmoflow`, etc.).
  - `--accelerator-type h100`: Indicates that H100 accelerators will be used.
  - `--num-accelerators`: Number of accelerators per host.
  - `--num-client-hosts`: Number of client hosts participating in the benchmark.
    - --num-client-hosts 1 for using only a single node
  - `--client-host-memory-in-gb`: Memory allocated per client host.

The output will include an estimate of files required and storage space needed (e.g., "159 files consuming ~21GB").

---

## Step 6: Generate Dataset

Generate the dataset based on the estimated size:

```
./benchmark.sh datagen --hosts mlperf-node1,mlperf-node2 --workload resnet50 \
--accelerator-type h100 --num-parallel 1 \
--param dataset.num_files_train=400 \
--param dataset.data_folder=resnet50_data
```

- **Parameter Explanation**:
  - `--hosts`: Lists all (1, 2, ...) participating hosts (e.g., Node1 and Node2).
  - `--num-parallel`: Number of parallel threads for data generation.
  - `--param dataset.num_files_train=400`: Specifies the number of training files to generate.
  - `--param dataset.data_folder=resnet50_data`: Directory where generated data will be stored.

---

## Step 7: Run Benchmark

Run the benchmark using the generated dataset:

```
./benchmark.sh run --hosts mlperf-node1,mlperf-node2 --workload resnet50 \
--accelerator-type h100 --num-accelerators 1 \
--results-dir resnet50_h100_results \
--param dataset.num_files_train=400 \
--param dataset.data_folder=resnet50_data
```

- **Parameter Explanation**:
  - `--results-dir`: Directory where benchmark results will be saved.
  - If using only one node, modify `--hosts` as ` ./benchmark.sh run --hosts mlperf-node1 ...`
  - Other parameters are consistent with those used during data generation.

The benchmark will run for approximately **nine minutes** under optimal conditions.

---

## Step 8: Monitor I/O Activity (Optional)

While the benchmark is running, monitor I/O activity using `iotop` or `blktrace`:

```
iotop -b -o -q -d 1 | ts '%Y-%m-%dT%H:%M:%S' > log4.txt
```
OR
```
Refer to blktrace.md for other method for I/O activity.
```

- **Importance**:
  This helps profile I/O performance during benchmarking. The output is saved in a timestamped log file (`log4.txt`, `parsed_output_hdd.txt`).

---

## Step 9: Clean Up Training and Result Files (Optional but Recommended)

After running the benchmark, delete training and result files to free up storage space, especially if you plan to rerun benchmarks or generate new datasets.

### Steps to Clean Up Files:

1. **Navigate to Dataset and Results Directory in interactive node**:
   ```
   cd /root/mlperf-storage
   ```

2. **Delete Training Files**:
   ```
   rm -rf resnet50_data
   ```

3. **Delete Result Files**:
   ```
   rm -rf resnet50_h100_results
   ```

4. **Clear Temporary Files (if any)**:
   ```
   rm -rf *.log *.tmp
   ```

5. **Verify Free Space**:
   Check available storage space after cleanup:
   ```
   df -h
   ```

- **Why Clean Up?**
    - Prevent storage bottlenecks due to large datasets and results.
    - Ensure compliance with MLPerf guidelines by avoiding reuse of cached data between runs.

---

## Notes and Tips

- **Adjust Thread Count**:
   Modify thread count in the YAML configuration file (`resnet50_h100.yaml`) to optimize performance based on your system's capabilities.

- **Clear Cache Before Running Benchmarks**:
   Use these commands to flush filesystem buffers and clear caches:
   ```
   sudo sync
   sudo sysctl -w vm.drop_caches=3
   ```

- **Cleanup Old Data**:
   Remove old datasets or results before generating new ones:
   ```
   sudo rm trace_output*.blktrace.*
   ```

For more details, refer to [MLPerf Storage GitHub Repository](https://github.com/mlcommons/storage).

---
