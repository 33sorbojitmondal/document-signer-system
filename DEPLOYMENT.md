# Deployment Guide

## Prerequisites

- Git installed
- GitHub CLI (`gh`) installed
- Vercel CLI (`npm i -g vercel@latest`)
- Node.js 18+

---

## Step 1: Push to GitHub

Open terminal in the project folder and run:

```bash
# Login to GitHub (opens browser)
gh auth login

# Create repo and push (one command)
gh repo create document-signer-system --public --source=. --remote=origin --push
```

**Or use the script:**
```bash
scripts\setup-github.bat
```

Your repo will be at:
`https://github.com/YOUR_USERNAME/document-signer-system`

---

## Step 2: Set Up PostgreSQL (Required for Vercel)

Vercel serverless cannot use SQLite. Use free PostgreSQL from Neon:

1. Go to [https://neon.tech](https://neon.tech) and create a free account
2. Create a new project/database
3. Copy the **connection string** (starts with `postgresql://`)

---

## Step 3: Deploy to Vercel

```bash
# Login to Vercel (opens browser)
vercel login

# Deploy to production
vercel --prod
```

**Or use the script:**
```bash
scripts\deploy-vercel.bat
```

---

## Step 4: Add Environment Variables in Vercel

Go to **Vercel Dashboard → Your Project → Settings → Environment Variables**

Add these:

| Variable | Value | Example |
|----------|-------|---------|
| `SECRET_KEY` | Random 50-char string | `django-secret-key-change-this-abc123xyz` |
| `DEBUG` | `False` | `False` |
| `DATABASE_URL` | Neon PostgreSQL URL | `postgresql://user:pass@host/db?sslmode=require` |
| `ALLOWED_HOSTS` | Your Vercel domain | `document-signer-system.vercel.app,.vercel.app` |
| `CSRF_TRUSTED_ORIGINS` | HTTPS origin | `https://document-signer-system.vercel.app` |

After adding variables, **redeploy** from Vercel dashboard or run `vercel --prod` again.

---

## Step 5: Run Database Migrations

After first deploy with DATABASE_URL set, migrations run automatically via `build.sh`.

To run manually:
```bash
vercel env pull .env.local
# Set DATABASE_URL locally, then:
python manage.py migrate
```

---

## Connect GitHub to Vercel (Auto-Deploy)

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your GitHub repository `document-signer-system`
3. Framework Preset: **Other**
4. Build Command: `bash build.sh`
5. Add environment variables from Step 4
6. Click **Deploy**

Future pushes to GitHub will auto-deploy to Vercel.

---

## Local Development

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Uses SQLite locally (no DATABASE_URL needed).

---

## Project URLs

| Service | URL |
|---------|-----|
| GitHub | `https://github.com/YOUR_USERNAME/document-signer-system` |
| Vercel Live | `https://document-signer-system.vercel.app` (after deploy) |
| Local | `http://127.0.0.1:8000` |
