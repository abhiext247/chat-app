from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union


class MessageContent(BaseModel):
    """Content of a message, which can be text or a tool call result."""
    type: str  # 'text' or 'tool_call_result'
    text: Optional[str] = None
    tool_call_result: Optional[Dict[str, Any]] = None


class Message(BaseModel):
    """A chat message with role and content."""
    role: str  # 'user' or 'assistant'
    content: Union[str, List[MessageContent]]


class ChatRequest(BaseModel):
    """Request model for chat messages."""
    messages: List[Message]


class ChatResponse(BaseModel):
    """Response model for chat messages."""
    message: Message


class ToolCallRequest(BaseModel):
    """Model for a tool call request."""
    name: str
    arguments: Dict[str, Any]


class ToolCallResponse(BaseModel):
    """Model for a tool call response."""
    result: Any