FROM pytorch/pytorch:2.2.1-cuda12.1-cudnn8-runtime

# ============================================
# Environment Variables
# ============================================
ENV DEBIAN_FRONTEND=noninteractive
ENV HF_HOME=/app/models
ENV TORCH_HOME=/app/models
ENV PYTHONUNBUFFERED=1

# ============================================
# System Dependencies
# ============================================
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    git \
    curl \
    wget \
    python3-pip \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# ============================================
# Python Dependencies
# ============================================
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ============================================
# Clone MusicGen (AudioCraft)
# ============================================
RUN git clone --depth 1 --branch v1.0.0 https://github.com/facebookresearch/audiocraft /app/audiocraft

# Install MusicGen from source
WORKDIR /app/audiocraft
RUN pip install --no-cache-dir -e .

# Return to app directory
WORKDIR /app

# ============================================
# Download Default Models (on first build)
# ============================================
# This ensures models are cached in the image
RUN python -c "from audiocraft.models import MusicGen; MusicGen.get_pretrained('melody_10s'); from huggingface_hub import hf_hub_download; hf_hub_download(repo_id='facebook/musicgen-small', filename='melody_10s.pt')" 2>/dev/null || true

RUN python -c "from diffusers import StableDiffusionPipeline; StableDiffusionPipeline.from_pretrained('runwayml/stable-diffusion-v1-5'); from huggingface_hub import hf_hub_download; hf_hub_download(repo_id='runwayml/stable-diffusion-v1-5', filename='v1-5-pruned-emaonly.ckpt')" 2>/dev/null || true

# ============================================
# Copy Application Code
# ============================================
COPY . .

# ============================================
# Create Directories
# ============================================
RUN mkdir -p /app/models /app/output /app/config /app/logs

# ============================================
# Health Check
# ============================================
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import torch; import torchvision; import diffusers; print('OK')" || exit 1

# ============================================
# Entry Point
# ============================================
CMD ["python", "orchestrator/main.py"]
