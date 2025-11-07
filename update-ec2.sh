#!/bin/bash
# WizardView EC2 Update Script
# Run this script to update WizardView on your EC2 instance

set -e  # Exit on error

echo "🧙‍♂️ Updating WizardView..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

APP_DIR="/var/www/staffview"
SERVICE_NAME="staffview"

cd "$APP_DIR"

echo -e "${BLUE}1. Pulling latest changes...${NC}"
git pull origin main

echo -e "${BLUE}2. Updating dependencies...${NC}"
source venv/bin/activate
pip install -r requirements.txt

echo -e "${BLUE}3. Restarting application...${NC}"
sudo systemctl restart $SERVICE_NAME

echo -e "${BLUE}4. Checking status...${NC}"
sleep 2
sudo systemctl status $SERVICE_NAME --no-pager | head -10

echo ""
echo -e "${GREEN}✓ Update complete!${NC}"
echo ""
echo "View logs with: sudo journalctl -u $SERVICE_NAME -f"

