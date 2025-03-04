
# Moving Docker Data Between SSD and HDD

Here are some instructions on how to determine Docker's current storage location and move its data directory between an SSD and HDD. These steps can help ensure proper migration while maintaining Docker's functionality.

---

## 1. Determine Docker's Storage Location

### Check Docker's Root Directory
By default, Docker stores its data in `/var/lib/docker`. To verify this location, run:
```
docker info | grep "Docker Root Dir"
```

### Verify the Mount Point
To confirm which device is being used for the storage directory, use:
```
df -h /var/lib/docker
```
The output will indicate the filesystem and mount point (e.g., `/dev/sda3`: SSD).

---

## 2. Move Docker Data from SSD to HDD

To relocate Docker's data directory from an SSD to an HDD, follow these steps:

### Step 1: Stop Docker Service
Stop the Docker service to safely move the data:
```
sudo systemctl stop docker
```

### Step 2: Move Data to HDD
Move the current data directory from the SSD (`/var/lib/docker`) to a new location on the HDD (e.g., `/home/docker-data`):
```
sudo mv /var/lib/docker /home/docker-data
```

### Step 3: Create a Symlink
Create a symbolic link so Docker can continue accessing its data at the default path:
```
sudo ln -s /home/docker-data /var/lib/docker
```

### Step 4: Restart Docker Service
Restart the Docker service to apply changes:
```
sudo systemctl start docker
```

---

## 3. Move Docker Data from HDD Back to SSD

To revert Docker's data back to its original location on the SSD, follow these steps:

### Step 1: Check for Existing Symlink
Verify if `/var/lib/docker` is currently a symlink:
```
ls -l /var/lib/docker
```
If it points to another location (e.g., `/home/docker-data`), you'll see an arrow in the output.

### Step 2: Remove Symlink
Remove the existing symlink:
```
sudo rm /var/lib/docker
```

### Step 3: Move Data Back to SSD
Move the data from the HDD back to its original location on the SSD:
```
sudo mv /home/docker-data /var/lib/docker/
```

### Step 4: Restart Docker Service
Restart the Docker service to apply changes:
```
sudo systemctl start docker
```

---

## Additional Notes

- **Use `rsync` for Safer Transfers**: Instead of `mv`, you can use `rsync` for a safer transfer with progress tracking:
  ```
  sudo rsync -aP /var/lib/docker /home/docker-data
  ```

- **Clean Up Unused Data**: Before moving data, clean up unused images, containers, and volumes to save space:
  ```
  docker system prune -a
  ```

  Restart Docker after making this change:
  ```
  sudo systemctl restart docker
  ```

---
