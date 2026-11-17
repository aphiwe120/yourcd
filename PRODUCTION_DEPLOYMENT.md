# 🚀 Production Deployment Guide - Live Link Setup

## Overview

This guide walks you through deploying the Medical Coding Assistant to production with a **live public URL** that doctors can access from anywhere.

---

## 🎯 Deployment Options

### Option 1: **Cloud Platform (Recommended for Quick Setup)**
- **Services**: Render, Heroku, Railway, Fly.io
- **Pros**: Easy setup, auto-scaling, SSL included, global access
- **Cons**: Small monthly cost ($7-50/month)
- **Time**: 15-30 minutes

### Option 2: **Hospital Server (On-Premises)**
- **Hardware**: Dedicated Windows/Linux server
- **Pros**: Full control, HIPAA-compliant, no cloud
- **Cons**: Requires IT infrastructure, security setup
- **Time**: 1-2 hours

### Option 3: **Docker + Kubernetes (Advanced)**
- **Pros**: Scalable, containerized, enterprise-ready
- **Cons**: Complex setup
- **Time**: 2-3 hours

---

## ⭐ OPTION 1: Deploy to Render.com (Easiest - Recommended)

### Step 1: Prepare Files for Deployment

Create a `Procfile` in your project root:

```
web: cd backend && python -m uvicorn app:app --host 0.0.0.0 --port $PORT
```

### Step 2: Create `.gitignore` (if not already present)

```
*.pyc
__pycache__/
.env
.DS_Store
*.egg-info/
dist/
build/
.venv/
venv/
```

### Step 3: Ensure `requirements.txt` is updated

```bash
cd C:\Users\sizwe\Downloads\yourcd\backend
pip freeze > requirements.txt
```

### Step 4: Push to GitHub

```bash
cd C:\Users\sizwe\Downloads\yourcd
git init
git add .
git commit -m "Initial commit: Medical Coding Assistant"
git remote add origin https://github.com/YOUR_USERNAME/yourcd.git
git branch -M main
git push -u origin main
```

### Step 5: Deploy on Render.com

1. Go to **https://render.com** and sign up (free account)
2. Click **"New" → "Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `medical-coding-assistant`
   - **Environment**: `Python 3.11`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && python -m uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free (or $7/month for better uptime)

5. Click **"Create Web Service"**
6. Wait for deployment (2-3 minutes)
7. Your live URL: `https://medical-coding-assistant.onrender.com`

### Cost
- **Free tier**: $0/month (can sleep after 15 min inactivity)
- **Paid tier**: $7-10/month (always online)

---

## 🏢 OPTION 2: Deploy to Hospital Server (On-Premises)

### Requirements
- **Server**: Windows Server 2019+ or Linux (Ubuntu 20.04+)
- **Hardware**: 2GB RAM, 10GB storage, 100Mbps network
- **Software**: Python 3.13, SSL certificate

### Step 1: Set Up Server

#### On Windows Server:
```powershell
# Install Python 3.13
# Download from https://www.python.org/downloads/

# Install dependencies
cd C:\your-app-location\backend
pip install -r requirements.txt

# Test run
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

#### On Linux Server:
```bash
sudo apt update
sudo apt install python3.13 python3.13-venv
python3.13 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

### Step 2: Configure Reverse Proxy (Nginx)

Create `/etc/nginx/sites-available/medical-coding`:

```nginx
upstream uvicorn {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name medical-coding.yourhospital.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name medical-coding.yourhospital.com;

    # SSL Certificates (from Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/medical-coding.yourhospital.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/medical-coding.yourhospital.com/privkey.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;

    location / {
        proxy_pass http://uvicorn;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static {
        alias /path/to/backend/static;
        expires 30d;
    }
}
```

### Step 3: Set Up SSL Certificate

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d medical-coding.yourhospital.com
```

### Step 4: Create Systemd Service (Auto-start)

Create `/etc/systemd/system/medical-coding.service`:

```ini
[Unit]
Description=Medical Coding Assistant
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/path/to/backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python -m uvicorn app:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable medical-coding
sudo systemctl start medical-coding
```

### Step 5: Configure Firewall

```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

---

## 🐳 OPTION 3: Docker Deployment (Advanced)

### Create `Dockerfile`

```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Copy requirements
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend/ ./

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Create `docker-compose.yml`

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    environment:
      - PYTHONUNBUFFERED=1
    restart: always
```

### Deploy

```bash
docker-compose up -d
# Access at http://localhost:8000
```

---

## 🔒 Security Best Practices for Production

### 1. Environment Variables
Create `.env` file:
```
OPENAI_API_KEY=sk-...
DATABASE_PATH=/secure/location/data.duckdb
DEBUG=False
ALLOWED_HOSTS=medical-coding.yourhospital.com
```

Update `app.py`:
```python
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_PATH = os.getenv("DATABASE_PATH", "data.duckdb")
DEBUG = os.getenv("DEBUG", "False") == "True"
```

### 2. HTTPS/SSL Certificate
- **Free**: Use Let's Encrypt (certbot)
- **Paid**: Purchase from Namecheap, GoDaddy

### 3. Rate Limiting
Add to `app.py`:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/query")
@limiter.limit("100/minute")
async def query_endpoint(request: Request, query: QueryRequest):
    # ... endpoint code
```

### 4. Database Backups
Automated daily backup:
```bash
# backup.sh (Linux/Mac)
#!/bin/bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
cp /app/data.duckdb /backups/data.duckdb.${TIMESTAMP}
# Keep last 30 days
find /backups -name "data.duckdb.*" -mtime +30 -delete
```

Schedule with cron:
```bash
0 2 * * * /path/to/backup.sh
```

### 5. Monitoring & Logging
Add to `app.py`:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
```

---

## 🌍 Domain Setup

### For Render.com (Easiest)
1. Buy domain from Namecheap ($1-15/year)
2. In Render dashboard: **Settings → Custom Domain**
3. Add: `medical-coding.yourhospital.com`
4. Add CNAME record to Namecheap DNS

### For Hospital Server
1. Set up DNS A record pointing to server IP
2. Configure SSL certificate for domain
3. Update nginx config with domain name

---

## 📊 Monitoring & Maintenance

### Health Check Endpoint
```bash
# Monitor every 5 minutes
curl https://medical-coding.yourhospital.com/api/health
```

### Database Size
```bash
# DuckDB file size
ls -lh data.duckdb
# Should be ~100MB

# Backup size
du -sh /backups/
```

### Server Resources
```bash
# CPU and Memory
top -b -n 1 | grep medical-coding

# Disk space
df -h
```

---

## 🚀 Deployment Checklist

### Pre-Deployment
- [ ] Update `requirements.txt`
- [ ] Test locally: `python -m uvicorn app:app --reload`
- [ ] Database backed up
- [ ] SSL certificate ready
- [ ] Environment variables configured
- [ ] Code committed to Git

### Deployment
- [ ] Deploy to production platform
- [ ] Verify domain works
- [ ] Test from multiple locations
- [ ] Check SSL certificate
- [ ] Verify database loaded (41,008 codes)

### Post-Deployment
- [ ] Share URL with medical staff
- [ ] Monitor logs for errors
- [ ] Check performance metrics
- [ ] Verify backups running
- [ ] Document support contacts

---

## 📱 Mobile & Remote Access

### For Hospital Staff at Home

**Option 1: VPN (Most Secure)**
```
1. Set up VPN on hospital server
2. Doctors connect to VPN
3. Access: http://internal-url
```

**Option 2: Public HTTPS (Easier)**
```
1. Deploy to public cloud
2. Add authentication (optional)
3. Access: https://medical-coding.yourhospital.com
```

**Option 3: Mobile App Wrapper**
```
Wrap web app in mobile shell:
- iOS: React Native / Swift
- Android: React Native / Kotlin
```

---

## 🔧 Troubleshooting Production Issues

### High CPU Usage
```bash
# Check slow queries
tail -f /var/log/medical-coding.log | grep SLOW

# Restart service
sudo systemctl restart medical-coding
```

### Database Locked Error
```bash
# Kill stuck processes
ps aux | grep uvicorn
kill -9 <PID>

# Restart
sudo systemctl restart medical-coding
```

### Out of Memory
```bash
# Check memory usage
free -h

# Increase swap
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### SSL Certificate Expired
```bash
# Renew certificate
sudo certbot renew

# Check expiration
sudo certbot certificates
```

---

## 📈 Expected Production Performance

| Metric | Expected | Alert Threshold |
|--------|----------|-----------------|
| Response Time | <1s | >5s |
| Uptime | 99%+ | <98% |
| CPU Usage | 1-5% | >80% |
| Memory | 500MB | >1.5GB |
| Disk | 100MB | >500GB |
| Error Rate | <0.1% | >1% |

---

## 💰 Cost Comparison

| Option | Setup | Monthly | Notes |
|--------|-------|---------|-------|
| **Render** | 15 min | $7-50 | Easiest, recommended |
| **Hospital Server** | 2 hours | $0 | Full control, requires IT |
| **Docker** | 1 hour | $20-100 | Cloud-agnostic |
| **AWS/Azure** | 1-2 hrs | $20-100 | Enterprise-grade |

---

## 🎯 Recommended Path (Quick Start)

**For immediate production launch (this week):**

1. ✅ Deploy to **Render.com** (free tier)
   - Takes 15 minutes
   - No credit card for free tier
   - Live URL in 3 minutes

2. ✅ Share URL with hospital IT
3. ✅ Collect feedback
4. ✅ Plan permanent solution (hospital server or paid cloud)

---

## 📞 Support During Deployment

### If you get stuck:
1. Check [ADMIN_GUIDE.md](ADMIN_GUIDE.md) - System operations
2. Review logs: `tail -f app.log`
3. Test API: `curl https://your-url/api/health`
4. Verify database: Check data.duckdb file exists

### Common Questions

**Q: Can doctors access from home?**
A: Yes! Deploy to cloud (Render/AWS) or set up VPN

**Q: What about HIPAA compliance?**
A: 
- No patient data stored (safe)
- Use hospital server (on-premises)
- Enable HTTPS/SSL
- Add authentication
- Log all accesses

**Q: How do I scale to 1000+ users?**
A: 
- Use cloud platform with auto-scaling
- Load balance across servers
- Upgrade database
- Add caching (Redis)

**Q: Can I use my own domain?**
A: Yes! All options support custom domains

---

## ✅ You're Ready!

Pick your deployment option and follow the steps. If you run into issues, refer back to this guide or the ADMIN_GUIDE.md.

**Next Steps:**
1. Choose deployment option (Render recommended for speed)
2. Follow the setup steps
3. Test from multiple devices
4. Share live URL with doctors
5. Monitor and collect feedback

---

**Questions?** Refer to the specific option section or check the ADMIN_GUIDE.md

**Estimated Time to Live:**
- Render.com: 20 minutes ⭐
- Hospital Server: 2 hours
- Docker: 1 hour

🚀 **Let's get it live!**
