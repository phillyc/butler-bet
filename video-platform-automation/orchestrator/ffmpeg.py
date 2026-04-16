"""
FFmpeg wrapper for video/audio processing.
"""

import logging
import subprocess
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class FFmpegCompositor:
    """FFmpeg wrapper for video/audio operations."""
    
    def __init__(
        self,
        video_bitrate: str = '2500k',
        audio_bitrate: str = '192k',
        frame_rate: int = 30
    ):
        """
        Initialize FFmpeg compositor.
        
        Args:
            video_bitrate: Output video bitrate
            audio_bitrate: Output audio bitrate
            frame_rate: Output frame rate
        """
        self.video_bitrate = video_bitrate
        self.audio_bitrate = audio_bitrate
        self.frame_rate = frame_rate
        
        # Check if ffmpeg is available
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            logger.info("FFmpeg is available")
        except subprocess.CalledProcessError:
            logger.error("FFmpeg not found. Install it with: apt-get install ffmpeg")
            raise
    
    def animate_thumbnail(self, image_path: str, duration: int = 30, output: str = None) -> str:
        """
        Add simple animation to thumbnail (zoom + pan effect).
        
        Args:
            image_path: Input image path
            duration: Output video duration in seconds
            output: Output path (will be auto-generated if not provided)
            
        Returns:
            Path to animated video
        """
        image_path = Path(image_path)
        output_dir = output.parent if output else image_path.parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if not output:
            output = output_dir / f"animated_{image_path.name}.mp4"
        
        # Apply zoom-in effect using scale and crop filters
        # Start zoomed in at 120%, scale down to 100% over duration
        cmd = [
            'ffmpeg', '-y',
            '-loop', '1',
            '-i', str(image_path),
            '-vf', f'scale=iw*1.2:ih*1.2, crop=iw:ih,setsar=1,fps={self.frame_rate}',
            '-t', str(duration),
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            str(output)
        ]
        
        logger.info(f"Animating thumbnail: {image_path} -> {output}")
        subprocess.run(cmd, check=True)
        
        return str(output)
    
    def compose_video(self, video: str, audio: str, output: str = None) -> str:
        """
        Composite video with audio.
        
        Args:
            video: Input video path
            audio: Input audio path
            output: Output path
            
        Returns:
            Path to composed video
        """
        output_dir = Path(output).parent if output else Path('output/composed')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if not output:
            video_name = Path(video).stem
            output = output_dir / f"{video_name}_composed.mp4"
        
        cmd = [
            'ffmpeg', '-y',
            '-i', video,
            '-i', audio,
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-b:v', self.video_bitrate,
            '-b:a', self.audio_bitrate,
            '-vf', f'fps={self.frame_rate}',
            '-pix_fmt', 'yuv420p',
            str(output)
        ]
        
        logger.info(f"Composing video: {video} + {audio} -> {output}")
        subprocess.run(cmd, check=True)
        
        return str(output)
    
    def compose_storytime(
        self,
        audio: str,
        bg_music: str,
        visual: str,
        output: str = None
    ) -> str:
        """
        Composite storytime video (TTS + bg music + looping visual).
        
        Args:
            audio: TTS audio path
            bg_music: Background music path
            visual: Looping visual path
            output: Output path
            
        Returns:
            Path to composed video
        """
        output_dir = Path(output).parent if output else Path('output/composed')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if not output:
            output = output_dir / f"storytime_composed.mp4"
        
        # Loop visual to match audio duration
        # Mix TTS with bg music (lower bg music volume)
        cmd = [
            'ffmpeg', '-y',
            '-stream_loop', '-1',  # Loop visual
            '-i', visual,
            '-i', audio,
            '-i', bg_music,
            '-filter_complex', '[1:a][2:a]amix=inputs=2:duration=first[audio]',
            '-map', '0:v',
            '-map', '[audio]',
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-b:v', self.video_bitrate,
            '-b:a', self.audio_bitrate,
            '-vf', f'fps={self.frame_rate}',
            '-pix_fmt', 'yuv420p',
            str(output)
        ]
        
        logger.info(f"Composing storytime: {visual} + {audio} + {bg_music} -> {output}")
        subprocess.run(cmd, check=True)
        
        return str(output)
    
    def loop_audio(self, audio_path: str, target_duration: int, output: str = None) -> str:
        """
        Loop audio to target duration.
        
        Args:
            audio_path: Input audio path
            target_duration: Target duration in seconds
            output: Output path
            
        Returns:
            Path to looped audio
        """
        output_dir = Path(output).parent if output else Path('output/audio')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if not output:
            audio_name = Path(audio_path).stem
            output = output_dir / f"{audio_name}_looped.wav"
        
        cmd = [
            'ffmpeg', '-y',
            '-stream_loop', '-1',
            '-i', audio_path,
            '-t', str(target_duration),
            '-c:a', 'pcm_s16le',
            str(output)
        ]
        
        logger.info(f"Looping audio: {audio_path} -> {output}")
        subprocess.run(cmd, check=True)
        
        return str(output)
