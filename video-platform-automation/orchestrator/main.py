"""
Video Platform Automation Pipeline Orchestrator

Single entry point that orchestrates the pipeline for different niches.
Can be called from CLI, cron jobs, or API.
"""

import os
import sys
import yaml
import logging
import argparse
from pathlib import Path
from typing import Optional

# Add app root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestrator.logger import setup_logger
from orchestrator.config import load_config
from orchestrator.musicgen import MusicGenGenerator
from orchestrator.stable_diffusion import StableDiffusionGenerator
from orchestrator.ffmpeg import FFmpegCompositor
from orchestrator.youtube import YouTubeUploader
from orchestrator.llm import LLMAssistant

# Set up logging
logger = logging.getLogger(__name__)

class VideoPipeline:
    """Main pipeline orchestrator."""
    
    def __init__(self, config_path: str = None):
        """Initialize pipeline with config."""
        self.config = load_config(config_path)
        self.output_dir = Path(self.config.get('output_dir', 'output/default'))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components (lazy load to avoid GPU on startup)
        self._musicgen = None
        self._sd = None
        self._ffmpeg = None
        self._youtube = None
        self._llm = None
        
        logger.info(f"Pipeline initialized for channel: {self.config.get('channel_id', 'default')}")
    
    @property
    def musicgen(self) -> MusicGenGenerator:
        if self._musicgen is None:
            self._musicgen = MusicGenGenerator()
        return self._musicgen
    
    @property
    def sd(self) -> StableDiffusionGenerator:
        if self._sd is None:
            self._sd = StableDiffusionGenerator()
        return self._sd
    
    @property
    def ffmpeg(self) -> FFmpegCompositor:
        if self._ffmpeg is None:
            self._ffmpeg = FFmpegCompositor()
        return self._ffmpeg
    
    @property
    def youtube(self) -> YouTubeUploader:
        if self._youtube is None:
            self._youtube = YouTubeUploader()
        return self._youtube
    
    @property
    def llm(self) -> LLMAssistant:
        if self._llm is None:
            self._llm = LLMAssistant()
        return self._llm
    
    def run_music_niche(self, prompt: str) -> str:
        """
        Run the music playlist pipeline.
        
        1. Generate music from prompt
        2. Generate thumbnail image from prompt
        3. Animate thumbnail (simple loop)
        4. Composite music + animated thumbnail
        5. Generate title/description via LLM
        6. Upload to YouTube
        
        Returns: Video upload URL or error
        """
        logger.info(f"Starting music pipeline with prompt: {prompt}")
        
        # Step 1: Generate music (60-120 min playlist)
        logger.info("Step 1: Generating music...")
        music_path = self.musicgen.generate(prompt, duration=3600)  # 60 min
        logger.info(f"Music generated: {music_path}")
        
        # Step 2: Generate thumbnail
        logger.info("Step 2: Generating thumbnail...")
        thumbnail_path = self.sd.generate(prompt, size=(1280, 720))
        logger.info(f"Thumbnail generated: {thumbnail_path}")
        
        # Step 3: Animate thumbnail (loop for 30-60 seconds)
        logger.info("Step 3: Animating thumbnail...")
        animated_path = self.ffmpeg.animate_thumbnail(thumbnail_path, duration=30)
        logger.info(f"Animated thumbnail: {animated_path}")
        
        # Step 4: Composite video with music
        logger.info("Step 4: Compositing video...")
        video_path = self.ffmpeg.compose_video(
            video=animated_path,
            audio=music_path,
            output=self.output_dir / f"music_playlist.mp4"
        )
        logger.info(f"Video composed: {video_path}")
        
        # Step 5: Generate metadata
        logger.info("Step 5: Generating metadata...")
        metadata = self.llm.generate_video_metadata(prompt, niche='music')
        logger.info(f"Metadata: {metadata}")
        
        # Step 6: Upload to YouTube
        logger.info("Step 6: Uploading to YouTube...")
        result = self.youtube.upload(
            video_path=video_path,
            title=metadata['title'],
            description=metadata['description'],
            tags=metadata['tags']
        )
        logger.info(f"Upload result: {result}")
        
        return result
    
    def run_storytime_niche(self, prompt: str) -> str:
        """
        Run the sleepy storytime pipeline.
        
        1. Generate calm script from theme via LLM
        2. Generate TTS audio
        3. Generate background music
        4. Generate sleepy visuals
        5. Composite audio + visuals
        6. Upload to YouTube
        
        Returns: Video upload URL or error
        """
        logger.info(f"Starting storytime pipeline with theme: {prompt}")
        
        # Step 1: Generate script
        logger.info("Step 1: Generating script...")
        script = self.llm.generate_story(prompt, tone='calm', duration=1800)  # 30 min
        logger.info(f"Script generated: {len(script)} characters")
        
        # Step 2: Generate TTS audio
        logger.info("Step 2: Generating TTS audio...")
        tts_path = self.llm.text_to_speech(script, voice='calm')
        logger.info(f"TTS audio generated: {tts_path}")
        
        # Step 3: Generate background music (ambient)
        logger.info("Step 3: Generating background music...")
        bg_music = self.musicgen.generate(prompt + " ambient chill", duration=1800)
        logger.info(f"Background music: {bg_music}")
        
        # Step 4: Generate sleepy visuals
        logger.info("Step 4: Generating visuals...")
        thumbnail = self.sd.generate(prompt + " cozy, dark, sleepy", size=(1280, 720))
        animated = self.ffmpeg.animate_thumbnail(thumbnail, duration=60)
        
        # Step 5: Composite (TTS + ambient music + looping visuals)
        logger.info("Step 5: Compositing video...")
        video_path = self.ffmpeg.compose_storytime(
            audio=tts_path,
            bg_music=bg_music,
            visual=animated,
            output=self.output_dir / f"storytime.mp4"
        )
        logger.info(f"Video composed: {video_path}")
        
        # Step 6: Upload
        logger.info("Step 6: Uploading to YouTube...")
        metadata = self.llm.generate_video_metadata(prompt, niche='storytime')
        result = self.youtube.upload(
            video_path=video_path,
            title=metadata['title'],
            description=metadata['description'],
            tags=metadata['tags']
        )
        
        return result
    
    def run_podcast_niche(self, prompt: str) -> str:
        """
        Run the animated podcast pipeline.
        
        1. Generate dialogue script from topic
        2. Generate two voice TTS tracks
        3. Generate character avatars
        4. Animate avatars with lip-sync
        5. Composite video
        6. Upload to YouTube
        
        Returns: Video upload URL or error
        """
        logger.info(f"Starting podcast pipeline with topic: {prompt}")
        
        # This is a placeholder - needs more tooling
        raise NotImplementedError("Podcast pipeline not yet implemented")
    
    def run(self):
        """Run the appropriate pipeline based on config."""
        niche = self.config.get('niche', 'music')
        prompt_file = self.config.get('prompt_file')
        
        if prompt_file and os.path.exists(prompt_file):
            with open(prompt_file) as f:
                prompt = f.read().strip()
        else:
            prompt = self.config.get('prompt', 'default prompt')
        
        logger.info(f"Running {niche} pipeline with prompt: {prompt}")
        
        if niche == 'music':
            return self.run_music_niche(prompt)
        elif niche == 'storytime':
            return self.run_storytime_niche(prompt)
        elif niche == 'podcast':
            return self.run_podcast_niche(prompt)
        else:
            raise ValueError(f"Unknown niche: {niche}")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description='Video Platform Automation Pipeline')
    parser.add_argument('--config', type=str, default='config/default/config.yaml',
                        help='Path to config file')
    parser.add_argument('--niche', type=str, choices=['music', 'storytime', 'podcast'],
                        help='Override niche from config')
    parser.add_argument('--prompt', type=str, help='Override prompt from config')
    parser.add_argument('--channel-id', type=str, help='Override channel ID')
    parser.add_argument('--dry-run', action='store_true', help='Show pipeline steps without executing')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logger()
    
    # Load config
    config = load_config(args.config)
    
    # Override with CLI args
    if args.niche:
        config['niche'] = args.niche
    if args.prompt:
        config['prompt'] = args.prompt
    if args.channel_id:
        config['channel_id'] = args.channel_id
    
    # Run pipeline
    pipeline = VideoPipeline(config)
    
    try:
        result = pipeline.run()
        logger.info(f"Pipeline completed successfully: {result}")
        return 0
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
