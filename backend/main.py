from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import List, Dict, Any

from models import ChatRequest, ChatResponse, Message, MessageContent, ToolCallRequest, ToolCallResponse
from gemini_service import GeminiService
from tool_service import ToolService

app = FastAPI(title="Chat App Backend")

# Configure CORS to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
gemini_service = GeminiService()
tool_service = ToolService()

# Sample test.txt file
with open("test.txt", "w") as f:
    f.write("This is a test file.\nIt contains some sample text for demonstration purposes.")

@app.get("/")
async def root():
    return {"message": "Chat App Backend is running"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Convert to dict for easier processing
        messages_dict = [msg.model_dump() for msg in request.messages]

        print("main.py wali messages_dict:-->", messages_dict)
        
        # Get response from Gemini
        response = gemini_service.generate_response(messages_dict)

        print("response at main.py: ",response)
        
        if "error" in response:
            raise HTTPException(status_code=500, detail=response["error"])
        
        # Check if Gemini suggested a tool call
        if "tool_call" in response:
            # Create a response with the tool call suggestion
            tool_call = response["tool_call"]
            
            # Process the tool call
            tool_result = tool_service.process_tool_call(
                tool_call["name"], 
                tool_call["arguments"]
            )
            
            # Return the assistant message with both text and tool call result
            message = Message(
                role="assistant",
                content=[
                    MessageContent(type="text", text=response["text"]),
                    MessageContent(type="tool_call_result", tool_call_result=tool_result)
                ]
            )
            
        else:
            # Return simple text response
            message = Message(
                role="assistant",
                content=response["text"]
            )
        
        return ChatResponse(message=message)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/tool", response_model=ToolCallResponse)
async def tool_call(request: ToolCallRequest):
    try:
        result = tool_service.process_tool_call(request.name, request.arguments)
        return ToolCallResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)