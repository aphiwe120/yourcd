# 🚀 Deploy to Render.com in 15 Minutes

## Overview
This is the **fastest way** to get your Medical Coding Assistant live with a public URL that anyone can access.

**Time Required**: 15-20 minutes  
**Cost**: Free (or $7/month for always-on)  
**Result**: Live URL like `https://medical-coding-assistant.onrender.com`

---

## 📋 Prerequisites

1. ✅ GitHub account (free at github.com)
2. ✅ Render account (free at render.com)
3. ✅ Your code ready to push

---

## 🔧 Step 1: Prepare Your Code for Deployment

### 1a. Create `Procfile` in project root

Create a file at: `C:\Users\sizwe\Downloads\yourcd\Procfile`

**Content:**
```
web: cd backend && python -m uvicorn app:app --host 0.0.0.0 --port $PORT
```

This tells Render how to start your app.

### 1b. Update `requirements.txt` with ALL dependencies

```bash
cd C:\Users\sizwe\Downloads\yourcd\backend
pip install gunicorn  # Production server
pip freeze > requirements.txt
```

Your `requirements.txt` should include:
- fastapi
- uvicorn
- duckdb
- pandas
- openpyxl
- pytest
- gunicorn

### 1c. Create `.gitignore` file

Create: `C:\Users\sizwe\Downloads\yourcd\.gitignore`

**Content:**
```
*.pyc
__pycache__/
*.pyo
*.egg-info/
dist/
build/
.env
*.db
*.duckdb
.DS_Store
.venv/
venv/
```

---

## 🌐 Step 2: Push Code to GitHub

### 2a. Create GitHub Repository

1. Go to **https://github.com/new**
2. **Repository name**: `medical-coding-assistant`
3. **Description**: "ICD-10 code lookup for South African doctors"
4. **Public** (so Render can access it)
5. Click **"Create repository"**

### 2b. Push Your Code

```powershell
cd C:\Users\sizwe\Downloads\yourcd

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Medical Coding Assistant - Production ready with 41,008 ICD-10 codes"

# Add remote (replace YOURUSERNAME with your GitHub username)
git remote add origin https://github.com/YOURUSERNAME/medical-coding-assistant.git

# Rename branch to main
git branch -M main

# Push
git push -u origin main
```

**Example:**
```powershell
git remote add origin https://github.com/aphiwe120/medical-coding-assistant.git
```

---

## 🚀 Step 3: Deploy on Render.com

### 3a. Create Render Account

1. Go to **https://render.com**
2. Click **"Sign up"** (free account)
3. Use GitHub to sign up (easiest)
4. Grant Render access to your GitHub

### 3b. Create Web Service

1. Click **"Dashboard"** (top right)
2. Click **"New" → "Web Service"**
3. Click **"Connect a repository"**
4. Find and select `medical-coding-assistant`
5. Click **"Connect"**

### 3c. Configure Service

**Fill in these fields:**

| Field | Value |
|-------|-------|
| **Name** | `medical-coding-assistant` |
| **Environment** | `Python 3.11` |
| **Region** | `Singapore` (or closest to you) |
| **Build Command** | `pip install -r backend/requirements.txt` |
| **Start Command** | `cd backend && python -m uvicorn app:app --host 0.0.0.0 --port $PORT` |
| **Plan** | `Free` (or `Starter` for $7/month) |

### 3d. Deploy

1. Click **"Create Web Service"**
2. Wait 2-3 minutes for deployment
3. ✅ Your live URL will appear!

**Example URL**: `https://medical-coding-assistant.onrender.com`

---

## ✅ Verification

### Check if it's working:

```bash
# Health check
curl https://medical-coding-assistant.onrender.com/api/health
```

**Expected Response:**
```json
{"status":"ok","row_count":41008}
```

### Try a search:

Open in browser:
```
https://medical-coding-assistant.onrender.com
```

Type a diagnosis to search!

---

## 🌍 Add Custom Domain (Optional)

### 5a. Buy Domain

1. Go to **Namecheap.com** or **GoDaddy.com**
2. Search for domain like: `medical-coding.yourhospital.com`
3. Buy for 1 year (~$10)

### 5b. Add to Render

1. In Render dashboard, go to **Settings**
2. Click **"Custom Domain"**
3. Enter your domain: `medical-coding.yourhospital.com`
4. Add the CNAME record from Namecheap

Done! Now you have: `https://medical-coding.yourhospital.com`

---

## 📊 Monitoring

### View Logs
- In Render dashboard, click **"Logs"**
- Scroll to see real-time activity

### Monitor Performance
- Click **"Metrics"**
- View CPU, Memory, Requests

### Check Status
```bash
curl https://your-url/api/health
```

---

## 🔄 Deploy Updates

When you make code changes:

```bash
cd C:\Users\sizwe\Downloads\yourcd
git add .
git commit -m "Updated search engine"
git push origin main
```

Render automatically redeploys! ✨

---

## 💡 Pro Tips

### Free Tier Limitations
- App sleeps after 15 minutes of inactivity
- Wakes up when accessed (takes 30 seconds)
- Perfect for testing

### Free Tier to Paid
- Click **"Settings" → "Plan"**
- Upgrade to **Starter ($7/month)** for:
  - Always-on (no sleeping)
  - Custom domain
  - Better performance

### Environment Variables (If Needed)

1. In Render: **Settings → Environment**
2. Add variables:
   ```
   OPENAI_API_KEY=sk-...
   DATABASE_URL=/path/to/data.duckdb
   ```

3. Update Python code to use them:
   ```python
   import os
   api_key = os.getenv("OPENAI_API_KEY")
   ```

---

## 🆘 Troubleshooting

### "Build failed"
- Check **Logs** tab
- Usually missing dependency in requirements.txt
- Fix and push again

### "Service is offline"
- Check **Logs** for errors
- Restart: **Settings → Restart Service**
- Or redeploy: `git push origin main`

### "Database connection error"
- Make sure data.duckdb is committed to Git
- Check file permissions

### "Slow loading"
- Likely free tier waking up from sleep
- Upgrade to Starter plan ($7/month)

---

## 🎯 Share with Hospital

Once deployed, share this link:
```
https://medical-coding-assistant.onrender.com
```

**OR** (if using custom domain):
```
https://medical-coding.yourhospital.com
```

That's it! 🎉

---

## 📱 Mobile Access

The app is fully responsive! Doctors can access from:
- 💻 Desktop browsers
- 📱 Mobile phones
- 📲 Tablets
- 🖥️ Any device with a browser

---

## 🔒 Security Note

The free Render deployment:
- ✅ Has HTTPS/SSL by default
- ✅ No patient data stored
- ✅ Read-only database
- ✅ Safe for hospital use

For HIPAA compliance:
- Consider upgrading to paid tier
- Add authentication if needed
- Use hospital server instead (see PRODUCTION_DEPLOYMENT.md)

---

## 📊 Quick Comparison

| Feature | Free | Starter ($7/mo) | Business ($50/mo) |
|---------|------|-----------------|-------------------|
| **Always On** | ❌ | ✅ | ✅ |
| **Custom Domain** | ❌ | ✅ | ✅ |
| **Free Tier URL** | ✅ | ✅ | ✅ |
| **Performance** | Fair | Good | Excellent |
| **Best For** | Testing | Hospital | Enterprise |

---

## ✅ Deployment Complete!

You now have:
- ✅ Live public URL
- ✅ 41,008 ICD-10 codes accessible
- ✅ Automatic HTTPS/SSL
- ✅ No patient data stored
- ✅ Fast <1 second searches
- ✅ Mobile-friendly interface

---

## 🎓 Next Steps

1. ✅ Share URL with medical staff
2. ✅ Send them [DOCTORS_GUIDE.md](DOCTORS_GUIDE.md)
3. ✅ Gather feedback
4. ✅ Monitor usage in Render dashboard
5. ✅ Plan next phase (custom domain, etc.)

---

## 📞 Support

If you get stuck:
1. Check **Render Logs** (dashboard → Logs)
2. Review [PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md)
3. See [ADMIN_GUIDE.md](ADMIN_GUIDE.md) for general troubleshooting

---

**Congratulations!** 🎉 Your Medical Coding Assistant is now live and accessible to your entire hospital!

Time to deployment: **15 minutes**  
Cost: **Free (optional $7/month)**  
Result: **Live production URL ready for use**

🚀 **Go live with confidence!**
