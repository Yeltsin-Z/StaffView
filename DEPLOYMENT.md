# ⚡ StaffView Deployment Guide

**Gandalf's tool for regression clarity - Now in Production!**

This guide covers multiple deployment options for StaffView.

---

## 🚀 Quick Start - Production Server

### Option 1: Using Gunicorn (Recommended)

**Install Gunicorn:**
```bash
pip install gunicorn
```

**Run in production:**
```bash
gunicorn --config gunicorn_config.py app:app
```

The app will be available at `http://your-server-ip:5001`

---

## 🐳 Docker Deployment

### Build and Run with Docker

**Build the image:**
```bash
docker build -t staffview:latest .
```

**Run the container:**
```bash
docker run -d \
  --name staffview \
  -p 5001:5001 \
  -v $(pwd)/artifacts:/app/artifacts:ro \
  -v $(pwd)/uploads:/app/uploads \
  staffview:latest
```

### Using Docker Compose (Easier)

**Start the service:**
```bash
docker-compose up -d
```

**Stop the service:**
```bash
docker-compose down
```

**View logs:**
```bash
docker-compose logs -f
```

---

## ☁️ Cloud Platform Deployments

### 1. AWS EC2

**Setup:**
```bash
# SSH into your EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv nginx

# Clone/upload your project
cd /opt
sudo git clone <your-repo>
cd staffview

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run with Gunicorn
gunicorn --config gunicorn_config.py app:app
```

**Setup as systemd service:**
Create `/etc/systemd/system/staffview.service`:
```ini
[Unit]
Description=StaffView - Regression Comparison Tool
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/opt/staffview
Environment="PATH=/opt/staffview/venv/bin"
ExecStart=/opt/staffview/venv/bin/gunicorn --config gunicorn_config.py app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable staffview
sudo systemctl start staffview
sudo systemctl status staffview
```

### 2. Heroku

**Create Procfile:**
```bash
echo "web: gunicorn --config gunicorn_config.py app:app" > Procfile
```

**Deploy:**
```bash
heroku create your-staffview-app
git push heroku main
heroku open
```

### 3. Google Cloud Run

**Build and deploy:**
```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/staffview
gcloud run deploy staffview --image gcr.io/PROJECT-ID/staffview --platform managed
```

### 4. DigitalOcean App Platform

1. Connect your GitHub repository
2. DigitalOcean will auto-detect the Dockerfile
3. Click "Deploy"

### 5. Railway.app

1. Connect GitHub repository
2. Railway auto-detects Python app
3. Automatically deploys

---

## 🔒 Production Configuration

### Environment Variables

Create `.env` file:
```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
ARTIFACTS_DIR=/path/to/artifacts
MAX_UPLOAD_SIZE=104857600  # 100MB
```

Update `app.py` to use environment variables:
```python
import os
from dotenv import load_dotenv

load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-me-in-production')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_UPLOAD_SIZE', 104857600))
```

### Nginx Reverse Proxy

**Create `/etc/nginx/sites-available/staffview`:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Upload size limit
        client_max_body_size 100M;
    }
}
```

**Enable and restart:**
```bash
sudo ln -s /etc/nginx/sites-available/staffview /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 🔐 Security Checklist

Before going live:

- [ ] Change default SECRET_KEY
- [ ] Enable HTTPS/SSL
- [ ] Set up firewall rules
- [ ] Configure upload size limits
- [ ] Add authentication (if needed)
- [ ] Set up backup for uploads
- [ ] Configure logging
- [ ] Monitor disk space (uploads folder)
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Rate limiting for uploads

---

## 📊 Monitoring

### Check Application Health

```bash
# Docker
docker ps
docker logs staffview

# Systemd
sudo systemctl status staffview
sudo journalctl -u staffview -f

# Logs
tail -f uploads/server.log
```

### Resource Monitoring

```bash
# CPU and Memory
htop

# Disk space
df -h
du -sh uploads/

# Network
netstat -tlnp | grep 5001
```

---

## 🔄 Updates and Maintenance

### Update Application

**Docker:**
```bash
docker-compose down
docker-compose pull
docker-compose up -d
```

**Systemd:**
```bash
cd /opt/staffview
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart staffview
```

### Backup Strategy

**Backup uploads:**
```bash
tar -czf staffview-uploads-$(date +%Y%m%d).tar.gz uploads/
```

**Restore uploads:**
```bash
tar -xzf staffview-uploads-YYYYMMDD.tar.gz
```

---

## 🌐 Custom Domain Setup

1. **Point DNS A record** to your server IP
2. **Update Nginx config** with your domain
3. **Get SSL certificate** with certbot
4. **Update ALLOWED_HOSTS** in app.py (if implemented)

---

## 📈 Scaling

### Horizontal Scaling

Use a load balancer with multiple instances:

**docker-compose.yml:**
```yaml
services:
  staffview:
    build: .
    deploy:
      replicas: 3
    ports:
      - "5001-5003:5001"
```

### Vertical Scaling

Adjust Gunicorn workers:
```python
# gunicorn_config.py
workers = 8  # Increase based on CPU cores
```

---

## 🐛 Troubleshooting

### Application won't start
```bash
# Check logs
docker logs staffview
# or
sudo journalctl -u staffview -n 50
```

### Upload fails
- Check disk space: `df -h`
- Check permissions: `ls -la uploads/`
- Check upload size limit in Nginx

### Port already in use
```bash
# Find process
sudo lsof -i :5001
# Kill process
sudo kill -9 <PID>
```

---

## 📞 Support

For deployment issues:
1. Check logs first
2. Review this guide
3. Check GitHub issues
4. Contact your DevOps team

---

## 🎉 You're Live!

Once deployed, access StaffView at:
- **HTTP**: `http://your-domain.com`
- **HTTPS**: `https://your-domain.com`

Share with your team and start comparing those regression tests! ⚡

---

*Last updated: October 31, 2025*

