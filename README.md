# Document Signer System

Enterprise-Grade Secure Digital Signature Solution for MAKAUT CS781 Project II (Final Year).

## Overview

A full-stack web application that enables users to digitally sign and verify documents using RSA-2048 cryptographic algorithms. The system ensures document authenticity, integrity, and tamper detection.

**Prepared by:**
- RAHUL PANJA (18700122011)
- SK SAHIL AKTAR (18700122093)

**Under the guidance of:** Prof. Argha Kusum Das  
**Institution:** Techno International New Town, Department of Computer Science & Engineering

## Features

- User registration and authentication with automatic RSA key pair generation
- Document upload and secure storage
- RSA-2048 digital signature generation using PSS padding with SHA-256
- Real-time signature verification and tamper detection
- Dark-themed modern web interface
- Document status tracking (Uploaded, Signed, Verified, Tampered)

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11, Django 4.2 |
| Cryptography | cryptography library (RSA-2048-PSS-SHA256) |
| Database | SQLite (configurable to MySQL) |
| Frontend | HTML5, CSS3, Bootstrap 5 |
| Architecture | Layered MVC Pattern |

## Quick Start

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Installation

```bash
cd document-signer-system
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open your browser and navigate to **http://127.0.0.1:8000/**

### Usage

1. **Register** a new account (RSA key pair is generated automatically)
2. **Login** with your credentials
3. **Upload** a document from the dashboard
4. **Sign** the document using your private RSA key
5. **Verify** the signature to confirm authenticity and detect tampering

## Project Structure

```
document-signer-system/
├── document_signer/     # Django project settings
├── signer/              # Main application
│   ├── crypto_utils.py  # RSA signing & verification logic
│   ├── models.py        # UserProfile, Document, DigitalSignature
│   ├── views.py         # Controller layer
│   └── forms.py         # Form definitions
├── templates/signer/    # View layer (HTML templates)
├── static/css/          # Stylesheets
├── media/documents/     # Uploaded files
├── PROJECT_REPORT.md    # Academic project report
└── requirements.txt
```

## System Workflow

```
Login → Upload Document → Generate Signature → Verify Signature
```

## Security

- RSA-2048 key pairs generated per user at registration
- SHA-256 hashing for document integrity
- RSA-PSS padding for signature generation
- Tamper detection via hash comparison
- Django session-based authentication

## Deployment

### GitHub
Repository: https://github.com/33sorbojitmondal/document-signer-system

### Vercel (Live Demo)
The app is deployed on Vercel. Set these environment variables in the Vercel dashboard:

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Random Django secret key |
| `DEBUG` | `False` for production |
| `DATABASE_URL` | PostgreSQL connection string (use [Neon](https://neon.tech) free tier) |
| `ALLOWED_HOSTS` | `your-app.vercel.app,.vercel.app` |
| `CSRF_TRUSTED_ORIGINS` | `https://your-app.vercel.app` |

**Note:** Vercel requires PostgreSQL because the serverless filesystem is ephemeral. Document files are stored in the database.

### Deploy to Vercel

```bash
npm i -g vercel
vercel login
vercel --prod
```
