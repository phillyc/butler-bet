"""
MusicGen wrapper for audio generation.
"""

import logging
from pathlib import Path
from typing import Optional
from audiocraft.models import MusicGen
from audiocraft.data.audio import write_audio

logger = logging.getLogger(__name__)


class MusicGenGenerator:
    """Generate music using MusicGen."""
    
    def __init__(self, model: str = 'musicgen-small'):
        """
        Initialize MusicGen generator.
        
        Args:
            model: Pretrained model to use (musicgen-small, musicgen-medium, etc.)
        """
        self.model = model
        self._model = None
        logger.info(f"MusicGenGenerator initialized with model: {model}")
    
    @property
    def model(self):
        """Lazy load model to avoid GPU on import."""
        if self._model is None:
            logger.info(f"Loading MusicGen model: {self.model}...")
            self._model = MusicGen.get_pretrained(self.model)
            logger.info("MusicGen model loaded")
        return self._model
    
    @model.setter
    def model(self, value):
        self._model = None  # Reset cached model
        self.model = value
    
    def generate(self, prompt: str, duration: int = 3600, output_dir: str = None) -> str:
        """
        Generate music from prompt.
        
        Args:
            prompt: Text prompt for music generation
            duration: Duration in seconds (default: 60 min = 3600)
            output_dir: Output directory for audio file
            
        Returns:
            Path to generated audio file
        """
        logger.info(f"Generating music: {prompt[:50]}...")
        
        # Generate with Melody model for 10 seconds (MusicGen limitation)
        # Then we can loop/fade for longer
        logger.info("Generating base melody...")
        self.model.set_generation_params(duration=10)  # Max 10s per generation
        outputs = self.model.generate([prompt])
        
        # Save the generated audio
        output_dir = Path(output_dir) if output_dir else Path('output/audio')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # MusicGen outputs are tensors, save to file
        audio_data = outputs[0]
        output_path = output_dir / f"{prompt.replace(' ', '_')[:50]}.wav"
        write_audio(audio_data, str(output_path))
        
        logger.info(f"Generated audio saved to: {output_path}")
        
        return str(output_path)
    
    def generate_loopable(self, prompt: str, duration: int = 60, output_dir: str = None) -> str:
        """
        Generate a loopable music segment.
        
        Args:
            prompt: Text prompt
            duration: Desired duration in seconds
            output_dir: Output directory
            
        Returns:
            Path to looped audio file
        """
        # Generate 10-second clip and loop it
        clip_path = self.generate(prompt, duration=10, output_dir=output_dir)
        
        # Use FFmpeg to loop the clip
        from orchestrator.ffmpeg import FFmpegCompositor
        ffmpeg = FFmpegCompositor()
        looped_path = ffmpeg.loop_audio(clip_path, target_duration=duration)
        
        logger.info(f"Looped audio saved to: {looped_path}")
        return looped_path
