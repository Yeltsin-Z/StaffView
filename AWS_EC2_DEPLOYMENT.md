# ⚡ StaffView - AWS EC2 Deployment Guide

Complete guide to deploy StaffView on AWS EC2.

## Prerequisites

- AWS Account with EC2 access
- SSH key pair for EC2 access
- Domain name (optional, for custom domain)

---

## Step 1: Launch EC2 Instance

### 1.1 Create EC2 Instance
1. Log in to AWS Console → EC2 Dashboard
2. Click **"Launch Instance"**
3. Configure:
   - **Name**: `staffview-server`
   - **AMI**: Ubuntu Server 22.04 LTS (Free tier eligible)
   - **Instance type**: t2.micro (free tier) or t2.small (recommended)
   - **Key pair**: Create new or use existing
   - **Network settings**:
     - ✅ Allow SSH (port 22) from your IP
     - ✅ Allow HTTP (port 80) from anywhere
     - ✅ Allow HTTPS (port 443) from anywhere (if using SSL)
   - **Storage**: 8-20 GB gp3
4. Click **"Launch Instance"**

### 1.2 Note Your Instance Details
```bash
# Note these values:
EC2_PUBLIC_IP="your-ec2-public-ip"
KEY_FILE="path/to/your-key.pem"
```

---

## Step 2: Connect to Your EC2 Instance

```bash
# Set correct permissions for your key file
chmod 400 your-key.pem

# Connect via SSH
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

---

## Step 3: Install Dependencies on EC2

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install Nginx (web server/reverse proxy)
sudo apt install nginx -y

# Install Git
sudo apt install git -y

# Verify installations
python3 --version
pip3 --version
nginx -v
git --version
```

---

## Step 4: Deploy StaffView Application

### 4.1 Clone the Repository
```bash
# Create application directory
sudo mkdir -p /var/www/staffview
sudo chown ubuntu:ubuntu /var/www/staffview
cd /var/www/staffview

# Clone your repository
git clone https://github.com/Yeltsin-Z/StaffView.git .
```

### 4.2 Set Up Python Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Test the application
python app.py
# Press Ctrl+C to stop after verifying it starts
```

### 4.3 Create Directories
```bash
# Create uploads directory
mkdir -p uploads/extracted
```

---

## Step 5: Configure Systemd Service

Create a systemd service to run StaffView automatically:

```bash
# Create service file
sudo nano /etc/systemd/system/staffview.service
```

Paste this configuration:

```ini
[Unit]
Description=StaffView - Regression Artifacts Comparison Tool
After=network.target

[Service]
Type=notify
User=ubuntu
Group=ubuntu
WorkingDirectory=/var/www/staffview
Environment="PATH=/var/www/staffview/venv/bin"
ExecStart=/var/www/staffview/venv/bin/gunicorn app:app --config gunicorn_config.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Save and exit (Ctrl+X, Y, Enter).

### 5.1 Start the Service
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable staffview

# Start the service
sudo systemctl start staffview

# Check status
sudo systemctl status staffview

# View logs if needed
sudo journalctl -u staffview -f
```

---

## Step 6: Configure Nginx as Reverse Proxy

### 6.1 Create Nginx Configuration
```bash
# Create Nginx site configuration
sudo nano /etc/nginx/sites-available/staffview
```

Paste this configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;  # Replace with your domain or EC2 public IP
    
    client_max_body_size 100M;  # Allow large file uploads
    
    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Increase timeouts for large uploads
        proxy_connect_timeout 600s;
        proxy_send_timeout 600s;
        proxy_read_timeout 600s;
    }
    
    location /static {
        alias /var/www/staffview/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

Save and exit (Ctrl+X, Y, Enter).

### 6.2 Enable the Site
```bash
# Create symbolic link to enable site
sudo ln -s /etc/nginx/sites-available/staffview /etc/nginx/sites-enabled/

# Remove default site (optional)
sudo rm /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx

# Enable Nginx to start on boot
sudo systemctl enable nginx
```

---

## Step 7: Access Your Application

Your StaffView application should now be accessible at:
- **HTTP**: `http://your-ec2-public-ip`
- **With Domain**: `http://your-domain.com` (after DNS configuration)

---

## Step 8 (Optional): Set Up SSL with Let's Encrypt

### 8.1 Install Certbot
```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 8.2 Obtain SSL Certificate
```bash
# Replace with your domain
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

Follow the prompts:
- Enter email address
- Agree to terms
- Choose to redirect HTTP to HTTPS (recommended)

### 8.3 Auto-Renewal
```bash
# Test auto-renewal
sudo certbot renew --dry-run

# Auto-renewal is set up automatically via cron/systemd timer
```

---

## Useful Commands

### Application Management
```bash
# View application logs
sudo journalctl -u staffview -f

# Restart application
sudo systemctl restart staffview

# Stop application
sudo systemctl stop staffview

# Check application status
sudo systemctl status staffview
```

### Update Application
```bash
cd /var/www/staffview
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart staffview
```

### Nginx Management
```bash
# Test Nginx config
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### System Monitoring
```bash
# Check disk space
df -h

# Check memory usage
free -h

# Check running processes
top

# Check open ports
sudo netstat -tulpn | grep LISTEN
```

---

## Security Best Practices

### 1. Update Security Group Rules
- Restrict SSH (port 22) to your IP only
- Keep HTTP (80) and HTTPS (443) open

### 2. Set Up Firewall (UFW)
```bash
# Enable UFW
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 80/tcp      # HTTP
sudo ufw allow 443/tcp     # HTTPS
sudo ufw enable
sudo ufw status
```

### 3. Regular Updates
```bash
# Set up automatic security updates
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure --priority=low unattended-upgrades
```

### 4. Monitor Logs
```bash
# Check auth logs for suspicious activity
sudo tail -f /var/log/auth.log
```

---

## Troubleshooting

### Application Won't Start
```bash
# Check service status
sudo systemctl status staffview

# View detailed logs
sudo journalctl -u staffview -n 50

# Check if port 5001 is in use
sudo netstat -tulpn | grep 5001

# Manually test the app
cd /var/www/staffview
source venv/bin/activate
python app.py
```

### 502 Bad Gateway
```bash
# Check if Gunicorn is running
sudo systemctl status staffview

# Check Nginx error logs
sudo tail -f /var/log/nginx/error.log

# Verify Nginx can reach Gunicorn
curl http://127.0.0.1:5001
```

### Permission Issues
```bash
# Fix ownership
sudo chown -R ubuntu:ubuntu /var/www/staffview

# Fix permissions for uploads
chmod -R 755 /var/www/staffview/uploads
```

### Out of Disk Space
```bash
# Check disk usage
df -h

# Find large files
sudo du -h /var/www/staffview | sort -rh | head -10

# Clean up uploads (if needed)
rm -rf /var/www/staffview/uploads/extracted/*
```

---

## Backup Strategy

### Automated Backup Script
```bash
# Create backup script
sudo nano /usr/local/bin/backup-staffview.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/home/ubuntu/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup uploads
tar -czf $BACKUP_DIR/staffview-uploads-$DATE.tar.gz /var/www/staffview/uploads

# Keep only last 7 days
find $BACKUP_DIR -name "staffview-uploads-*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

```bash
# Make executable
sudo chmod +x /usr/local/bin/backup-staffview.sh

# Schedule daily backup (crontab)
crontab -e
# Add this line:
0 2 * * * /usr/local/bin/backup-staffview.sh
```

---

## Cost Optimization

### Free Tier Eligible Setup
- **Instance**: t2.micro (750 hours/month free for 12 months)
- **Storage**: 30 GB EBS (free tier)
- **Data Transfer**: 15 GB out/month (free tier)

### Beyond Free Tier
- Consider **t2.small** for better performance (~$17/month)
- Use **Reserved Instances** for 30-70% discount (1-3 year commitment)
- Monitor costs with **AWS Budgets**

---

## Next Steps

1. ✅ Application is running on EC2
2. ✅ Accessible via public IP
3. 🔄 Point your domain to EC2 (optional)
4. 🔄 Set up SSL certificate (recommended)
5. 🔄 Configure monitoring and alerts
6. 🔄 Set up automated backups

---

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review application logs: `sudo journalctl -u staffview -f`
3. Review Nginx logs: `sudo tail -f /var/log/nginx/error.log`

Happy deploying! 🚀

