# 🚀 QUICK START REFERENCE CARD

## ⚡ For Hospital Staff (Doctors & Coders)

```
1. Open browser
2. Go to: http://localhost:8000
3. Type diagnosis: "fever and cough"
4. Click: Search
5. View results: ICD-10 codes
6. Done!
```

**Questions?** → Read [DOCTORS_GUIDE.md](DOCTORS_GUIDE.md)

---

## 🏥 For Hospital IT (Administrators)

```
Check Status:
  curl http://localhost:8000/api/health

Expected: {"status":"ok","row_count":41008}

If down:
  cd C:\Users\sizwe\Downloads\yourcd\backend
  python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

**Full Guide?** → Read [ADMIN_GUIDE.md](ADMIN_GUIDE.md)

---

## ⚙️ For Technical Staff (Developers)

**System Files:**
- Backend: `C:\Users\sizwe\Downloads\yourcd\backend\`
- Database: `backend\data.duckdb` (41,008 codes)
- Frontend: `backend\static\` (HTML/CSS/JS)
- API: `backend\app.py` (FastAPI)

**Documentation:** Read [backend/README.md](backend/README.md)

---

## 📊 System At A Glance

| Item | Status | Details |
|------|--------|---------|
| **Server** | ✅ | Port 8000, running |
| **Database** | ✅ | 41,008 SA ICD-10 codes |
| **Frontend** | ✅ | Doctor-friendly UI |
| **API** | ✅ | All endpoints working |
| **Performance** | ✅ | <1 second response |
| **Security** | ✅ | Read-only, no patient data |

---

## 📚 Documentation Index

| Guide | For Whom | Purpose |
|-------|----------|---------|
| **README.md** | Everyone | Start here! Overview |
| **DOCTORS_GUIDE.md** | Doctors | How to use system |
| **ADMIN_GUIDE.md** | IT Admin | Operations & monitoring |
| **backend/README.md** | Developers | Technical details |
| **LAUNCH_CHECKLIST.md** | IT Manager | Pre-launch checklist |
| **SYSTEM_SUMMARY.txt** | Management | Executive summary |

---

## 🎯 Key Facts

- **41,008** SA ICD-10 codes loaded
- **<1 second** average search time
- **No login** required
- **Mobile** friendly
- **Read-only** database (safe)
- **No patient data** stored
- **Runs on** port 8000

---

## 🌐 Access URLs

```
Web Interface:     http://localhost:8000
Health Check:      http://localhost:8000/api/health
API Query:         http://localhost:8000/api/query (POST)
```

---

## 🆘 If Something Breaks

1. **Check health:**
   ```
   curl http://localhost:8000/api/health
   ```

2. **Restart server:**
   ```
   Kill Python process, then:
   python -m uvicorn app:app --host 0.0.0.0 --port 8000
   ```

3. **Still broken?**
   - Read: [ADMIN_GUIDE.md](ADMIN_GUIDE.md) - Troubleshooting section

---

## ✅ You're All Set!

**Everything is ready to use. No installation or configuration needed.**

👉 **Next Step:** Share `http://localhost:8000` with doctors and provide them with [DOCTORS_GUIDE.md](DOCTORS_GUIDE.md)

---

**Version:** 1.0  
**Status:** Production Ready  
**Date:** 2024-11-17  
**Data:** 41,008 SA ICD-10 Codes (2021)
