"""FastAPI application for Kuberi Gold Investment workflow."""
import uuid
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse

from app.models import ChatRequest, PurchaseRequest, PurchaseRecord, ChatMessage
from app.database import get_purchases_collection, get_chat_history_collection
from app.ai_service import gemini_service

# Initialize FastAPI app
app = FastAPI(title="Kuberi Gold Investment App")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the main chat interface."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/chat")
async def chat(chat_request: ChatRequest):
    """
    Process user question about gold investments using Google Gemini.
    
    Args:
        chat_request: User's question
        
    Returns:
        AI-generated response with investment nudge
    """
    try:
        # Get AI response from Gemini
        ai_response = gemini_service.get_response(chat_request.message)
        
        # Store chat history in MongoDB
        chat_message = ChatMessage(
            user_message=chat_request.message,
            ai_response=ai_response
        )
        
        chat_collection = get_chat_history_collection()
        chat_collection.insert_one(chat_message.model_dump())
        
        return JSONResponse({
            "response": ai_response,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")


@app.get("/api/gold-price")
async def get_gold_price():
    """
    Get current real-time gold price.
    
    Returns:
        JSON with current price per gram (24K)
    """
    import random
    # Simulate live gold price fluctuation around ₹7,200
    base_price = 7200.0
    fluctuation = random.uniform(-10.0, 10.0)
    current_price = base_price + fluctuation
    
    return JSONResponse({
        "success": True,
        "price_per_gram": round(current_price, 2),
        "currency": "INR",
        "timestamp": datetime.now().isoformat()
    })


@app.post("/api/purchase")
async def purchase_gold(purchase_request: PurchaseRequest):
    """
    Process digital gold purchase (₹10).
    
    Args:
        purchase_request: Purchase details
        
    Returns:
        Purchase confirmation with transaction ID
    """
    try:
        # Generate unique transaction ID
        transaction_id = f"TXN{uuid.uuid4().hex[:12].upper()}"
        
        # Create purchase record
        purchase_record = PurchaseRecord(
            user_name=purchase_request.user_name,
            amount=purchase_request.amount,
            transaction_id=transaction_id
        )
        
        # Store in MongoDB
        purchases_collection = get_purchases_collection()
        result = purchases_collection.insert_one(purchase_record.model_dump())
        
        return JSONResponse({
            "success": True,
            "transaction_id": transaction_id,
            "amount": purchase_request.amount,
            "currency": "INR",
            "timestamp": datetime.now().isoformat(),
            "message": "Digital gold purchase successful!"
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing purchase: {str(e)}")


@app.get("/success", response_class=HTMLResponse)
async def success_page(request: Request, transaction_id: str = ""):
    """
    Display purchase success confirmation page.
    
    Args:
        request: FastAPI request
        transaction_id: Transaction ID from purchase
    """
    return templates.TemplateResponse(
        "success.html",
        {
            "request": request,
            "transaction_id": transaction_id,
            "amount": 10.0,
            "currency": "INR"
        }
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Kuberi Gold Investment App"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
