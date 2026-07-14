@echo off
echo ============================================
echo  Document Signer System - Vercel Deploy
echo ============================================
echo.
echo Step 1: Login to Vercel
call vercel login
echo.
echo Step 2: Deploy to production
call vercel --prod
echo.
echo IMPORTANT: Add these environment variables in Vercel Dashboard:
echo   SECRET_KEY      = (generate a random 50-char string)
echo   DEBUG           = False
echo   DATABASE_URL    = (PostgreSQL from neon.tech - free tier)
echo   ALLOWED_HOSTS   = your-app.vercel.app,.vercel.app
echo   CSRF_TRUSTED_ORIGINS = https://your-app.vercel.app
echo.
echo Get free PostgreSQL at: https://neon.tech
pause
