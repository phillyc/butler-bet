# Unit Economics & Cost Tracking

## Critical Assumption

**CMR Benchmark**: $3 CPM (cost per mille = per 1,000 views)
- Conservative estimate for crowded niches
- Higher CPM possible in educational/finance, lower in music/chill
- Track actuals per video, adjust projections

## Break-Even Analysis

### Formula
```
Break-Even Views = Production Cost / CPM × 1,000
Revenue = Views × CPM / 1,000
```

### At $3 CPM with $10 Production Cost
```
Break-Even Views = 10 / 3 × 1,000 = 3,333 views
```
**Minimum required per video**: ~3,500 views to break even

### Reality Check
YouTube revenue isn't instant. A video might get:
- Week 1: 500 views → $1.50
- Week 4: 2,000 views → $6.00
- Month 3: 10,000 views → $30.00

**Key insight**: Need ~3,333 cumulative views over time to break even on a $10 video

---

## Niche-Specific Cost Analysis

### Niche 1: Music Playlists

#### Cost Breakdown (Optimized)
| Component | Low-Cost Option | Cost | Premium Option | Cost |
|-----------|----------------|------|----------------|------|
| **Music** | MusicGen (local) | $0 | Suno (paid) | $10-30/mo |
| **Thumbnail** | SDXL (local) | $0 | Midjourney | $10-30/mo |
| **Animation** | FFmpeg (local) | $0 | Remotion | $0 |
| **Metadata** | LLM (free tier) | $0 | Claude/GPT | $5-20/mo |
| **Infrastructure** | Local GPU | $0 | AWS/Cloud | $5-20/mo |
| **YouTube API** | Free | $0 | Free | $0 |
| **Total** | | **~$0-50/mo** | | **~$25-100/mo** |

#### Per-Video Cost at Scale
- **Free stack**: ~$0.50-2.00 (electricity, cloud storage)
- **Premium stack**: ~$2-5 (API calls, subscriptions)

#### Volume Needed for Profit
| Cost/Video | Views for BE | Profit per 10k views |
|------------|--------------|---------------------|
| $0.50 | 167 views | $29.50 |
| $2.00 | 667 views | $28.00 |
| $5.00 | 1,667 views | $25.00 |

**Verdict**: **Best economics** - can run locally, near-zero marginal cost per video

---

### Niche 2: Sleepy Storytime

#### Cost Breakdown
| Component | Low-Cost Option | Cost | Premium Option | Cost |
|-----------|----------------|------|----------------|------|
| **Script** | LLM (free tier) | $0 | Claude 3.5 | $5/video |
| **TTS** | Coqui/Piper (local) | $0 | ElevenLabs | $5-15/video |
| **Music** | MusicGen (local) | $0 | Suno | $1-5/video |
| **Thumbnail** | SDXL (local) | $0 | Midjourney | $0.20-1/video |
| **Animation** | FFmpeg | $0 | Remotion | $0 |
| **Infrastructure** | Local GPU | $0 | Cloud GPU | $1-3/video |
| **YouTube API** | Free | $0 | Free | $0 |
| **Total** | | **~$0-2/video** | | **~$12-25/video** |

#### Per-Video Cost at Scale
- **Free stack**: ~$1-3 (cloud GPU, storage)
- **Premium stack**: ~$15-30 (ElevenLabs, high-quality TTS)

#### Volume Needed for Profit
| Cost/Video | Views for BE | Profit per 10k views |
|------------|--------------|---------------------|
| $1.00 | 333 views | $29.00 |
| $3.00 | 1,000 views | $27.00 |
| $15.00 | 5,000 views | $15.00 |
| $25.00 | 8,333 views | $5.00 |

**Verdict**: **Breakable at scale** - need ~5k views/video to profit with premium TTS

**Key risk**: ElevenLabs at $15/video means we need strong performance to justify

---

### Niche 3: Animated Podcasts

#### Cost Breakdown
| Component | Low-Cost Option | Cost | Premium Option | Cost |
|-----------|----------------|------|----------------|------|
| **Script** | LLM (free tier) | $0 | Claude | $2-5/video |
| **Audio** | ElevenLabs (2 voices) | $10-20/video | Custom | $5-10/video |
| **Animation** | SadTalker (local) | $0 | D-ID/HeyGen | $20-50/video |
| **Characters** | SDXL (local) | $0 | Custom assets | $5-10/video |
| **Infrastructure** | Local GPU | $0 | Cloud GPU | $5-15/video |
| **YouTube API** | Free | $0 | Free | $0 |
| **Total** | | **~$0-25/video** | | **~$50-100/video** |

#### Per-Video Cost at Scale
- **Free stack**: ~$5-15 (cloud GPU, time investment)
- **Premium stack**: ~$75-100 (D-ID/HeyGen at scale)

#### Volume Needed for Profit
| Cost/Video | Views for BE | Profit per 10k views |
|------------|--------------|---------------------|
| $5.00 | 1,667 views | $25.00 |
| $15.00 | 5,000 views | $15.00 |
| $50.00 | 16,667 views | $0.00 |
| $100.00 | 33,333 views | -$40.00 |

**Verdict**: **High risk** - $50-100/video needs 16k-33k views just to break even

**Only viable if**: Viral potential, brand deals, or $10+ CPM achievable

---

## Economic Summary

| Niche | Low-Cost BE | Premium BE | Scalability | Risk Level |
|-------|-------------|------------|-------------|------------|
| **Niche 1 (Music)** | 167 views | 667 views | ⭐⭐⭐⭐⭐ | Low |
| **Niche 2 (Storytime)** | 333 views | 5,000 views | ⭐⭐⭐⭐ | Medium |
| **Niche 3 (Podcast)** | 1,667 views | 16,667 views | ⭐⭐ | High |

---

## Tracking Template

### Per-Video Sheet (Google Sheets / CSV)
```
| Video ID | Niche | Cost | Upload Date | Day1Views | Day7Views | Day30Views | TotalViews | Revenue | ROI |
|----------|-------|------|-------------|-----------|-----------|------------|------------|---------|-----|
| V001     | Music | $2.00| 2026-04-16  | 0         | 0         | 0          | 0          | $0.00   | -100%|
```

### Weekly Summary Sheet
```
| Week | VideosCreated | TotalCost | TotalViews | Revenue | Profit | Views/Video |
|------|---------------|-----------|------------|---------|--------|-------------|
| 1    | 5             | $10.00    | 2,500      | $7.50   | -$2.50 | 500         |
```

---

## Cost Optimization Strategies

### 1. Start Free, Scale Later
- Run MusicGen, SDXL, FFmpeg locally
- Use free LLM tiers initially
- Reinvest revenue into premium tools only after proving concept

### 2. Batch Production
- Generate 10 thumbnails in one SDXL pass
- Process 5 videos in one GPU session
- Reduces cloud compute costs significantly

### 3. Content Recycling
- Repurpose long-form to Shorts/Reels
- Extract clips for TikTok/Instagram
- Increases total views per production dollar

### 4. A/B Test Thumbnails
- Upload same video with different thumbnails
- Find highest CTR variant
- Improves organic reach

### 5. Graduated Tool Investment
```
Phase 1: All free stack → Validate concept
Phase 2: Add ElevenLabs for storytime → If music playlist works
Phase 3: Add D-ID/HeyGen for podcasts → If storytime profitable
```

---

## Decision Framework

### When to Pivot from Free → Paid Tool
```
IF (Tool Cost / Video) < ($3 × AverageViews / 1,000 × 0.5)
THEN tool is justified
```

Example: If average video gets 5,000 views:
- $3 CPM × 5,000 / 1,000 = $15 revenue
- Willing to spend up to $7.50 (50% of revenue) on tool
- **ElevenLabs at $10/video**: Borderline, needs >6,667 views
- **Suno at $30/mo for unlimited**: Worth it at 3,000+ views/mo

### Kill Switch Criteria
```
IF (VideosPublished > 10) AND (AverageViews < BreakEvenViews)
THEN reconsider strategy or niche
```

Example: After 10 storytime videos averaging 2,000 views each:
- Total views: 20,000
- Revenue: $60
- Cost (ElevenLabs): ~$150
- **Loss: $90 → Pivot needed**

---

## Action Items

1. **Set up cost tracking** - Google Sheet or CSV before first upload
2. **Start with Niche 1 (music)** - Lowest cost, easiest to scale
3. **Run 5-10 test videos** - Validate baseline performance
4. **Track CTR, watch time, RPM** - Beyond just views
5. **Only invest in premium tools after proving concept**
6. **Kill switch**: If 10 videos average <2,000 views, reconsider

---

## Notes for Future Reference

**Remember**: The goal isn't $10 videos with 50k views. It's $0.50 videos with 5k views.

**Margin is king** - At $3 CPM, every dollar spent on production is a dollar that needs 333 views to recoup.

**Start cheap, prove value, then scale** - Don't pre-invest in ElevenLabs or D-ID before you know which niche works.

**YouTube is a long game** - Evergreen content can earn for months. Track revenue over 30-90 days, not just first week.
