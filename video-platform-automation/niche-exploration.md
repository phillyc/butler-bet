# YouTube Automation: Niche Exploration

## Goal
Build an AI pipeline for unsupervised long-form video generation and posting across multiple niches.

---

## Niche 1: 60-120 Minute Music Playlists

### Workflow
1. **Input Prompt**: "Friendly wizards in medieval forests ponder their orbs while darkness looms on the horizon. Chill, downtempo, hip hop."
2. **Music Generation/Collection**: Artlist.io or AI-generated
3. **Thumbnail Generation**: AI image generation with theme
4. **Thumbnail Animation**: Minor looping animation (30s-1m loop)
5. **Composition**: Layer music over animated thumbnail
6. **Metadata Generation**: Title, description, hashtags (LLM)
7. **Upload**: YouTube API

### Requirements Analysis

#### Music Sources
**Option A: AI-Generated Music**
- **Suno AI** - Can generate full tracks with prompts, commercial rights if paid
- **Udio** - Similar to Suno, high quality
- **Stable Audio** - Stable Diffusion's music model, shorter clips
- **AudioCraft (MusicGen)** - Open-source, run locally
- **Pros**: Unlimited scale, truly automated
- **Cons**: Quality varies, commercial licensing concerns

**Option B: Stock Music**
- **Artlist.io** - License library, not AI-generated
- **Epidemic Sound** - Similar, YouTube integration
- **Pros**: High quality, clear licensing
- **Cons**: Manual curation needed, limited automation

**Option C: Hybrid**
- Use AI for unique tracks + stock for filler
- Build local library of "vibe packs"

#### Thumbnail Animation
**Tools to explore:**
- **Remotion** - React-based, can create looping animations
- **FFmpeg** - Can loop still images, add subtle zooms/pans
- **Manim** - More for mathematical, but can do simple animations
- **P5.js** - Generative visuals, export to video
- **Stable Video Diffusion** - AI video generation (might be overkill)
- **Runway Gen-2** - AI video, expensive
- **Leonardo AI** - Has motion features

**Recommended approach**: FFmpeg-based simple animations (zoom, pan, overlay particles) + looping

#### Technical Stack
```
Prompt → [MusicGen/Suno] → Generate Music
     → [Stable Diffusion] → Generate Thumbnail
     → [Remotion/FFmpeg] → Animate Thumbnail
     → [FFmpeg] → Composite (audio + video)
     → [LLM] → Generate Title/Description/Tags
     → [YouTube API] → Upload
```

---

## Niche 2: Sleepy Storytime

### Workflow
1. **Input Theme**: "History lessons from the Roman Empire to fall asleep to"
2. **Script Generation**: LLM writes engaging, calm narrative
3. **TTS**: Text-to-speech with calming voice
4. **Background Music**: Chill ambient music
5. **Visuals**: Sleepy thumbnail/looping animation
6. **Composition**: Audio + visuals
7. **Upload**: YouTube API

### Requirements Analysis

#### Script Generation
- **LLM**: Claude or GPT for narrative generation
- **Style guidelines**: Calm, repetitive pacing, no sudden jumps
- **Length control**: Need ~30-60 min scripts
- **Research**: Can pull from Wikipedia/APIs for accuracy

#### TTS Options
**High-quality paid:**
- **ElevenLabs** - Best quality, commercial rights, multiple voices
- **Play.ht** - Good alternative
- **Resemble AI** - Custom voice cloning

**Open-source/local:**
- **Coqui TTS** - Good quality, runs locally
- **Piper** - Fast, lightweight
- **XTTS** - ElevenLabs-style, open weights

**Pros/Cons**: ElevenLabs is expensive at scale but high quality. Coqui/Piper are free but lower quality.

#### Background Music
Same options as Niche 1, but need:
- Ambient/chill music
- Loopable tracks
- No vocals/lyrics (or very minimal)

#### Visuals
- Similar to Niche 1: looping thumbnails
- Can use darker, moodier imagery
- Sleepy themes: stars, forests, cozy rooms

#### Technical Stack
```
Theme → [LLM] → Generate Script (calm tone)
      → [ElevenLabs/Coqui] → TTS Audio
      → [MusicGen/Suno] → Background Music
      → [SD/Remotion] → Visual Loop
      → [FFmpeg] → Composite
      → [YouTube API] → Upload
```

---

## Niche 3: Animated Podcasts

### Workflow
1. **Topic Mining**: News, research papers, trending topics
2. **Script/Audio Generation**: Two-speaker podcast format
3. **Character Generation**: AI avatars (dogs, people, etc.)
4. **Animation**: Lip-sync, expressions
5. **Upload**: YouTube API

### Requirements Analysis

#### Audio Generation
**Google's AI Podcast Tool**: Need to find/experiment
- **ElevenLabs** - Can generate two distinct voices in conversation
- **Play.ht** - Multi-speaker conversations
- **Custom solution**: Generate dialogue script + two TTS passes + splice

**Script Generation**:
- LLM creates natural dialogue format
- Topic sourcing: Reddit API, News API, ArXiv API, Wikipedia

#### Animation
**Tools to explore:**
- **D-ID** - Talking head avatars, lip-sync
- **HeyGen** - Similar, professional quality
- **SadTalker** - Open-source, less polished
- **Wav2Lip** - Lip-sync on any video
- **Seedance 2** - User mentioned, need to research
- **Nano Banana** - User mentioned, need to research
- **Runway** - More general AI video
- **Kaiber** - Style transfer, animation

**Recommendation**: Start with D-ID or HeyGen for talking heads, or SadTalker + Wav2Lip for open-source

#### Character Generation
- **Stable Diffusion** - Generate character images
- **Character consistency** - Need LoRA or consistent prompts
- **Multiple characters** - Maintain visual consistency across episodes

#### Technical Stack
```
Topic → [LLM] → Generate Dialogue Script
      → [ElevenLabs] → Generate Two Voice Tracks
      → [Stable Diffusion] → Generate Character Images
      → [D-ID/SadTalker] → Lip-sync Animation
      → [FFmpeg] → Composite Audio/Video
      → [YouTube API] → Upload
```

---

## Monetization Comparison

### YouTube
- **YouTube Partner Program**: 1,000 subs + 4,000 watch hours (or 10M Shorts views)
- **CPM**: $2-10 RPM depending on niche
- **Music playlists**: Lower CPM (music-heavy), but high watch time potential
- **Storytime**: Medium CPM, good for evergreen content
- **Podcasts**: Higher CPM if educational/entertainment
- **Pros**: Established, reliable
- **Cons**: 50% of ad revenue to YouTube, strict duplicate content policies

### Facebook/Instagram
- **In-Stream Ads**: 1,000 followers + 60k min view minutes (90 days)
- **CPM**: Generally lower than YouTube
- **Reels Play Bonus**: Varies, currently more generous for Reels
- **Pros**: Cross-posting from YouTube easy
- **Cons**: More volatile algorithm, lower RPM

### TikTok
- **Creativity Program Beta**: 10k followers + 100k views (30 days)
- **CPM**: Very variable, currently 0.5-2 RPM
- **Pros**: Fast growth potential
- **Cons**: Very low RPM, content needs to be 1+ min

### Conclusion
**Start with YouTube** - Most reliable monetization. Facebook/IG are easy add-ons via cross-posting. TikTok if Shorts format works.

---

## MVP Approach

### Phase 1: Test All Three Niches (Weeks 1-4)
**Goal**: Find which niche performs best with minimal tool investment

**Week 1-2**: Build basic pipeline for Niche 1 (music playlists)
- Easiest to automate
- Lowest production complexity
- Test with 3-5 videos

**Week 3**: Test Niche 2 (storytime)
- Requires better TTS
- Script generation complexity

**Week 4**: Test Niche 3 (podcasts)
- Most complex
- Requires animation tools

### Phase 2: Double Down (Weeks 5-8)
- Focus on winning niche
- Optimize pipeline
- Increase output frequency

### Phase 3: Scale (Weeks 9+)
- Parallelize video generation
- Add more channels (FB/IG/TikTok)
- Experiment with batch production

---

## Tool Investment Priority

### Must-Have (Immediate)
1. **FFmpeg** - Video/audio compositing
2. **YouTube API** - Upload automation
3. **LLM access** - Script/metadata generation
4. **Stable Diffusion** - Thumbnail generation
5. **Music generation** - Suno/Udio/MusicGen

### Nice-to-Have (Phase 2)
1. **ElevenLabs** - Premium TTS
2. **D-ID/HeyGen** - Podcast animation
3. **Remotion** - Professional video composition
4. **Artlist/Epidemic** - Stock music (if AI fails)

---

## Next Steps

1. **Research music tools** - Suno vs Udio vs MusicGen
2. **Test TTS quality** - ElevenLabs vs Coqui
3. **Explore animation** - D-ID free tier, SadTalker local
4. **Build skeleton pipeline** - FFmpeg + YouTube API
5. **Generate 3 test videos** - One per niche
6. **Upload and monitor** - 2 weeks, track CTR/watch time

Let's start documenting what we learn.
