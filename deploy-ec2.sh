#!/bin/bash
# WizardView EC2 Deployment Script
# Run this script ON YOUR EC2 INSTANCE after cloning the repository

set -e  # Exit on error

echo "🧙‍♂️ WizardView EC2 Deployment Script"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
APP_DIR="/var/www/staffview"
APP_USER="ubuntu"
SERVICE_NAME="staffview"

echo -e "${BLUE}Step 1: Checking prerequisites...${NC}"
# Check if running as ubuntu user
if [ "$USER" != "$APP_USER" ]; then
    echo -e "${YELLOW}Warning: This script should be run as ubuntu user${NC}"
    echo "Current user: $USER"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo -e "${GREEN}✓ Prerequisites check complete${NC}"
echo ""

echo -e "${BLUE}Step 2: Installing system dependencies...${NC}"
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx git

echo -e "${GREEN}✓ System dependencies installed${NC}"
echo ""

echo -e "${BLUE}Step 3: Setting up application directory...${NC}"
if [ ! -d "$APP_DIR" ]; then
    sudo mkdir -p "$APP_DIR"
    sudo chown $APP_USER:$APP_USER "$APP_DIR"
fi

cd "$APP_DIR"

# Check if this is a git repository
if [ ! -d ".git" ]; then
    echo "Error: Not a git repository. Please clone the repository first:"
    echo "  git clone https://github.com/Yeltsin-Z/WizardView.git $APP_DIR"
    exit 1
fi

echo -e "${GREEN}✓ Application directory ready${NC}"
echo ""

echo -e "${BLUE}Step 4: Setting up Python virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${GREEN}✓ Python environment ready${NC}"
echo ""

echo -e "${BLUE}Step 5: Creating required directories...${NC}"
mkdir -p uploads/extracted
chmod 755 uploads

echo -e "${GREEN}✓ Directories created${NC}"
echo ""

echo -e "${BLUE}Step 6: Setting up systemd service...${NC}"
sudo tee /etc/systemd/system/$SERVICE_NAME.service > /dev/null <<EOF
[Unit]
Description=WizardView - Regression Artifacts Comparison Tool
After=network.target

[Service]
Type=notify
User=$APP_USER
Group=$APP_USER
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/gunicorn app:app --config gunicorn_config.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl restart $SERVICE_NAME

echo -e "${GREEN}✓ Systemd service configured${NC}"
echo ""

echo -e "${BLUE}Step 7: Configuring Nginx...${NC}"

# Get the server name (use public IP or ask user)
read -p "Enter your domain name or press Enter to use EC2 public IP: " SERVER_NAME

if [ -z "$SERVER_NAME" ]; then
    # Try to get public IP
    SERVER_NAME=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 || echo "_")
fi

sudo tee /etc/nginx/sites-available/$SERVICE_NAME > /dev/null <<EOF
server {
    listen 80;
    server_name $SERVER_NAME;
    
    client_max_body_size 100M;
    
    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        proxy_connect_timeout 600s;
        proxy_send_timeout 600s;
        proxy_read_timeout 600s;
    }
    
    location /static {
        alias $APP_DIR/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Enable site
sudo ln -sf /etc/nginx/sites-available/$SERVICE_NAME /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test and restart Nginx
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl enable nginx

echo -e "${GREEN}✓ Nginx configured${NC}"
echo ""

echo -e "${BLUE}Step 8: Setting up firewall...${NC}"
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
echo "y" | sudo ufw enable || true

echo -e "${GREEN}✓ Firewall configured${NC}"
echo ""

echo -e "${GREEN}=================================="
echo "🧙‍♂️ WizardView Deployment Complete!"
echo "==================================${NC}"
echo ""
echo "Application Status:"
sudo systemctl status $SERVICE_NAME --no-pager | head -5
echo ""
echo "Access your application at:"
echo "  http://$SERVER_NAME"
echo ""
echo "Useful commands:"
echo "  View logs:       sudo journalctl -u $SERVICE_NAME -f"
echo "  Restart app:     sudo systemctl restart $SERVICE_NAME"
echo "  Check status:    sudo systemctl status $SERVICE_NAME"
echo ""
echo "Next steps:"
echo "  1. Test the application by opening http://$SERVER_NAME"
echo "  2. (Optional) Set up SSL with: sudo certbot --nginx -d yourdomain.com"
echo "  3. (Optional) Configure monitoring and backups"
echo ""
echo "Happy comparing! 🚀"

