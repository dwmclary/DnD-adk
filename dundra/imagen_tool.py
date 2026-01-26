import os
import uuid
import base64
from typing import Optional, Any

from crewai.tools import BaseTool
from pydantic import Field, PrivateAttr

try:
    from google import genai
    from google.genai import types
    from PIL import Image
    import io
except ImportError:
    genai = None
    types = None
    Image = None

class ImagenTool(BaseTool):
    name: str = "Imagen_Images_Creator"
    description: str = "A tool designed to generate images using Google's Vertex AI Imagen model."
    model: str = Field(default="imagen-3.0-generate-001", description="The Imagen model to use.")
    number_of_images: int = Field(default=1, description="Number of images to generate.")
    output_dir: str = Field(default="generated_images", description="Directory to save generated images.")
    
    _client: Optional[Any] = PrivateAttr(default=None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if genai is None or Image is None:
            raise ImportError("Please install `google-genai` and `Pillow` packages to use ImagenTool.")
        
        # When using Vertex AI, keys are not used, but ADC (Application Default Credentials).
        # However, google-genai client might still accept api_key if we were using AI Studio.
        # For Vertex AI, we rely on the environment being configured (GOOGLE_GENAI_USE_VERTEXAI=TRUE)
        # and implicit credentials or explicit project/location which google-genai picks up from env.
        
        # We initialize the client without args to let it pick up defaults from env
        self._client = genai.Client(
            vertexai=True, 
            project=os.environ.get("GOOGLE_CLOUD_PROJECT"), 
            location=os.environ.get("GOOGLE_CLOUD_LOCATION")
        )
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _run(self, prompt: str) -> str:
        """
        Generates an image based on the prompt and saves it to disk.
        Returns the path to the saved image.
        """
        try:
            print(f"Generating image for prompt: {prompt} with model {self.model}")
            
            # Using Vertex AI Imagen API (generate_images)
            response = self._client.models.generate_images(
                model=self.model,
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=self.number_of_images,
                )
            )
            
            saved_paths = []
            
            if response.generated_images:
                for generated_image in response.generated_images:
                    image_bytes = generated_image.image.image_bytes
                    
                    filename = f"imagen_{uuid.uuid4()}.png"
                    filepath = os.path.join(self.output_dir, filename)
                    
                    with open(filepath, "wb") as f:
                        f.write(image_bytes)
                    
                    saved_paths.append(filepath)
            
            if not saved_paths:
                return "No images generated."
                
            return "\n".join(saved_paths)

        except Exception as e:
            return f"Error generating image: {str(e)}"
