# Video Platform Automation Tools & Resources

A collection of tools, APIs, and documentation for automatically generating and publishing content to YouTube, Instagram, Facebook, TikTok, and other video platforms.

## Quick Start

### Tools & Libraries

#### Video Generation
- **Remotion** - React-based video generation (great for programmatic video creation)
- **MoviePy** - Python video editing library
- **FFmpeg** - Command-line video/audio processing
- **Manim** - Mathematical animation engine (3Blue1Brown's tool)
- **P5.js** - Creative coding for generative visuals
- **OpenCV** - Computer vision and video processing

#### Audio & Speech
- **Whisper** - OpenAI's speech-to-text model (for auto-captions, transcripts)
- **ElevenLabs** - AI voice synthesis
- **Coqui TTS** - Open-source text-to-speech
- **SoX** - Sound eXchange (audio processing)

#### Image & Graphics
- **Pillow** - Python imaging library
- **ImageMagick** - Image manipulation
- **GIMP/Photoshop scripts** - Batch image processing
- **Canva API** - Template-based design automation

#### Social Media APIs
- **YouTube Data API v3** - Upload, manage, analyze YouTube content
- **Instagram Graph API** - Instagram/Facebook content management
- **TikTok API** - Video upload and management (developer access required)
- **Facebook Graph API** - Cross-platform posting

### Automation Patterns

#### 1. Batch Video Processing
```bash
# Process multiple videos in parallel
find videos/ -name "*.mp4" -exec ffmpeg -i {} -vf scale=1280:720 output_{}.mp4 \;
```

#### 2. Auto-Caption Generation
```python
# Using Whisper for automatic captions
import whisper
model = whisper.load_model("base")
result = model.transcribe("video.mp4")
# Extract subtitles and save as SRT
```

#### 3. Cross-Platform Publishing
- Extract metadata from one platform
- Resize/crop for different aspect ratios (16:9, 9:16, 1:1)
- Schedule uploads via APIs
- Track performance across platforms

## Current Projects

### ASR for Poker Vlogs
- Auto-extract card calls from video audio
- Generate timing-synced captions
- Create searchable transcripts

### Batch Content Creation
- Template-driven video generation
- Automated thumbnail creation
- Multi-format export (YouTube, Shorts, Reels)

## Getting Started

### Prerequisites
- Python 3.9+
- FFmpeg installed
- Platform API credentials

### Installation
```bash
git clone https://github.com/phillyc/video-platform-automation.git
cd video-platform-automation
pip install -r requirements.txt
```

## Quick Start

### Local Development

```bash
# Clone repo
git clone https://github.com/phillyc/video-platform-automation.git
cd video-platform-automation

# Build Docker image (first time only)
docker compose build

# Run music playlist pipeline
./run.sh --niche music --prompt "wizards forest chill downtempo" --channel-id test1

# Monitor output
./run.sh --channel-id test1 --logs

# Try different niches
./run.sh --niche storytime --prompt "roman empire history sleep" --channel-id test2
```

### AWS Deployment

```bash
# Same Docker image, just different deployment
docker tag video-pipeline:latest <aws-ecr-url>.dkr.ecr.<region>.amazonaws.com/video-pipeline:latest
docker push <aws-ecr-url>.dkr.ecr.<region>.amazonaws.com/video-pipeline:latest

# Run on ECS/Fargate (see infrastructure-design.md)
aws ecs run-task --cluster video-pipeline --task-definition video-pipeline:1
```

### Environment Variables

Create a `.env` file:

```bash
HF_TOKEN=your_huggingface_token
YOUTUBE_API_KEY=your_youtube_api_key
LLM_API_KEY=your_llm_api_key
```

Or set directly:
```bash
export HF_TOKEN=...
export YOUTUBE_API_KEY=...
```

### Running Locally (No Docker)

```bash
# Install dependencies
pip install -r requirements.txt

# Run directly
python orchestrator/main.py --config config/default/config.yaml
```

## Contributing

Found a useful tool or have a project to add? Open a PR!

### Adding a Tool
1. Add to the relevant section above
2. Link to official documentation
3. Note any cost/usage limits
4. Mention alternatives if applicable

## Resources

- [YouTube API Docs](https://developers.google.com/youtube/v3)
- [Instagram Basic Display API](https://developers.facebook.com/docs/instagram-basic-display-api)
- [TikTok Developer Portal](https://developers.tiktok.com/)
- [Remotion Docs](https://docs.remotion.ai/)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)

## License

MIT - Feel free to use for personal and commercial projects.
