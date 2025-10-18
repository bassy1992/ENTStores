# 🚀 Railway Media URL Preservation Solution

## 🔍 **The Problem**
Railway doesn't have persistent file storage, so when you redeploy:
- Local media files get deleted
- Database might reset
- Your Digital Ocean/Unsplash URLs get lost

## ✅ **The Solution**
I've created several scripts to preserve your media URLs across Railway deployments.

## 🛠️ **Quick Fix (Use This Now)**

### Step 1: Backup Your Current URLs
```bash
python backup_restore_media_urls.py backup
```
This creates a backup file with all your current media URLs.

### Step 2: After Railway Deployment
```bash
python backup_restore_media_urls.py restore
```
This restores all your media URLs from the backup.

## 🔄 **Automated Solution**

### Option A: Environment Variables (Recommended)
```bash
# Set up environment variables in Railway
python set_railway_media_env_vars.py

# After deployment, restore from environment variables
python restore_from_railway_env.py
```

### Option B: Full Deployment Script
```bash
# Complete deployment with automatic backup/restore
python railway_deploy_with_media_backup.py
```

## 📋 **Current Status**
Your database currently has:
- ✅ **11 products** with image URLs
- ✅ **8 product images** with URLs
- ⚠️ **0 categories** with image URLs

Sample URLs found:
- Slim Fit Denim Jeans: `https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=400&fit=crop`
- Premium Pullover Hoodie: `https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400&h=400&fit=crop`
- Classic Cotton T-Shirt: `https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop`

## 🎯 **Recommended Workflow**

### Before Each Deployment:
1. **Backup URLs**: `python backup_restore_media_urls.py backup`
2. **Deploy**: `railway up`
3. **Restore URLs**: `python backup_restore_media_urls.py restore`

### One-Time Setup (Better):
1. **Set Environment Variables**: `python set_railway_media_env_vars.py`
2. **Deploy**: `railway up`
3. **Auto-Restore**: `python restore_from_railway_env.py`

## 🔧 **Files Created**

| File | Purpose |
|------|---------|
| `backup_restore_media_urls.py` | Main backup/restore script |
| `set_railway_media_env_vars.py` | Set URLs as environment variables |
| `restore_from_railway_env.py` | Restore from environment variables |
| `railway_deploy_with_media_backup.py` | Complete deployment solution |
| `media_urls_backup_*.json` | Backup files (keep these safe!) |

## 🚨 **Important Notes**

1. **Keep Backup Files**: Always keep your `media_urls_backup_*.json` files safe
2. **Environment Variables**: Railway environment variables persist across deployments
3. **Database**: Make sure your Railway database is persistent (PostgreSQL)
4. **URLs**: Your URLs are from Unsplash, not Digital Ocean (which is fine!)

## 🔗 **Quick Commands**

```bash
# Check current status
python backup_restore_media_urls.py check

# Test if URLs are working
python backup_restore_media_urls.py test

# Backup before deployment
python backup_restore_media_urls.py backup

# Restore after deployment
python backup_restore_media_urls.py restore
```

## 💡 **Pro Tips**

1. **Automate**: Add the restore script to your Railway deployment process
2. **Monitor**: Check your URLs after each deployment
3. **Backup**: Keep multiple backup files for safety
4. **Environment**: Use Railway environment variables for permanent storage

## 🆘 **If URLs Are Already Lost**

If you've already lost your URLs after a deployment:
1. Check if you have any backup files: `ls media_urls_backup_*.json`
2. If yes, restore: `python backup_restore_media_urls.py restore --file [backup_file]`
3. If no backups, you'll need to re-add the URLs manually through Django admin

## 🎉 **Next Steps**

1. **Immediate**: Run `python backup_restore_media_urls.py backup` now
2. **Setup**: Run `python set_railway_media_env_vars.py` for permanent solution
3. **Deploy**: Test the workflow with your next deployment
4. **Monitor**: Check that URLs are preserved after deployment