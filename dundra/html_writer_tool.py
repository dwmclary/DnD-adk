import os
import uuid
from typing import Optional, Any
from google.cloud import storage

from google.adk.tools import BaseTool, ToolContext
from google.genai import types

class HtmlWriterTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="Html_Writer_Tool",
            description="A tool to write HTML content to a file in the generated_stories directory and upload it to Google Cloud Storage. Useful for saving the final campaign website."
        )
        self.__name__ = "Html_Writer_Tool" # Fix for ADK AFC util
        self.bucket_name = os.getenv("GCS_BUCKET_NAME")
        if not self.bucket_name:
            print("WARNING: GCS_BUCKET_NAME not set. Stories will only be saved locally.")

    def _get_declaration(self) -> types.FunctionDeclaration:
        return types.FunctionDeclaration(
            name=self.name,
            description=self.description,
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "html_content": types.Schema(
                        type="STRING",
                        description="The full HTML content of the story/campaign."
                    ),
                    "filename": types.Schema(
                        type="STRING",
                        description="The filename to save as, ending in .html (e.g. 'my_story.html')."
                    )
                },
                required=["html_content", "filename"]
            )
        )

    def run(self, html_content: str, filename: str = "campaign.html") -> str:
        """
        Writes the provided HTML content to a file in the generated_stories directory and uploads to GCS.
        """
        try:
            output_dir = "generated_stories"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            # Ensure filename ends with .html
            if not filename.endswith(".html"):
                filename += ".html"
                
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html_content)
            
            msg = f"Successfully wrote HTML content to {filepath}"

            if self.bucket_name:
                try:
                    storage_client = storage.Client()
                    bucket = storage_client.bucket(self.bucket_name)
                    blob = bucket.blob(filename)
                    blob.upload_from_filename(filepath)
                    
                    gcs_url = f"https://storage.googleapis.com/{self.bucket_name}/{filename}"
                    msg += f" and uploaded to {gcs_url}"
                except Exception as e:
                    msg += f". Failed to upload to GCS: {str(e)}"
                
            return msg
        except Exception as e:
            return f"Error writing HTML file: {str(e)}"
    
    async def run_async(self, args: dict[str, Optional[Any]], tool_context: ToolContext) -> str:
        html_content = args.get("html_content")
        filename = args.get("filename", "campaign.html")
        if not html_content:
            return "Error: html_content is required."
        return self.run(html_content, filename)
    
    def __call__(self, *args, **kwargs):
        if 'html_content' in kwargs:
             return self.run(kwargs['html_content'], kwargs.get('filename', 'campaign.html'))
        if len(args) > 0:
             return self.run(args[0], args[1] if len(args) > 1 else "campaign.html")
        return "Error: html_content is required."
