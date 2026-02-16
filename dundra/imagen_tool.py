import os
import uuid
import base64
from typing import Optional, Any
from google.cloud import storage

try:
    from google import genai
    from google.genai import types
    from PIL import Image
    import io
except ImportError:
    genai = None
    types = None
    Image = None

from google.adk.tools import BaseTool, ToolContext
from google.genai import types

class ImagenTool(BaseTool):
    def __init__(self, model: str = "imagen-3.0-generate-001", number_of_images: int = 1, output_dir: str = "generated_stories/generated_images"):
        super().__init__(
            name="Imagen_Images_Creator",
            description="A tool designed to generate images using Google's Vertex AI Imagen model."
        )
        self.model = model
        self.number_of_images = number_of_images
        self.output_dir = output_dir
        self.bucket_name = os.getenv("GCS_BUCKET_NAME")
        
        if genai is None or Image is None:
            raise ImportError("Please install `google-genai` and `Pillow` packages to use ImagenTool.")
        
        self._client = genai.Client(
            vertexai=True, 
            project=os.environ.get("GOOGLE_CLOUD_PROJECT"), 
            location=os.environ.get("GOOGLE_CLOUD_LOCATION")
        )
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _get_declaration(self) -> types.FunctionDeclaration:
        return types.FunctionDeclaration(
            name=self.name,
            description=self.description,
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "prompt": types.Schema(
                        type="STRING",
                        description="The prompt to generate an image for."
                    )
                },
                required=["prompt"]
            )
        )

    async def run_async(self, args: dict[str, Any], tool_context: ToolContext) -> str:
        # Check if 'prompt' is in args, handle case sensitivity or missing args if needed
        # The key might be 'prompt' or match the schema property name. 
        prompt = args.get("prompt")
        if not prompt:
             return "Error: No prompt provided."
        return self.run(prompt)

    def run(self, prompt: str) -> str:
        """
        Generates an image based on the prompt and saves it to disk and optionally uploads to GCS.
        Returns the path or URL to the saved image.
        """
        import tenacity
        from google.api_core import exceptions as google_exceptions
        
        # Retry configuration: wait exponentially, up to 60 seconds, retry on ResourceExhausted or ServiceUnavailable
        # We also check for "429" or "Reason: 429" in the exception string in case of wrapped errors.
        def _is_retryable_error(exception):
            if isinstance(exception, (google_exceptions.ResourceExhausted, google_exceptions.ServiceUnavailable, google_exceptions.TooManyRequests)):
                return True
            msg = str(exception).lower()
            return "429" in msg or "resourceexhausted" in msg or "quota" in msg or "too many requests" in msg

        @tenacity.retry(
            wait=tenacity.wait_exponential(multiplier=2, min=2, max=60),
            stop=tenacity.stop_after_attempt(5),
            retry=tenacity.retry_if_exception(_is_retryable_error),
            reraise=True
        )
        def _generate_with_retry():
            print(f"Generating image for prompt: '{prompt}' with model {self.model}")
            
            # Debug: print config
            try:
                config_obj = types.GenerateImagesConfig(
                    number_of_images=self.number_of_images,
                )
                print(f"Debug: Config object: {config_obj}")
            except Exception as e:
                print(f"Debug: Error creating config object: {e}")

            # Using Vertex AI Imagen API (generate_images)
            response = self._client.models.generate_images(
                model=self.model,
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=self.number_of_images,
                )
            )
            return response

        try:
            response = _generate_with_retry()
            
            saved_paths = []
            
            if response.generated_images:
                storage_client = None
                bucket = None
                if self.bucket_name:
                    try:
                        storage_client = storage.Client()
                        bucket = storage_client.bucket(self.bucket_name)
                    except Exception as e:
                        print(f"Failed to initialize GCS client: {e}")

                for generated_image in response.generated_images:
                    image_bytes = generated_image.image.image_bytes
                    
                    filename = f"imagen_{uuid.uuid4()}.png"
                    filepath = os.path.join(self.output_dir, filename)
                    
                    with open(filepath, "wb") as f:
                        f.write(image_bytes)
                    
                    # Upload to GCS if configured
                    if bucket:
                        try:
                            blob = bucket.blob(f"images/{filename}")
                            blob.upload_from_filename(filepath)
                            # blob.make_public() # Optional
                            gcs_url = f"https://storage.googleapis.com/{self.bucket_name}/images/{filename}"
                            saved_paths.append(gcs_url)
                        except Exception as e:
                            print(f"Failed to upload image to GCS: {e}")
                            saved_paths.append(filepath)
                    else:
                        saved_paths.append(filepath)
            
            if not saved_paths:
                return "No images generated."
                
            return "\n".join(saved_paths)

        except Exception as e:
            import traceback
            traceback.print_exc() # Print full traceback for debugging 400 errors
            return f"Error generating image: {str(e)}"

    def __call__(self, *args, **kwargs):
        # Support calling as specific method or just run
        if 'prompt' in kwargs:
            return self.run(kwargs['prompt'])
        if len(args) > 0:
            return self.run(args[0])
        return "Error: No prompt provided."
