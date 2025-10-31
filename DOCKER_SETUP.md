# 🐳 Docker Setup for StaffView

## Installing Docker on macOS

### Option 1: Docker Desktop (Recommended - GUI)

1. **Download Docker Desktop:**
   - Visit: https://www.docker.com/products/docker-desktop
   - Click "Download for Mac"
   - Choose the version for your chip:
     - **Apple Silicon (M1/M2/M3)** - ARM64
     - **Intel** - AMD64

2. **Install:**
   - Open the downloaded `.dmg` file
   - Drag Docker to Applications
   - Open Docker from Applications
   - Follow setup wizard

3. **Verify Installation:**
   ```bash
   docker --version
   docker-compose --version
   ```

### Option 2: Homebrew (Command Line)

```bash
# Install Docker
brew install --cask docker

# Start Docker Desktop
open -a Docker

# Wait for Docker to start (look for whale icon in menu bar)

# Verify
docker --version
docker-compose --version
```

---

## Quick Deploy Once Docker is Ready

After Docker is installed and running:

```bash
cd "/Users/yeltsinz/UniqueProjects/Gandalf regression reports"

# Build and start StaffView
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f staffview

# Open in browser
open http://localhost:5001
```

---

## Docker Commands Reference

### Starting/Stopping
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart services
docker-compose restart
```

### Monitoring
```bash
# View logs (all)
docker-compose logs

# Follow logs (real-time)
docker-compose logs -f

# View last 100 lines
docker-compose logs --tail=100

# Check container status
docker-compose ps

# Check resource usage
docker stats staffview
```

### Maintenance
```bash
# Rebuild image (after code changes)
docker-compose build

# Rebuild and restart
docker-compose up -d --build

# Remove everything (clean start)
docker-compose down -v

# Remove old images
docker image prune -a
```

---

## Troubleshooting

### Docker Desktop not starting
- Check if you have enough RAM (minimum 4GB)
- Restart your Mac
- Check macOS version (requires macOS 10.15+)

### Port 5001 already in use
```bash
# Find process using port
lsof -i :5001

# Kill the process
kill -9 <PID>

# Or change port in docker-compose.yml
ports:
  - "5002:5001"  # Changed to 5002
```

### Container keeps restarting
```bash
# Check logs for errors
docker-compose logs staffview

# Common issues:
# - Port conflict
# - Permission issues with volumes
# - Missing dependencies
```

---

## Ready to Deploy!

Once Docker Desktop is running (you'll see a whale icon in your menu bar):

1. Navigate to project:
   ```bash
   cd "/Users/yeltsinz/UniqueProjects/Gandalf regression reports"
   ```

2. Deploy:
   ```bash
   docker-compose up -d
   ```

3. Access:
   ```
   http://localhost:5001
   ```

That's it! StaffView will be running in a container! 🎉

