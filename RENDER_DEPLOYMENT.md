# 🚀 Deploy StaffView to Render

**Easy deployment with automatic HTTPS and free tier!**

---

## 📋 Prerequisites

- [x] GitHub account
- [x] Render account (sign up at https://render.com - FREE)
- [ ] StaffView code pushed to GitHub

---

## Step 1: Push to GitHub

If you haven't already pushed your code to GitHub:

```bash
cd "/Users/yeltsinz/UniqueProjects/Gandalf regression reports"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Deploy StaffView to Render"

# Create a new repo on GitHub, then:
git remote add origin https://github.com/YOUR-USERNAME/staffview.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy on Render

### Option A: One-Click Deploy with render.yaml (Recommended)

1. **Go to Render Dashboard:**
   - Visit: https://dashboard.render.com
   - Sign in with GitHub

2. **Create New Service:**
   - Click **"New +"** button
   - Select **"Web Service"**

3. **Connect Repository:**
   - Click **"Connect a repository"**
   - Authorize Render to access your GitHub
   - Select your **staffview** repository

4. **Configure (Auto-detected from render.yaml):**
   - Render will detect the `render.yaml` file
   - Click **"Apply"**
   - Review settings:
     - **Name:** staffview
     - **Region:** Oregon (or choose closest)
     - **Branch:** main
     - **Environment:** Docker
     - **Plan:** Free

5. **Deploy:**
   - Click **"Create Web Service"**
   - Render will:
     - Build your Docker image
     - Deploy the container
     - Assign a public URL
     - Set up automatic HTTPS

6. **Wait for Deployment:**
   - Watch the build logs
   - Takes ~3-5 minutes
   - Status will change to "Live" when ready

7. **Get Your URL:**
   - You'll see: `https://staffview.onrender.com`
   - Or: `https://staffview-XXXX.onrender.com`
   - **Share this URL with your team!**

### Option B: Manual Configuration

If render.yaml isn't auto-detected:

1. **After connecting repository:**
   - **Name:** staffview
   - **Region:** Oregon (or nearest)
   - **Branch:** main
   - **Root Directory:** (leave blank)
   - **Environment:** Docker
   - **Dockerfile Path:** ./Dockerfile

2. **Instance Type:**
   - Select **"Free"** (or paid if needed)

3. **Advanced Settings:**
   - Add environment variable:
     - Key: `FLASK_ENV`
     - Value: `production`
   - Health Check Path: `/`
   - Port: `5001`

4. **Create Web Service**

---

## Step 3: Verify Deployment

Once deployment is complete:

1. **Click the URL** (looks like `https://staffview.onrender.com`)

2. **You should see:**
   - ⚡ StaffView header
   - Welcome message
   - Upload area
   - Features section

3. **Test functionality:**
   - Try uploading an artifact
   - Check comparison view
   - Verify all features work

---

## 🌐 Share with Your Team

Your StaffView is now live at:
```
https://staffview.onrender.com
```
(or whatever URL Render assigns)

**Share this URL with your team members - they can access it from anywhere!**

---

## 🔧 Managing Your Deployment

### View Logs
1. Go to Render Dashboard
2. Click on your **staffview** service
3. Click **"Logs"** tab
4. View real-time application logs

### Redeploy (After Code Changes)
```bash
# Make changes to your code
git add .
git commit -m "Update feature"
git push origin main

# Render automatically redeploys! 🎉
```

### Manual Deploy
1. Go to Render Dashboard
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

### Environment Variables
1. Go to **"Environment"** tab
2. Click **"Add Environment Variable"**
3. Add variables like:
   - `SECRET_KEY`: your-secret-key
   - `MAX_UPLOAD_SIZE`: 104857600

### Custom Domain
1. Go to **"Settings"** tab
2. Scroll to **"Custom Domain"**
3. Add your domain (e.g., staffview.yourcompany.com)
4. Update DNS records as instructed

---

## 💡 Important Notes

### Free Tier Limitations
- ✅ **Free HTTPS** included
- ✅ **Automatic deployments** from GitHub
- ⚠️ **Spins down after 15 min of inactivity**
- ⚠️ **First request after spin-down takes ~30 seconds**
- ⚠️ **750 hours/month** (plenty for most use cases)

**Upgrade to paid plan (~$7/month) if you need:**
- Always-on service (no spin down)
- More resources
- Faster performance

### Persistent Storage
- Uploaded artifacts are stored in the container
- ⚠️ **Container storage is ephemeral** (lost on restart)
- For production, consider:
  - Using Render's persistent disks ($1/GB/month)
  - External storage (AWS S3, Google Cloud Storage)

### Updating Configuration
After changing `render.yaml`:
```bash
git add render.yaml
git commit -m "Update Render config"
git push origin main
# Render auto-deploys with new config
```

---

## 🐛 Troubleshooting

### Build Fails
**Check logs in Render Dashboard:**
- Look for missing dependencies
- Verify Dockerfile syntax
- Check if all files are committed to Git

**Common issues:**
```bash
# Make sure these files exist:
- Dockerfile
- requirements.txt
- app.py
- templates/

# Verify Dockerfile builds locally:
docker build -t staffview-test .
```

### App Won't Start
1. Check **Logs** tab in Render
2. Common issues:
   - Port configuration (ensure it's 5001)
   - Missing environment variables
   - Python dependencies

### Slow Initial Load (Free Tier)
- This is normal - free tier spins down
- Upgrade to paid plan for always-on service
- Or use a uptime monitoring service to ping it every 10 minutes

### Upload Fails
- Check file size (default limit: 100MB)
- Verify disk space isn't full
- Check logs for specific errors

---

## 📊 Monitoring

### Health Checks
Render automatically monitors:
- HTTP health checks every 30 seconds
- Restarts service if unhealthy
- Email notifications for failures

### View Metrics
1. Go to **"Metrics"** tab
2. See:
   - CPU usage
   - Memory usage
   - Request count
   - Response times

---

## 🔐 Security Best Practices

1. **Set SECRET_KEY:**
   ```
   Environment → Add Variable
   Key: SECRET_KEY
   Value: generate-a-random-secret-key-here
   ```

2. **HTTPS:**
   - ✅ Automatically enabled by Render
   - ✅ Free SSL certificate

3. **Environment Variables:**
   - Never commit secrets to Git
   - Use Render's environment variables

4. **Access Control:**
   - Consider adding authentication
   - Use Render's IP whitelisting if needed

---

## 💰 Cost

### Free Tier (Recommended to Start)
- **Cost:** $0/month
- **Perfect for:** Team testing, internal tools
- **Limitations:** Spins down after inactivity

### Paid Plan (For Production)
- **Cost:** ~$7/month
- **Benefits:**
  - Always-on
  - More resources
  - Priority support
  - No spin-down

---

## 🎉 Success!

Once deployed, your team can access StaffView at:

**https://staffview.onrender.com**

Features available:
- ✅ Upload artifacts from anywhere
- ✅ Compare regressions in real-time
- ✅ Automatic HTTPS security
- ✅ No maintenance needed
- ✅ Automatic updates from Git

---

## 📞 Support

- **Render Docs:** https://render.com/docs
- **Community Forum:** https://community.render.com
- **Status Page:** https://status.render.com

---

## 🚀 Next Steps

1. Push code to GitHub
2. Deploy on Render
3. Share URL with team
4. Start comparing regressions!

**Let's get StaffView live!** ⚡

---

*Last updated: October 31, 2025*

