import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Add current directory to path
sys.path.append(os.getcwd())

from dundra.tools import adk_imagen_tool

def test_imagen_tool():
    print("Testing ImagenTool via ADK wrapper...")
    
    # We can try to invoke it.
    # CrewaiTool wraps the tool, so we might need to access the underlying tool or run it as an agent would?
    # Actually CrewaiTool is an ADK thing that adapts it.
    
    # Let's inspect what adk_imagen_tool is.
    print(f"adk_imagen_tool type: {type(adk_imagen_tool)}")
    print(f"adk_imagen_tool dict: {adk_imagen_tool.__dict__}")
    
    # It seems to be an instance of CrewaiTool.
    # Let's try to access the underlying tool if possible, or just call run if it has it.
    
    # If it's the ADK wrapper, it might not be directly callable like a function?
    # Let's check `dundra/tools.py`:
    # adk_imagen_tool = CrewaiTool(..., tool=imagen_tool)
    
    # We can also test the underlying tool directly.
    from dundra.tools import imagen_tool
    
    print("\nTesting underlying ImagenTool directly...")
    prompt = "A cute pixel art robot holding a wrench"
    result = imagen_tool._run(prompt)
    
    print(f"Result: {result}")
    
    if os.path.exists(result):
        print(f"SUCCESS: Image generated at {result}")
    else:
        # If result is multiple paths joined by newline
        paths = result.split("\n")
        if all(os.path.exists(p) for p in paths):
             print(f"SUCCESS: Images generated at {paths}")
        else:
            print(f"FAILURE: File not found at {result}")

if __name__ == "__main__":
    test_imagen_tool()
