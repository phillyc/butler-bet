"""
Stable Diffusion wrapper for image generation.
"""

import logging
from pathlib import Path
from typing import Optional, Tuple
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image

logger = logging.getLogger(__name__)


class StableDiffusionGenerator:
    """Generate images using Stable Diffusion."""
    
    def __init__(
        self,
        model: str = 'runwayml/stable-diffusion-v1-5',
        width: int = 1280,
        height: int = 720,
        use_fp16: bool = True
    ):
        """
        Initialize Stable Diffusion generator.
        
        Args:
            model: Model to use from HuggingFace
            width: Image width
            height: Image height
            use_fp16: Use FP16 for faster inference (requires GPU)
        """
        self.model = model
        self.width = width
        self.height = height
        self.use_fp16 = use_fp16
        self._pipeline = None
        
        logger.info(f"StableDiffusionGenerator initialized: {model}")
    
    @property
    def pipeline(self):
        """Lazy load pipeline."""
        if self._pipeline is None:
            logger.info(f"Loading Stable Diffusion model: {self.model}...")
            
            dtype = torch.float16 if self.use_fp16 and torch.cuda.is_available() else torch.float32
            
            self._pipeline = StableDiffusionPipeline.from_pretrained(
                self.model,
                torch_dtype=dtype,
                safety_checker=None  # Disable for automated generation
            )
            
            if torch.cuda.is_available():
                self._pipeline = self._pipeline.cuda()
            
            logger.info("Stable Diffusion pipeline loaded")
        
        return self._pipeline
    
    def generate(
        self,
        prompt: str,
        negative_prompt: str = None,
        size: Tuple[int, int] = None,
        num_images: int = 1,
        output_dir: str = None
    ) -> str:
        """
        Generate image(s) from prompt.
        
        Args:
            prompt: Text prompt for image generation
            negative_prompt: What to avoid in the image
            size: (width, height) tuple
            num_images: Number of images to generate
            output_dir: Output directory
            
        Returns:
            Path to first generated image
        """
        if size:
            self.width, self.height = size
        
        logger.info(f"Generating image: {prompt[:50]}...")
        
        with torch.no_grad():
            generator = torch.Generator(device='cuda') if torch.cuda.is_available() else None
            
            image = self.pipeline(
                prompt=prompt,
                negative_prompt=negative_prompt,
                width=self.width,
                height=self.height,
                num_inference_steps=50,
                guidance_scale=7.5,
                generator=generator,
                num_images_per_prompt=num_images,
            ).images[0]
        
        # Save image
        output_dir = Path(output_dir) if output_dir else Path('output/thumbnails')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = output_dir / f"{prompt.replace(' ', '_')[:50]}.jpg"
        image.save(output_path)
        
        logger.info(f"Image saved to: {output_path}")
        
        return str(output_path)
