"""Google Gemini AI service for gold investment queries."""
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# System prompt for Kuberi AI
SYSTEM_PROMPT = """You are Kuberi AI, a professional and friendly financial advisor specializing in gold investments within the Simplify Money app.

Your communication style:
- Professional yet warm and approachable
- Clear, concise, and easy to understand
- Confident and knowledgeable
- Helpful and supportive

Your responsibilities:
1. Provide accurate, well-researched information about gold investments
2. Explain the benefits of digital gold: 24K purity, high liquidity, no storage concerns, accessible with small amounts
3. Answer questions about gold prices, market trends, and investment strategies
4. Naturally guide users toward investing in digital gold through Simplify Money
5. Keep responses focused and actionable (2-4 sentences)

When discussing investment opportunities:
- Mention that users can start with as little as ₹10 on Simplify Money
- Highlight the convenience and safety of digital gold
- Gently ask if they'd like to make their first investment
- Be encouraging but never pushy

Always prioritize being helpful and informative. Build trust through expertise, then naturally suggest investment opportunities."""


class GeminiService:
    """Service for interacting with Google Gemini AI."""
    
    def __init__(self):
        """Initialize Gemini service."""
        self.api_key = GEMINI_API_KEY
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"
        
    def get_response(self, user_question: str) -> str:
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
            full_prompt = f"{SYSTEM_PROMPT}\n\nUser Question: {user_question}\n\nKuberi AI Response:"
            
            # Prepare request payload
            payload = {
                "contents": [{
                    "parts": [{
                        "text": full_prompt
                    }]
                }]
            }
            
            # Make API request
            response = requests.post(
                f"{self.api_url}?key={self.api_key}",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                print(f"Error calling Gemini API: {response.status_code} - {response.text}")
                return self._get_fallback_response()
            
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return self._get_fallback_response()
    
    def _get_fallback_response(self) -> str:
        """Return fallback response if API fails."""
        return (
            f"I'm here to help you with gold investments! "
            f"Digital gold is a smart way to invest - you can start with just ₹10 on Simplify Money. "
            f"It's 24K pure, highly liquid, and has no storage hassles. "
            f"Would you like to make your first investment today?"
        )


# Singleton instance
gemini_service = GeminiService()
