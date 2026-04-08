# 🚀 Deployment Guide - Hugging Face Spaces

Complete step-by-step guide to deploy the Code Review Environment to Hugging Face Spaces.

## 📋 Pre-Deployment Checklist

Run the validation script first:
```bash
cd code-review-env
python validate_submission.py
```

✅ Ensure all checks pass before proceeding!

---

## 🔧 Step 1: Prepare Your Hugging Face Account

1. **Create/Login to Hugging Face Account**
   - Go to https://huggingface.co/
   - Sign up or log in

2. **Get Your Access Token**
   - Go to https://huggingface.co/settings/tokens
   - Click "New token"
   - Name it (e.g., "openenv-hackathon")
   - Select "write" permissions
   - Copy the token (you'll need this later)

---

## 🏗️ Step 2: Create a New Space

1. **Navigate to Spaces**
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"

2. **Configure Space Settings**
   - **Space name**: `code-review-env` (or your preferred name)
   - **License**: MIT
   - **Select SDK**: Choose "Gradio"
   - **Space hardware**: CPU basic (free tier is sufficient)
   - **Visibility**: Public (required for hackathon)
   - Click "Create Space"

---

## 📤 Step 3: Upload Files

### Option A: Using Git (Recommended)

```bash
# Clone your new space
git clone https://huggingface.co/spaces/YOUR_USERNAME/code-review-env
cd code-review-env

# Copy all files from your local code-review-env
cp -r /path/to/Meta-Hackathon/code-review-env/* .

# Add and commit
git add .
git commit -m "Initial commit: Code Review Intelligence Environment"

# Push to Hugging Face
git push
```

### Option B: Using Web Interface

1. Click "Files" tab in your Space
2. Click "Add file" → "Upload files"
3. Upload ALL files from `code-review-env/` directory:
   - ✅ inference.py
   - ✅ environment.py
   - ✅ models.py
   - ✅ openenv.yaml
   - ✅ app.py
   - ✅ Dockerfile
   - ✅ requirements.txt
   - ✅ README.md
   - ✅ graders/ (entire directory)
   - ✅ data/ (entire directory)
4. Commit the changes

---

## 🔐 Step 4: Configure Secrets

1. **Go to Space Settings**
   - Click "Settings" tab in your Space
   - Scroll to "Repository secrets"

2. **Add Required Secrets**
   
   **HF_TOKEN** (Required):
   - Name: `HF_TOKEN`
   - Value: Your Hugging Face token from Step 1
   - Click "Add"
   
   **API_BASE_URL** (Optional - has default):
   - Name: `API_BASE_URL`
   - Value: `https://api.openai.com/v1` (or your custom endpoint)
   - Click "Add"
   
   **MODEL_NAME** (Optional - has default):
   - Name: `MODEL_NAME`
   - Value: `gpt-4o-mini` (or your preferred model)
   - Click "Add"

---

## ⏳ Step 5: Wait for Build

1. **Monitor Build Progress**
   - Go to "Logs" tab
   - Watch the build process
   - This may take 5-10 minutes

2. **Build Status Indicators**
   - 🟡 Building: Space is being built
   - 🟢 Running: Space is live and ready
   - 🔴 Error: Check logs for issues

3. **Common Build Issues**
   - **Timeout**: Reduce dependencies or optimize Dockerfile
   - **Memory error**: Ensure code fits in 8GB RAM limit
   - **Import errors**: Check requirements.txt

---

## ✅ Step 6: Verify Deployment

### Test 1: Check Space is Running
```bash
curl https://YOUR_USERNAME-code-review-env.hf.space
```
Should return HTTP 200

### Test 2: Test the Gradio Interface
1. Open your Space URL in browser
2. Select a task from dropdown
3. Click "Run Demo"
4. Verify output appears

### Test 3: Test reset() Endpoint
The Gradio interface should load without errors, which confirms reset() works.

---

## 🎯 Step 7: Tag Your Space

1. **Add OpenEnv Tag**
   - Go to Space settings
   - Under "Tags", add: `openenv`
   - Save changes

2. **Add Additional Tags** (Optional)
   - `code-review`
   - `developer-tools`
   - `meta-hackathon`

---

## 📊 Step 8: Run Final Validation

### Local Validation
```bash
cd code-review-env
python validate_submission.py
```

### Test Inference Script Locally
```bash
# Set environment variables
export HF_TOKEN="your-token"
export API_BASE_URL="https://api.openai.com/v1"
export MODEL_NAME="gpt-4o-mini"

# Run inference
python inference.py
```

Expected output:
```
[START] task=bug_detection env=code-review model=gpt-4o-mini
[STEP] step=1 action=identify_bug(...) reward=0.01 done=false error=null
...
[END] success=true steps=10 rewards=0.01,0.01,...
```

---

## 🐳 Step 9: Test Docker Build (Optional but Recommended)

```bash
cd code-review-env

# Build Docker image
docker build -t code-review-env .

# Run container
docker run -p 7860:7860 \
  -e HF_TOKEN="your-token" \
  -e API_BASE_URL="https://api.openai.com/v1" \
  -e MODEL_NAME="gpt-4o-mini" \
  code-review-env

# Test in browser
# Open http://localhost:7860
```

---

## 📝 Step 10: Submit to Hackathon

1. **Verify All Requirements**
   - ✅ Space is "Running" (not building or stopped)
   - ✅ Space URL returns 200
   - ✅ Gradio interface loads
   - ✅ Tagged with `openenv`
   - ✅ All files uploaded
   - ✅ Secrets configured

2. **Get Your Space URL**
   - Format: `https://huggingface.co/spaces/YOUR_USERNAME/code-review-env`
   - Or: `https://YOUR_USERNAME-code-review-env.hf.space`

3. **Submit to Hackathon**
   - Use the Space URL in your submission
   - Include any additional documentation requested

---

## 🔧 Troubleshooting

### Space Won't Start
- Check logs for errors
- Verify all files are uploaded
- Ensure secrets are set correctly
- Check Dockerfile syntax

### Build Timeout
- Reduce dependencies in requirements.txt
- Optimize Docker build steps
- Use smaller base image

### Import Errors
- Verify all Python files are uploaded
- Check requirements.txt includes all dependencies
- Ensure file structure is correct

### Gradio Interface Not Loading
- Check app.py for errors
- Verify port 7860 is exposed in Dockerfile
- Check browser console for errors

### Inference Script Fails
- Verify HF_TOKEN is set
- Check API_BASE_URL is correct
- Ensure MODEL_NAME is valid
- Test locally first

---

## 📞 Support

If you encounter issues:

1. **Check Logs**: Space → Logs tab
2. **Review Documentation**: README.md
3. **Run Validation**: `python validate_submission.py`
4. **Test Locally**: Run Docker container locally
5. **Check Examples**: Review reference projects in guidelines

---

## ✅ Final Checklist

Before submitting, verify:

- [ ] Space is in "Running" state
- [ ] Space URL returns HTTP 200
- [ ] Gradio interface loads and works
- [ ] Tagged with `openenv`
- [ ] All secrets configured
- [ ] inference.py in root directory
- [ ] Docker builds successfully
- [ ] Local validation passes
- [ ] README is complete
- [ ] All 3 tasks work correctly

---

## 🎉 Success!

Your Code Review Intelligence Environment is now deployed and ready for submission!

**Space URL**: `https://huggingface.co/spaces/YOUR_USERNAME/code-review-env`

Good luck with the hackathon! 🚀
