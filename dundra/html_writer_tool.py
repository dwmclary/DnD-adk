import os
import uuid
from typing import Optional
from google.cloud import storage

class HtmlWriterTool:
    name: str = "Html_Writer_Tool"
    description: str = "A tool to write HTML content to a file in the generated_stories directory and upload it to Google Cloud Storage. Useful for saving the final campaign website."
    
    def __init__(self):
        self.bucket_name = os.getenv("GCS_BUCKET_NAME")
        if not self.bucket_name:
            print("WARNING: GCS_BUCKET_NAME not set. Stories will only be saved locally.")

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
                    # Make public or just return authenticated link? 
                    # Ideally we might want it public for this demo, or we assume the user has access.
                    # blob.make_public() # Optional, depending on bucket policy
                    
                    gcs_url = f"https://storage.googleapis.com/{self.bucket_name}/{filename}"
                    msg += f" and uploaded to {gcs_url}"
                except Exception as e:
                    msg += f". Failed to upload to GCS: {str(e)}"
                
            return msg
        except Exception as e:
            return f"Error writing HTML file: {str(e)}"
    
    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)
