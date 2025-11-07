#!/usr/bin/env python3
"""
Keep-alive script to prevent Render free tier cold starts
Run this on a separate service or your local machine
"""
import requests
import time
from datetime import datetime

# Your WizardView URL
STAFFVIEW_URL = "https://staffview.onrender.com"  # Update with your actual URL
PING_INTERVAL = 14 * 60  # 14 minutes in seconds

def ping_service():
    """Ping the service to keep it alive"""
    try:
        response = requests.get(f"{STAFFVIEW_URL}/api/structure", timeout=30)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if response.status_code in [200, 302]:  # 302 is redirect to login
            print(f"[{timestamp}] ✓ Service is alive (status: {response.status_code})")
        else:
            print(f"[{timestamp}] ⚠ Unexpected status: {response.status_code}")
    except requests.exceptions.Timeout:
        print(f"[{timestamp}] ⚠ Request timeout")
    except Exception as e:
        print(f"[{timestamp}] ✗ Error: {e}")

if __name__ == "__main__":
    print(f"Starting keep-alive service for {STAFFVIEW_URL}")
    print(f"Pinging every {PING_INTERVAL // 60} minutes")
    print("-" * 60)
    
    while True:
        ping_service()
        time.sleep(PING_INTERVAL)

