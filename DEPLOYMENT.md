# 🚀 PythonAnywhere Deployment Guide

## Step 1: Create Account
1. Go to: https://www.pythonanywhere.com
2. Click "Sign up" and choose **Beginner (Free)** account
3. Remember your username!

---

## Step 2: Upload Files

### Option A: Using GitHub (Recommended)
1. Create a GitHub repository
2. Push your code to GitHub
3. In PythonAnywhere, open a **Bash console**
4. Run:
   ```bash
   git clone https://github.com/YOUR_USERNAME/supplier-collector.git
   cd supplier-collector
   ```

### Option B: Manual Upload
1. Go to **"Files"** tab in PythonAnywhere
2. Click "Upload a file"
3. Upload these files:
   - `app.py`
   - `wsgi.py`
   - `requirements.txt`
   - `schema.json`
   - `static/index.html`

---

## Step 3: Install Dependencies
1. Open a **Bash console** (from "Consoles" tab)
2. Run these commands:
   ```bash
   cd supplier-collector
   pip3.10 install --user flask openpyxl
   ```

---

## Step 4: Configure Web App
1. Go to **"Web"** tab
2. Click **"Add a new web app"**
3. Choose your domain: `YOUR_USERNAME.pythonanywhere.com`
4. Select **"Manual configuration"**
5. Choose **Python 3.10**

### Configure WSGI file:
1. Click on the WSGI configuration file link
2. **Delete everything** in the file
3. Paste this code:
   ```python
   import sys
   import os

   # IMPORTANT: Replace YOUR_USERNAME with your actual username
   project_home = '/home/YOUR_USERNAME/supplier-collector'
   if project_home not in sys.path:
       sys.path = [project_home] + sys.path

   from app import app as application
   ```
4. Save the file

### Set paths:
Back in the Web tab, set:
- **Source code**: `/home/YOUR_USERNAME/supplier-collector`
- **Working directory**: `/home/YOUR_USERNAME/supplier-collector`

---

## Step 5: Create data folder
In Bash console:
```bash
cd supplier-collector
mkdir -p data
```

---

## Step 6: Reload & Test
1. Click the big green **"Reload"** button
2. Visit: `https://YOUR_USERNAME.pythonanywhere.com`
3. ✅ Your app is live!

---

## 📱 Share the Link
- Anyone can access: `https://YOUR_USERNAME.pythonanywhere.com`
- Phone, PC, anywhere - just need internet

---

## 🔐 Optional: Add Password Protection
If you want password protection, set environment variable:
1. Go to **Web tab**
2. Scroll to "Environment variables"
3. Add:
   - Name: `APP_PASSWORD`
   - Value: `your_secret_password`
4. Reload the app

---

## ⚠️ Important Notes:
- Free tier: your app sleeps after inactivity (wakes up on visit)
- Excel file saved in `/home/YOUR_USERNAME/supplier-collector/data/`
- Backup file: `backup.jsonl` keeps all submissions safe

---

## 🆘 Troubleshooting:
- **500 Error?** Check error logs in Web tab
- **Module not found?** Reinstall: `pip3.10 install --user flask openpyxl`
- **Files not found?** Check paths have YOUR actual username

---

## Need Help?
Check PythonAnywhere forums or contact support!
