import os

class ToolService:
    """Service for handling tool calls."""
    
    def process_tool_call(self, name: str, arguments: dict):
        """Process a tool call and return the result."""
        if name == "read_file":
            return self.read_file(arguments.get("file_path"))
        else:
            return {"error": f"Unknown tool: {name}"}
    
    def read_file(self, file_path: str):
        """Read a file and return its contents."""
        try:
            # Make sure the file path doesn't try to access sensitive areas
            base_dir = os.path.dirname(os.path.abspath(__file__))
            absolute_path = os.path.join(base_dir, file_path)
            
            # Simple security check to prevent directory traversal
            if not os.path.abspath(absolute_path).startswith(base_dir):
                return {"error": "Access denied: Cannot access files outside the base directory"}
            
            if not os.path.exists(absolute_path):
                return {"error": f"File not found: {file_path}"}
            
            with open(absolute_path, 'r') as file:
                content = file.read()
                
            return {"content": content}
        except Exception as e:
            return {"error": f"Error reading file: {str(e)}"}