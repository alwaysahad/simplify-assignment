"""Data models for the application."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Chat message model."""
    user_message: str
    ai_response: str
    timestamp: datetime = Field(default_factory=datetime.now)


class PurchaseRequest(BaseModel):
    """Purchase request model."""
    user_name: Optional[str] = "Guest User"
    amount: float = 10.0  # Fixed ₹10 as per requirement


class PurchaseRecord(BaseModel):
    """Purchase record model for MongoDB."""
    user_name: str
    amount: float
    currency: str = "INR"
    timestamp: datetime = Field(default_factory=datetime.now)
    transaction_id: str
    status: str = "completed"


class ChatRequest(BaseModel):
    """Chat request model."""
    message: str
