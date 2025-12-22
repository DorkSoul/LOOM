# LOOM Quick Start Guide

## For NAS Deployment (Production)

### Step 1: Prepare Your NAS

Create the directory structure on your NAS:

```bash
mkdir -p /volume2/Dockerssd/loom/data
mkdir -p /volume2/Dockerssd/loom/logs
```

### Step 2: Create docker-compose.yml

Create a file at `/volume2/Dockerssd/loom/docker-compose.yml`:

```yaml
version: '3.8'

services:
  loom:
    image: ghcr.io/yourusername/loom:latest
    container_name: loom
    restart: unless-stopped
    ports:
      - "5001:5000"
    volumes:
      - /volume2/Dockerssd/loom/data:/app/data:rw
      - /volume2/Dockerssd/loom/logs:/app/logs:rw
    environment:
      - FLASK_ENV=production
      - DATABASE_PATH=/app/data/loom.db
      - SECRET_KEY=change-this-to-a-random-secret-key
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Step 3: Start the Application

```bash
cd /volume2/Dockerssd/loom
docker-compose pull
docker-compose up -d
```

### Step 4: Access LOOM

Open your browser and go to:
```
http://<your-nas-ip>:5001
```

Example: `http://192.168.1.100:5001`

---

## For Local Development

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/loom.git
cd loom
```

### Step 2: Set Up Python Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
python run.py
```

### Step 4: Access LOOM

Open your browser and go to:
```
http://localhost:5000
```

---

## Building and Pushing Updates

### Step 1: Make Your Changes

Edit the code as needed.

### Step 2: Test Locally

```bash
python run.py
```

### Step 3: Build Docker Image

```bash
docker build -t ghcr.io/yourusername/loom:latest .
```

### Step 4: Push to GitHub Container Registry

```bash
# Login to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u yourusername --password-stdin

# Push the image
docker push ghcr.io/yourusername/loom:latest
```

### Step 5: Update on NAS

```bash
cd /volume2/Dockerssd/loom
docker-compose pull
docker-compose up -d
```

---

## Using GitHub Actions (Automated)

The repository includes a GitHub Actions workflow that automatically builds and pushes the Docker image when you push to the main branch.

### Step 1: Push Your Changes

```bash
git add .
git commit -m "Your commit message"
git push origin main
```

### Step 2: Wait for Build

GitHub Actions will automatically:
1. Build the Docker image
2. Push it to GitHub Container Registry
3. Tag it as `latest`

### Step 3: Update on NAS

```bash
cd /volume2/Dockerssd/loom
docker-compose pull
docker-compose up -d
```

---

## Common Commands

### View Logs

```bash
docker-compose logs -f loom
```

### Restart Application

```bash
docker-compose restart
```

### Stop Application

```bash
docker-compose down
```

### Backup Database

```bash
cp /volume2/Dockerssd/loom/data/loom.db /volume2/Dockerssd/loom/backups/loom-$(date +%Y%m%d).db
```

---

## Troubleshooting

### Check if Container is Running

```bash
docker ps | grep loom
```

### View Container Logs

```bash
docker logs loom
```

### Check Health Status

```bash
curl http://localhost:5001/health
```

### Restart from Scratch

```bash
docker-compose down
docker-compose pull
docker-compose up -d
```

---

**You're all set!** Start organizing your life with LOOM.
