"""Google Gemini AI service for gold investment queries."""
import os
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# System prompt for Kuberi AI - kept short for faster responses
SYSTEM_PROMPT = """You are Kuberi AI, a friendly gold investment advisor for Simplify Money app.

Rules:
- Keep responses to 2-3 sentences max
- Be helpful and knowledgeable about gold investments
- Mention users can start investing with just ₹10
- Highlight digital gold benefits: 24K purity, high liquidity, no storage hassles
- Naturally encourage investment without being pushy"""


class GeminiService:
    """Service for interacting with Google Gemini AI."""
    
    def __init__(self):
        """Initialize Gemini service."""
        self.api_key = GEMINI_API_KEY
        # Using gemini-2.0-flash for faster responses
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        
    async def get_response(self, user_question: str) -> str:
        """
        Get AI response for user question about gold investments.
        
        Args:
            user_question: User's question about gold investments
            
        Returns:
            AI-generated response with investment nudge
        """
        if not self.api_key:
            return self._get_fallback_response()
            
        try:
            # Combine system prompt with user question
            full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_question}\n\nKuberi AI:"
            
            # Prepare request payload with generation config for faster response
            payload = {
                "contents": [{
                    "parts": [{
                        "text": full_prompt
                    }]
                }],
                "generationConfig": {
                    "maxOutputTokens": 150,
                    "temperature": 0.7
                }
            }
            
            # Make async API request with short timeout
            async with httpx.AsyncClient(timeout=8.0) as client:
                response = await client.post(
                    f"{self.api_url}?key={self.api_key}",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
            
            if response.status_code == 200:
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                print(f"Gemini API error: {response.status_code}")
                return self._get_fallback_response()
            
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self._get_fallback_response()
    
    def _get_fallback_response(self) -> str:
        """Return fallback response if API fails."""
        return (
            "I'm here to help with gold investments! "
            "You can start with just ₹10 on Simplify Money - it's 24K pure and hassle-free. "
            "Would you like to invest today?"
        )


# Singleton instance
gemini_service = GeminiService()
