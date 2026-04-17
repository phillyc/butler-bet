# Troubleshooting Guide

## Docker Compose Errors

### "no configuration file provided: not found"
**Solution:** Make sure you're in the repo directory with `docker-compose.yml`:
```bash
cd video-platform-automation
docker compose build
```

The `name: video-platform-automation` in `docker-compose.yml` should fix this.
**Solution:** Install NVIDIA Container Toolkit:

**Ubuntu/Debian:**
```bash
# Add NVIDIA repository
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# Install
sudo apt update
sudo apt install nvidia-container-toolkit

# Restart Docker
sudo systemctl restart docker

# Verify
docker info | grep nvidia
```

**Windows (Docker Desktop):**
- NVIDIA Container Toolkit is included
- Make sure "Use NVIDIA GPU" is enabled in Docker Desktop settings

### "Cannot connect to the Docker daemon"
**Solution:** Start Docker:
```bash
# Linux
sudo systemctl start docker

# macOS/Windows
# Start Docker Desktop app
```

## Build Errors

### "CUDA version mismatch"
**Solution:** Your GPU is RTX 4070 (Compute Capability 8.9), which supports CUDA 12.1. The Dockerfile uses `pytorch/pytorch:2.2.1-cuda12.1-cudnn8-runtime` which is correct.

If you get CUDA errors, update your NVIDIA drivers:
```bash
sudo apt install nvidia-driver-550
```

### "Out of memory building image"
**Solution:** Allocate more memory to Docker:
- Docker Desktop → Settings → Resources → Memory (set to 8GB+)
- Or build with less model caching

## Runtime Errors

### "No module named 'audiocraft'"
**Solution:** MusicGen installation failed. Rebuild:
```bash
./run.sh --rebuild
```

### "No GPU available, falling back to CPU"
**Solution:** See "NVIDIA runtime not detected" above. Without GPU, builds will be 10-100x slower.

### "YouTube API authentication failed"
**Solution:** You need OAuth credentials:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project
3. Enable YouTube Data API v3
4. Create OAuth 2.0 credentials (Desktop app)
5. Download `credentials.json` to repo root
6. Run pipeline once to generate token

## GPU on Laptop (RTX 4070)

Your RTX 4070 laptop GPU **will work** with this setup. The issue is usually:
1. Docker not finding the GPU (needs NVIDIA Container Toolkit)
2. Outdated NVIDIA drivers (update to 550+)
3. Docker Desktop not enabled for GPU

**Quick check:**
```bash
nvidia-smi
# Should show your RTX 4070

docker info | grep nvidia
# Should show "NVIDIA" in output
```

## Alternative: CPU Mode

If GPU isn't working, run in CPU mode (much slower but functional):
```bash
./run.sh --cpu --niche music --prompt "chill forest"
```

## Environment Variables

Create a `.env` file in the repo root:
```bash
HF_TOKEN=your_huggingface_token
YOUTUBE_API_KEY=your_youtube_api_key
LLM_API_KEY=your_llm_api_key
```

Then just run:
```bash
./run.sh --niche music --prompt "chill forest"
```
