# Docker Reinstallation Guide

## Step 1: Remove Docker Completely

The following commands will remove Docker packages, files, and directories:

```bash
# Remove Docker packages
sudo apt-get purge -y docker-engine docker docker.io docker-ce docker-ce-cli

# Remove Docker files and directories
sudo rm -rf /var/lib/docker
sudo rm -rf /etc/docker
sudo rm -rf /var/run/docker.sock

# Optional: remove Docker group if it exists
sudo groupdel docker 2>/dev/null

# Clean up unused packages
sudo apt-get autoremove -y
sudo apt-get autoclean
```

## Step 2: Reinstall DockerFollow these steps to reinstall Docker:

✅ Update and install dependencies:
```bash
sudo apt-get update

sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

## 🔐 Add Docker's official GPG key:

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL [https://download.docker.com/linux/ubuntu/gpg](https://download.docker.com/linux/ubuntu/gpg) | \
sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```


## 📦 Set up the Docker repository:
```bash
echo \
  "deb [arch=$(dpkg --print-architecture) \
  signed-by=/etc/apt/keyrings/docker.gpg] \
  [https://download.docker.com/linux/ubuntu](https://download.docker.com/linux/ubuntu) \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```


## 🔄 Install Docker Engine:

```bash
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```


## ▶️ Start Docker
```bash
sudo systemctl start docker
sudo systemctl enable docker
```


## ✅ Step 3: Verify Installation
Verify that Docker has been installed correctly by checking the version and running a test container:

```bash
sudo docker --version
sudo docker run hello-world
```


## ✅ Step 4: Try Restarting Docker Manually
After cleaning or checking configurations, try to restart Docker manually with:

```bash
sudo systemctl daemon-reload
sudo systemctl restart docker
```
```bash
sudo systemctl status docker
```

## ✅ Add your user to the Docker group:
```bash
sudo usermod -aG docker $USER
```
## 🔁 Log out and log back in
Or just reboot your machine to apply the group change:

```bash
reboot
```
## 🧪 Verify:
After logging in again, run:
```bash
groups
```
You should now see docker in the list.

## 🚀 Try your command again ( ):
```bash
sudo docker build -t langgraph-b-ai-agent-app .
```

# 🔥 The Issue:
The container is trying to run Uvicorn multiple times, but port 8000 is already in use, either:


## ✅ How to Fix It
Option 1: 🧹 Clean Restart (Recommended)
Stop the existing container:
```bash
docker stop langgraph-b-ai-agent-container
```

Remove the container (it won’t delete the image):
```bash
docker rm langgraph-b-ai-agent-container
```
Run it again, but this time only bind the necessary service ports, e.g., if FastAPI is at 8000 and Streamlit at 8501:

```bash
docker run -d -p 8000:8000 -p 8501:8501 --name 
langgraph-b-ai-agent-container langgraph-b-ai-agent-app
```
