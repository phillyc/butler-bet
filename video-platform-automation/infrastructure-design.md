# Infrastructure Design: Cattle vs Pets

## Guiding Principle

**Build once, deploy anywhere** - No local "pets". Every tool is containerized and composable.

## Requirements

1. **Single command startup** - `./build.sh` or `docker-compose up --build`
2. **Docker-native** - All tools in containers
3. **Stateless where possible** - Models cached, data persisted
4. **AWS-ready** - Same images run on ECS/EC2 without changes
5. **Multi-channel support** - Can run 10-20 instances independently

---

## Container Architecture

### Core Stack (All Containerized)

```
┌─────────────────────────────────────────────────────────────────┐
│                    video-platform-automation                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐   │
│  │   musicgen   │  │  stable-diff │  │        llm          │   │
│  │    (audio)   │  │     (image)  │  │     (text gen)      │   │
│  └──────────────┘  └──────────────┘  └─────────────────────┘   │
│         │                │                  │                   │
│         └────────────────┼──────────────────┘                   │
│                          │                                      │
│                   ┌──────▼──────┐                                │
│                   │   ffmpeg    │  (composing + encoding)       │
│                   │   (audio)   │                                │
│                   └─────────────┘                                │
│                          │                                      │
│                   ┌──────▼──────┐                                │
│                   │   youtube   │  (upload automation)          │
│                   │     api     │                                │
│                   └─────────────┘                                │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│                    Shared Volumes                                │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐   │
│  │   models/    │  │     output/  │  │       configs/      │   │
│  │ (cached)     │  │   (videos)   │  │   (API keys, etc)   │   │
│  └──────────────┘  └──────────────┘  └─────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Docker Compose Structure

### Option A: Monolith Container (Simplest)

All tools in one container, dependencies as pip packages

```yaml
version: '3.8'
services:
  video-pipeline:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - ./models:/app/models
      - ./output:/app/output
      - ./config:/app/config
    environment:
      - HUGGINGFACE_TOKEN=${HUGGINGFACE_TOKEN}
      - YOUTUBE_API_KEY=${YOUTUBE_API_KEY}
      - LLM_API_KEY=${LLM_API_KEY}
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

**Pros**: Simple, single container to manage  
**Cons**: Larger image, harder to swap individual tools

### Option B: Microservices (More Flexible)

Each tool in separate container, orchestrated together

```yaml
version: '3.8'
services:
  musicgen:
    build: ./services/musicgen
    volumes: [ ./models:/app/models ]
  
  stable-diffusion:
    build: ./services/sd
    volumes: [ ./models:/app/models ]
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
  
  llm:
    build: ./services/llm
    environment: [ LLM_API_KEY ]
  
  ffmpeg:
    image: ffmpeg:latest
  
  orchestrator:
    build: ./orchestrator
    depends_on: [ musicgen, stable-diffusion, llm, ffmpeg ]
    volumes:
      - ./models:/app/models
      - ./output:/app/output
```

**Pros**: Easy to swap tools, smaller images  
**Cons**: More complex orchestration

### Recommendation: Option A (Monolith for MVP)

Start with monolith, refactor to microservices if needed. The orchestration complexity is minimal.

---

## Dockerfile (Monolith Approach)

```dockerfile
FROM pytorch/pytorch:2.2.1-cuda12.1-cudnn8-runtime

# Install system deps
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Set environment defaults
ENV HF_HOME=/app/models
ENV TORCH_HOME=/app/models

# Health check
HEALTHCHECK --interval=30s --timeout=10s CMD python -c "import torch; print('OK')"

# Entry point
CMD ["python", "orchestrator/main.py"]
```

---

## Single Command Entry Points

### Local Development

```bash
# Build and run
./run.sh --niche music --prompt "wizards forest chill"

# Build without running
./build.sh

# Run existing container
./run.sh --existing pipeline-id
```

### AWS Deployment

```bash
# Same commands work!
./build.sh --aws
./run.sh --aws --niche storytime --prompt "roman empire facts"
```

### Parallel Execution (10-20 channels)

```bash
# Spin up 5 channels simultaneously
for i in {1..5}; do
  ./run.sh --niche music --prompt "wizards forest" --channel-id channel_$i &
done
wait
```

---

## Model Caching Strategy

### Problem
Large models (Stable Diffusion, MusicGen) need to be downloaded once, reused.

### Solution

```yaml
volumes:
  - ./models:/app/models  # Persist on host
  # OR for AWS:
  - model-cache:/app/models  # Named volume

# Dockerfile
RUN --mount=type=cache,target=/app/models \
    python -c "from diffusers import StableDiffusionPipeline; ..."
```

### AWS ECS/Fargate Strategy
- Use **EFS** for shared model cache
- OR mount model at container start (slow, but works)
- OR pre-build model into image (larger image, faster start)

---

## AWS Migration Path

### Same Docker Image, Different Deployment

| Local | AWS |
|-------|-----|
| `docker-compose up` | ECS Task Definition |
| `./models` volume | EFS mount or S3 |
| `localhost:8080` | Load balancer + container port |
| `docker network` | VPC + security groups |

### Fargate Task Definition (auto-generated)

```json
{
  "family": "video-pipeline",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "4096",
  "memory": "8192",
  "containerDefinitions": [{
    "name": "video-pipeline",
    "image": "phillyc/video-pipeline:latest",
    "portMappings": [],
    "environment": [
      {"name": "HUGGINGFACE_TOKEN", "valueFrom": "arn:aws:secretsmanager:..."}
    ],
    "mountPoints": [
      {"sourceVolume": "model-cache", "containerPath": "/app/models"}
    ]
  }],
  "volumes": [
    {"name": "model-cache", "efsVolumeConfiguration": {"filesystemId": "fs-..."}}
  ]
}
```

**Key insight**: Same `Dockerfile` and `docker-compose.yml` used locally and on AWS. Only deployment config changes.

---

## Multi-Channel Support

### Isolation Strategy

Each channel gets its own:
- Container instance
- Output directory
- Config file

```bash
./run.sh --channel wizard_chill
  ├─ output/wizard_chill/
  ├─ config/wizard_chill.yaml
  └─ container: video-pipeline-wizard-chill
```

### Orchestrator Script

```python
# orchestrator/main.py
def run_channel(channel_id, prompt, config):
    """Generate and upload one video for a channel."""
    output_dir = f"output/{channel_id}"
    config_file = f"config/{channel_id}.yaml"
    
    # Generate music
    music = musicgen.generate(prompt)
    
    # Generate thumbnail
    thumbnail = stable_diffusion.generate(prompt)
    
    # Animate + compose
    video = ffmpeg.compose(music, thumbnail)
    
    # Upload
    youtube.upload(video, config)
```

### Scaling to 20 Channels

```bash
# Use a job queue or simple parallelization
for channel in $(cat channels.txt); do
  ./run.sh --channel $channel &
done
```

---

## CI/CD for Automation

### GitHub Actions Workflow

```yaml
name: Build Pipeline

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: docker build -t video-pipeline:latest .
      
      - name: Push to ECR (AWS)
        run: |
          aws ecr get-login-password | docker login ...
          docker tag video-pipeline:latest my-ecr/video-pipeline:latest
          docker push my-ecr/video-pipeline:latest
```

**Result**: Every push builds and deploys the same image everywhere.

---

## Cost Optimization on AWS

### Fargate Spot Instances
- 70% cost reduction vs on-demand
- Acceptable for non-critical batch jobs
- Can survive interruptions (checkpoint output)

### Spot Fleet for 10-20 Channels
```bash
aws ec2 request-spot-instances \
  --spot-price 0.05 \
  --instance-count 20 \
  --launch-template LaunchTemplateId=lt-...
```

### Model Cache with EFS
- Shared across all channel instances
- Avoids re-downloading 5GB models per instance
- Cost: ~$0.10/GB/month

---

## Summary: Build Checklist

### Phase 1: Local Docker (Week 1)
- [ ] Dockerfile for monolith
- [ ] docker-compose.yml
- [ ] requirements.txt
- [ ] run.sh entry point
- [ ] Model caching setup

### Phase 2: AWS Migration (Week 2)
- [ ] ECR push pipeline
- [ ] ECS/Fargate task definition
- [ ] EFS for model cache
- [ ] Secrets Manager for API keys

### Phase 3: Multi-Channel (Week 3)
- [ ] Channel configuration system
- [ ] Parallel execution logic
- [ ] Output isolation
- [ ] Cost tracking per channel

---

## Next Steps

1. **Build the Dockerfile** - Get MusicGen + SDXL + FFmpeg in one container
2. **Write run.sh** - Single command to trigger a pipeline
3. **Test locally** - Ensure it works before AWS
4. **Document the pattern** - Same commands work on AWS

Want to start with the Dockerfile? I can draft it with:
- PyTorch base image (CUDA)
- MusicGen installation
- Stable Diffusion installation  
- FFmpeg
- Requirements pinned

Or should we write the orchestration script first and worry about Docker later?
