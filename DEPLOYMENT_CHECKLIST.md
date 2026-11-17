# 🚀 Production Deployment Checklist

## Overview
This checklist guides you through deploying your Medical Coding Assistant to production with a live public URL.

---

## 🎯 Choose Your Deployment Method

### ⭐ **OPTION A: Render.com (Recommended - 15 minutes)**
- **Best for**: Quick launch, testing, low-to-medium usage
- **Cost**: Free or $7/month
- **Time**: 15 minutes
- **Difficulty**: Easy ✅
- **Follow**: [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)

### **OPTION B: Hospital Server (On-Premises)**
- **Best for**: HIPAA compliance, data control, long-term
- **Cost**: One-time setup (or $20-50/month server rental)
- **Time**: 2 hours
- **Difficulty**: Medium
- **Follow**: [PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md) → Option 2

### **OPTION C: Docker (Advanced)**
- **Best for**: Cloud-agnostic, containerized
- **Cost**: $20-100/month
- **Time**: 1-2 hours
- **Difficulty**: Hard
- **Follow**: [PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md) → Option 3

---

## 📋 RENDER.COM DEPLOYMENT (FASTEST PATH)

### Phase 1: Code Preparation (5 minutes)

#### ☐ Create Procfile
- [ ] File: `C:\Users\sizwe\Downloads\yourcd\Procfile`
- [ ] Content:
  ```
  web: cd backend && python -m uvicorn app:app --host 0.0.0.0 --port $PORT
  ```

#### ☐ Update requirements.txt
- [ ] Run: `pip install gunicorn`
- [ ] Run: `pip freeze > backend/requirements.txt`
- [ ] Verify file contains all dependencies:
  - [ ] fastapi
  - [ ] uvicorn
  - [ ] duckdb
  - [ ] pandas
  - [ ] openpyxl
  - [ ] pytest
  - [ ] gunicorn

#### ☐ Create .gitignore
- [ ] File: `C:\Users\sizwe\Downloads\yourcd\.gitignore`
- [ ] Content includes:
  - [ ] *.pyc
  - [ ] __pycache__/
  - [ ] .env
  - [ ] *.duckdb
  - [ ] venv/

### Phase 2: GitHub Setup (5 minutes)

#### ☐ Create GitHub Repository
- [ ] Go to https://github.com/new
- [ ] Repository name: `medical-coding-assistant`
- [ ] Description: "ICD-10 code lookup for South African doctors"
- [ ] Set to: Public
- [ ] Click: Create repository

#### ☐ Push Code to GitHub
```powershell
cd C:\Users\sizwe\Downloads\yourcd
git init
git add .
git commit -m "Medical Coding Assistant - Production ready with 41,008 ICD-10 codes"
git remote add origin https://github.com/YOURUSERNAME/medical-coding-assistant.git
git branch -M main
git push -u origin main
```

- [ ] Confirm all files pushed
- [ ] Verify data.duckdb is in repository

### Phase 3: Render Deployment (5 minutes)

#### ☐ Create Render Account
- [ ] Go to https://render.com
- [ ] Sign up (preferably with GitHub account)
- [ ] Authorize Render to access GitHub

#### ☐ Create Web Service
- [ ] Click: Dashboard
- [ ] Click: New → Web Service
- [ ] Click: Connect a repository
- [ ] Select: `medical-coding-assistant`
- [ ] Click: Connect

#### ☐ Configure Service
Complete the configuration form:

| Field | Value |
|-------|-------|
| Name | `medical-coding-assistant` |
| Environment | `Python 3.11` |
| Region | Closest to your location |
| Build Command | `pip install -r backend/requirements.txt` |
| Start Command | `cd backend && python -m uvicorn app:app --host 0.0.0.0 --port $PORT` |
| Plan | `Free` (or `Starter $7/mo`) |

- [ ] All fields filled correctly
- [ ] Ready to deploy

#### ☐ Deploy
- [ ] Click: Create Web Service
- [ ] ⏳ Wait 2-3 minutes for build
- [ ] ✅ Check deployment logs
- [ ] ✅ Verify no errors

### Phase 4: Verification (5 minutes)

#### ☐ Test Live URL
- [ ] Copy URL from Render dashboard
- [ ] Example: `https://medical-coding-assistant.onrender.com`

#### ☐ Test Health Endpoint
```bash
curl https://medical-coding-assistant.onrender.com/api/health
```
- [ ] Response: `{"status":"ok","row_count":41008}`
- [ ] Confirm: 41,008 codes loaded

#### ☐ Test Web Interface
- [ ] Open URL in browser
- [ ] Page loads without errors
- [ ] Type a diagnosis: "fever"
- [ ] Click: Search Codes
- [ ] Results display correctly
- [ ] Multiple codes shown
- [ ] No "generic results" issue

#### ☐ Test on Mobile
- [ ] Open on smartphone
- [ ] Mobile layout responsive
- [ ] Search functionality works
- [ ] Results readable

---

## 🌍 OPTIONAL: Add Custom Domain

### ☐ Purchase Domain
- [ ] Go to Namecheap.com or GoDaddy.com
- [ ] Search: `medical-coding.yourhospital.com`
- [ ] Purchase 1-year domain (~$10)

### ☐ Add to Render
- [ ] In Render dashboard: Settings
- [ ] Click: Custom Domain
- [ ] Enter domain: `medical-coding.yourhospital.com`
- [ ] Get CNAME value from Render
- [ ] Add CNAME record in Namecheap DNS
- [ ] Wait 24 hours for DNS propagation

### ☐ Verify Custom Domain
- [ ] Access: `https://medical-coding.yourhospital.com`
- [ ] Confirm HTTPS works
- [ ] No SSL certificate warnings

---

## 📱 SHARE WITH HOSPITAL STAFF

### ☐ Document Preparation
- [ ] Copy: [DOCTORS_GUIDE.md](DOCTORS_GUIDE.md)
- [ ] Copy: [QUICK_START.md](QUICK_START.md)
- [ ] Copy: [ADMIN_GUIDE.md](ADMIN_GUIDE.md)

### ☐ Share with Doctors
- [ ] Send email with:
  - [ ] Live URL
  - [ ] Copy of DOCTORS_GUIDE.md
  - [ ] Copy of QUICK_START.md
  - [ ] Support contact information

### ☐ Brief IT Team
- [ ] Email: [ADMIN_GUIDE.md](ADMIN_GUIDE.md)
- [ ] Email: [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)
- [ ] Explain monitoring procedures
- [ ] Provide support contacts

### ☐ Optional: Training Session
- [ ] Schedule 15-minute webinar
- [ ] Show live demo
- [ ] Answer questions
- [ ] Record for reference

---

## 📊 POST-DEPLOYMENT MONITORING

### Daily (First Week)
- [ ] Check Render logs for errors
- [ ] Monitor performance metrics
- [ ] Verify health endpoint: `/api/health`
- [ ] Check error rate

### Weekly
- [ ] Review usage statistics
- [ ] Analyze search patterns
- [ ] Gather user feedback
- [ ] Check response times
- [ ] Verify uptime

### Monthly
- [ ] Review performance metrics
- [ ] Plan for upgrades
- [ ] Evaluate custom domain needs
- [ ] Consider upgrading to Starter plan if needed

---

## 🔧 TROUBLESHOOTING

### Issue: "Service offline"
- [ ] Check Render Logs
- [ ] Restart service: Settings → Restart Service
- [ ] Or: Push new commit to redeploy

### Issue: "Build failed"
- [ ] Check Build Logs in Render
- [ ] Usually missing dependency
- [ ] Add to requirements.txt
- [ ] Run: `pip freeze > requirements.txt`
- [ ] Push: `git push origin main`

### Issue: "No results from search"
- [ ] Already fixed in updated query_engine.py
- [ ] Verify: [SEARCH_ENGINE_FIX.md](SEARCH_ENGINE_FIX.md)
- [ ] Confirm: Deployment includes latest code

### Issue: "Database error"
- [ ] Verify: data.duckdb in GitHub repo
- [ ] Check: File permissions (644)
- [ ] Confirm: 41,008 records loaded

### Issue: "Slow loading"
- [ ] Free tier might be waking up (normal)
- [ ] Upgrade to Starter plan ($7/mo)
- [ ] Or switch to hospital server

---

## 💰 COST MANAGEMENT

### Free Tier ($0/month)
- [ ] App sleeps after 15 minutes
- [ ] Fine for testing and demos
- [ ] Restart time: ~30 seconds
- [ ] Good for: Initial launch

### Starter Plan ($7/month)
- [ ] Always-on (no sleeping)
- [ ] 100GB/month bandwidth
- [ ] Email support
- [ ] Good for: Hospital deployment

### When to Upgrade?
- [ ] Usage: >100 queries/day → Consider Starter
- [ ] Critical: Hospital-wide production → Must use Starter
- [ ] Scale: >1000 users → Consider Business plan

---

## 🔐 SECURITY CHECKLIST

### Database Security
- [ ] Read-only enforced
- [ ] No write operations allowed
- [ ] No patient data stored
- [ ] Regular backups in place

### Network Security
- [ ] HTTPS/SSL enabled ✅
- [ ] No unencrypted traffic
- [ ] Input validation active
- [ ] XSS protection enabled

### Authentication (Optional)
- [ ] Identify if needed
- [ ] Add to app.py if required:
  ```python
  from fastapi.security import HTTPBearer
  ```
- [ ] Update deployment if added

### Monitoring
- [ ] Render logs monitored
- [ ] Error alerts set up
- [ ] Performance baseline established
- [ ] Unusual activity tracked

---

## ✅ FINAL VERIFICATION

Before declaring "Live and Ready":

### Code
- [ ] All changes committed to Git
- [ ] Latest version deployed
- [ ] Search engine fixed (41,008 → specific results)
- [ ] No debug mode enabled

### Deployment
- [ ] Service deployed successfully
- [ ] No build errors
- [ ] No runtime errors
- [ ] Health check passing

### Functionality
- [ ] Web interface loads
- [ ] Search works (fever, diabetes, etc.)
- [ ] Results are specific (not generic)
- [ ] Mobile responsive

### Documentation
- [ ] RENDER_DEPLOYMENT.md ✅
- [ ] DOCTORS_GUIDE.md ✅
- [ ] ADMIN_GUIDE.md ✅
- [ ] QUICK_START.md ✅
- [ ] SEARCH_ENGINE_FIX.md ✅

### Users
- [ ] Medical staff notified
- [ ] IT team briefed
- [ ] Documentation distributed
- [ ] Support contacts provided

---

## 🎉 YOU'RE LIVE!

### Your Production Setup Includes:
✅ Live public URL (accessible worldwide)
✅ Automatic HTTPS/SSL encryption
✅ 41,008 ICD-10 codes loaded
✅ Specific search results (not generic)
✅ Mobile-friendly interface
✅ No patient data storage
✅ Automatic monitoring
✅ Easy scaling if needed

### Hospital Staff Can Now:
✅ Access from any browser
✅ Search for ICD-10 codes
✅ Find specific, relevant results
✅ Use on mobile phones
✅ No login required
✅ No special training needed

---

## 📞 SUPPORT DURING DEPLOYMENT

### Common Questions

**Q: How long until it's live?**
A: 15 minutes from start to finish!

**Q: Can doctors access from home?**
A: Yes! Live URL works worldwide

**Q: Is it secure?**
A: Yes! HTTPS/SSL + read-only database + no patient data

**Q: What if something breaks?**
A: Check Render logs, usually just restart service

**Q: Can we add authentication?**
A: Yes, follow ADMIN_GUIDE.md for details

**Q: How do we upgrade to paid tier?**
A: Click Settings → Plan in Render dashboard

---

## 🚀 DEPLOYMENT TIMELINE

| Phase | Time | Status |
|-------|------|--------|
| Code Prep | 5 min | ⏳ |
| GitHub Push | 5 min | ⏳ |
| Render Setup | 5 min | ⏳ |
| Deployment | 2-3 min | ⏳ |
| Verification | 5 min | ⏳ |
| **TOTAL** | **15 minutes** | **🎉 LIVE** |

---

## 📄 Documentation Reference

| Document | Purpose | Audience |
|----------|---------|----------|
| [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) | Deployment steps | Developers |
| [PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md) | All options | Architects |
| [DOCTORS_GUIDE.md](DOCTORS_GUIDE.md) | How to use | Doctors |
| [ADMIN_GUIDE.md](ADMIN_GUIDE.md) | Operations | IT Admin |
| [SEARCH_ENGINE_FIX.md](SEARCH_ENGINE_FIX.md) | Technical details | Developers |
| [QUICK_START.md](QUICK_START.md) | 1-page guide | Everyone |

---

## ✨ You're Ready!

✅ All documentation prepared  
✅ Code is production-ready  
✅ Database is loaded (41,008 codes)  
✅ Search engine is fixed (specific results)  
✅ Security is in place  

**Next Step:** Follow [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) and go live! 🚀

---

**Deployment Date**: [Enter date]  
**Deployed By**: [Enter name]  
**Live URL**: [Enter URL]  
**Status**: 🟢 PRODUCTION READY
