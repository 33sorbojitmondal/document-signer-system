@echo off
echo ============================================
echo  Document Signer System - GitHub Setup
echo ============================================
echo.
echo Step 1: Login to GitHub (browser will open)
gh auth login --hostname github.com --git-protocol https --web
echo.
echo Step 2: Create repository and push
gh repo create document-signer-system --public --source=. --remote=origin --push
echo.
echo Done! Repository URL:
gh repo view --web
pause
