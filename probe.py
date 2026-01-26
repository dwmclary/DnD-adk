
import os
import sys

# Check ADK
try:
    from google.adk.tools.crewai_tool import CrewaiTool
    print("Successfully imported CrewaiTool")
except ImportError as e:
    print(f"Failed to import CrewaiTool: {e}")

# Check BaseTool
try:
    from crewai_tools import BaseTool
    print("Successfully imported BaseTool from crewai_tools")
except ImportError:
    print("Failed to import BaseTool from crewai_tools")
    try:
        from crewai.tools import BaseTool
        print("Successfully imported BaseTool from crewai.tools")
    except ImportError:
        print("Failed to import BaseTool from crewai.tools")
        # List crewai_tools
        try:
            import crewai_tools
            print(f"crewai_tools dir: {dir(crewai_tools)}")
        except ImportError:
            print("Could not import crewai_tools")

# Check DallETool base
try:
    from crewai_tools import DallETool
    print(f"DallETool bases: {DallETool.__mro__}")
except ImportError:
    print("Could not import DallETool")
