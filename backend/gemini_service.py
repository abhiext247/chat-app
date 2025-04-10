import os
import google.generativeai as genai
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class GeminiService:
    """Service for interacting with Google's Gemini API."""

    def __init__(self):
        """Initialize the Gemini service with API key."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

    def generate_response(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a response from Gemini based on the chat history."""
        try:
            # Convert our message format to Gemini's expected format
            gemini_messages = []

            msg = messages

            role = "user" if msg[-1]["role"] == "user" else "model"

            if isinstance(msg[-1]["content"], str):
                    gemini_messages.append(
                        {"role": role, "parts": [msg[-1]["content"]]})
                    print("gemini_message in gemini_service.py:--> ",
                          gemini_messages)
            else:
                    # Handle complex content with tool calls
                    parts = []
                    for content_item in msg[-1]["content"]:
                        print("content_item type:-->", content_item["type"])
                        if content_item["type"] == "text":
                            parts.append(content_item["text"])
                        elif content_item["type"] == "tool_call_result":
                            # Format tool call results in a way Gemini can understand
                            tool_result = content_item["tool_call_result"]
                            parts.append(f"Tool call result: {tool_result}")

                    gemini_messages.append({"role": role, "parts": parts})

            # Send the conversation to Gemini
            # response = self.model.generate_content(gemini_messages)
            chat_session = self.model.start_chat(history=gemini_messages)
            response = chat_session.send_message("Continue")

            print("response at gemini_service.py: ", response)

            # Check if Gemini is suggesting a tool call
            text_response = response.text
            tool_call = self._extract_tool_call(text_response)

            if tool_call:
                # Return both the text and the extracted tool call
                return {
                    "text": text_response,
                    "tool_call": tool_call
                }
            else:
                # Return just the text response
                return {"text": text_response}

        except Exception as e:
            return {"error": f"Error generating response: {str(e)}"}

    def _extract_tool_call(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Extract tool calls from the response text.
        In a real implementation, we would use a more sophisticated method,
        but for this example we'll use a simple keyword approach.
        """
        # Simple detection of "read file" commands
        if "read file" in text.lower() or "read the file" in text.lower():
            # Extract the filename - looking for text between quotes or after "file"
            import re

            # Try to find filename in quotes
            file_match = re.search(r"[\'\"]([^\'\"]+)[\'\"]", text)
            if not file_match:
                # Try to find filename after "file" keyword
                file_match = re.search(r"file\s+([^\s.,]+)", text.lower())

            if file_match:
                filename = file_match.group(1)
                return {
                    "name": "read_file",
                    "arguments": {"file_path": filename}
                }

        return None
