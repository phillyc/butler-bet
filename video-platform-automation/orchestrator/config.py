"""
Configuration loader for pipeline settings.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

DEFAULT_CONFIG = {
    'niche': 'music',
    'channel_id': 'default',
    'prompt': '',
    'prompt_file': None,
    'output_dir': 'output/default',
    'log_level': 'info',
    
    # MusicGen settings
    'musicgen': {
        'model': 'musicgen-small',
        'duration': 3600,  # 60 minutes in seconds
        'temperature': 0.7,
        'top_k': 250,
        'top_p': 0.8,
    },
    
    # Stable Diffusion settings
    'stable_diffusion': {
        'model': 'runwayml/stable-diffusion-v1-5',
        'width': 1280,
        'height': 720,
        'num_inference_steps': 50,
        'guidance_scale': 7.5,
    },
    
    # FFmpeg settings
    'ffmpeg': {
        'video_bitrate': '2500k',
        'audio_bitrate': '192k',
        'frame_rate': 30,
    },
    
    # YouTube settings
    'youtube': {
        'privacy_status': 'private',  # or 'public', 'unlisted'
        'category_id': '22',  # People & Blogs
    },
    
    # LLM settings
    'llm': {
        'api_key': None,
        'model': 'anthropic/claude-3.5-sonnet',
    },
}


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load pipeline configuration from file or use defaults.
    
    Args:
        config_path: Path to YAML config file
        
    Returns:
        Merged configuration dict
    """
    config = DEFAULT_CONFIG.copy()
    
    if config_path and os.path.exists(config_path):
        with open(config_path) as f:
            user_config = yaml.safe_load(f) or {}
            config = merge_configs(config, user_config)
    
    # Override with environment variables if set
    config = apply_env_overrides(config)
    
    return config


def merge_configs(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively merge two dicts."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = value
    return result


def apply_env_overrides(config: Dict[str, Any]) -> Dict[str, Any]:
    """Override config values from environment variables."""
    env_overrides = {
        'channel_id': 'CHANNEL_ID',
        'output_dir': 'OUTPUT_DIR',
        'log_level': 'LOG_LEVEL',
    }
    
    for key, env_var in env_overrides.items():
        if env_var in os.environ:
            config[key] = os.environ[env_var]
    
    return config


def save_config(config: Dict[str, Any], config_path: str) -> None:
    """Save configuration to file."""
    Path(config_path).parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
