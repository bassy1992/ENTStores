@echo off

REM Deploy production data to Railway
echo 🚀 Deploying to Railway with production data...

REM Commit the changes
git add .
git commit -m "Add production data deployment script"

REM Push to Railway
echo 📤 Pushing to Railway...
git push origin main

echo ✅ Deployment initiated! Check Railway dashboard for progress.
echo 🌐 Your app will be available at: https://entstores-production.up.railway.app/
echo 🔧 Admin panel: https://entstores-production.up.railway.app/admin/

pause