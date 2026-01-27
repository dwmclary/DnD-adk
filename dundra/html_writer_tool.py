
import os
from crewai.tools import BaseTool
from pydantic import Field

class HtmlWriterTool(BaseTool):
    name: str = "Html_Writer_Tool"
    description: str = "A tool to write HTML content to a file in the generated_stories directory. Useful for saving the final campaign website."
    filename: str = Field(default="campaign.html", description="The filename to save the HTML content to.")
    
    def _run(self, html_content: str, filename: str = "campaign.html") -> str:
        """
        Writes the provided HTML content to a file in the generated_stories directory.
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
                
            return f"Successfully wrote HTML content to {filepath}"
        except Exception as e:
            return f"Error writing HTML file: {str(e)}"
