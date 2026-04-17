# Troubleshooting Guide

## Docker Compose Errors

### "no configuration file provided: not found"
**Solution:** Make sure you're in the repo directory with `docker-compose.yml`:
```bash
cd video-platform-automation
docker compose build
```

The `name: video-platform-automation` in `docker-compose.yml` should fix this.

**Note:** There's one service (`pipeline`) but multiple containers. Each run creates a container named `video-pipeline-<channel-id>`. To see all containers:
```bash
docker compose ps
```

### "NVIDIA runtime not detected"

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

## Build/Runtime Errors

### "RuntimeError: operator torchvision::nms does not exist"
**Cause:** torchvision/transformers version incompatibility
**Solution:** Rebuild with updated image (already fixed in repo):
```bash
./run.sh --rebuild
```

This updates torchvision to 0.17.2 which is compatible with the transformers version.

### "No module named 'audiocraft'"
**Solution:** MusicGen installation failed. Rebuild:
```bash
./run.sh --rebuild
```

### "CUDA out of memory"
**Solution:** Your GPU doesn't have enough VRAM for the model:
- Stable Diffusion v1.5 needs ~4GB VRAM minimum
- MusicGen needs ~2GB VRAM minimum
- You have RTX 4070 (8GB) which should be sufficient

If still failing, try:
1. Close other GPU applications
2. Use smaller batch sizes (not exposed in current UI)
3. Run on CPU (much slower): `./run.sh --cpu`

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

**Warning:** CPU generation will be 10-100x slower than GPU.

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

## Docker Specific Issues

### "Failed to resolve Docker Compose project name"
**Solution:** Make sure `docker-compose.yml` is in the same directory as `run.sh`:
```bash
cd video-platform-automation
docker compose build
```

### Container exits immediately with no logs
**Solution:** The pipeline may have finished quickly (no prompt provided):
```bash
# Check if container exited
docker compose ps

# View logs
./run.sh --logs

# Run with prompt
./run.sh --niche music --prompt "your prompt here" --channel-id test1
```

### "Permission denied" on output files
**Solution:** The container creates files as root, so they're owned by root:
```bash
# Fix permissions
sudo chown -R $USER:$USER output/ config/ logs/
```

Or rebuild the container:
```bash
./run.sh --stop
./run.sh --niche music --prompt "chill forest" --channel-id test1
```
