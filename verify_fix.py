
import os
import sys

# Ensure dundra can be imported
sys.path.append(os.getcwd())

try:
    from dundra.tools import characters_vertex_search_tool, campaign_vertex_search_tool
    print("Successfully imported tools.")
except ImportError as e:
    print(f"Failed to import tools: {e}")
    sys.exit(1)

def verify_tool_id(tool, name):
    print(f"\n--- Verifying {name} ---")
    data_store_id = tool.data_store_id
    print(f"ID: {data_store_id}")
    
    if not data_store_id:
        print("ERROR: data_store_id is empty")
        return False
        
    required_prefix = "projects/"
    if not data_store_id.startswith(required_prefix):
        print(f"ERROR: data_store_id should start with '{required_prefix}'")
        return False
        
    if "/collections/default_collection/dataStores/" not in data_store_id:
        print("ERROR: data_store_id seems to be missing collection or dataStores path components")
        return False
        
    print("SUCCESS: ID format looks correct.")
    return True

if __name__ == "__main__":
    c_ok = verify_tool_id(characters_vertex_search_tool, "Characters Tool")
    cmp_ok = verify_tool_id(campaign_vertex_search_tool, "Campaign Tool")
    
    if c_ok and cmp_ok:
        print("\nFix verified!")
        sys.exit(0)
    else:
        print("\nVerification failed.")
        sys.exit(1)
