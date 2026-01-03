# Kuberi AI Gold Investment App

A mini web application that emulates the Kuberi AI gold investment workflow from Simplify Money app. Built with FastAPI, Google Gemini AI, and MongoDB.

## Features

- 💬 **AI-Powered Chat**: Ask questions about gold investments and get intelligent responses
- 🤖 **Google Gemini Integration**: Uses Gemini AI to understand and respond to user queries
- 💰 **Digital Gold Purchase**: Invest ₹10 in digital gold with a single click
- 📊 **MongoDB Storage**: All purchases and chat history stored in MongoDB
- ✨ **Premium UI**: Modern, responsive design with smooth animations
- ✅ **Purchase Confirmation**: Beautiful success page with transaction details

## Tech Stack

- **Backend**: FastAPI (Python)
- **AI**: Google Gemini (google-generativeai SDK)
- **Database**: MongoDB
- **DB Client**: PyMongo
- **UI**: HTML + CSS (Jinja2 templates)

## Prerequisites

- Python 3.8+
- MongoDB (running locally on port 27017)
- Google Gemini API Key

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd kuberi-gold-app
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Google Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   MONGODB_URL=mongodb://localhost:27017/
   DATABASE_NAME=kuberi_gold
   ```

5. **Start MongoDB** (if not already running):
   ```bash
   mongod
   ```

## Running the Application

1. **Start the FastAPI server**:
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:8000
   ```

## Usage

1. **Ask Questions**: Type questions about gold investments in the chat interface
2. **Get AI Responses**: Kuberi AI will provide helpful, factually correct answers
3. **Investment Nudge**: The AI will naturally suggest investing in digital gold
4. **Purchase Gold**: Click the "Invest ₹10 in Digital Gold" button when it appears
5. **Confirmation**: View your purchase confirmation with transaction details

## API Endpoints

- `GET /` - Main chat interface
- `POST /api/chat` - Process user questions (expects JSON: `{"message": "your question"}`)
- `POST /api/purchase` - Process gold purchase (expects JSON: `{"user_name": "name", "amount": 10.0}`)
- `GET /success?transaction_id=xxx` - Purchase success page
- `GET /health` - Health check endpoint

## Project Structure

```
kuberi-gold-app/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic models
│   ├── database.py          # MongoDB connection
│   ├── ai_service.py        # Google Gemini integration
│   └── templates/
│       ├── index.html       # Chat interface
│       └── success.html     # Purchase confirmation
├── static/
│   └── style.css            # Premium styling
├── requirements.txt
├── .env.example
└── README.md
```

## Database Collections

- **purchases**: Stores all gold purchase transactions
- **chat_history**: Stores all chat conversations

## Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `MONGODB_URL`: MongoDB connection URL (default: `mongodb://localhost:27017/`)
- `DATABASE_NAME`: Database name (default: `kuberi_gold`)

## MongoDB Atlas Setup (Required for Data Persistence)

To store transactions and chat history, set up a free MongoDB Atlas cluster:

### 1. Create MongoDB Atlas Account
- Go to [mongodb.com/atlas](https://www.mongodb.com/atlas) and sign up (free)
- Create a new **Shared Cluster** (free tier)

### 2. Configure Database Access
- Go to **Database Access** → **Add New Database User**
- Create username and password (save these!)
- Set privileges to **"Read and write to any database"**

### 3. Configure Network Access
- Go to **Network Access** → **Add IP Address**
- Click **"Allow Access from Anywhere"** (adds `0.0.0.0/0`)

### 4. Get Connection String
- Go to **Database** → Click **Connect** → **"Connect your application"**
- Copy the connection string:
  ```
  mongodb+srv://username:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
  ```
- Replace `<password>` with your actual password

## Docker Hub

Pull and run the pre-built image from Docker Hub:

```bash
# Pull the image
docker pull alwaysahad/kuberi-gold-app:latest

# Run the container (with MongoDB for data persistence)
docker run -d -p 8000:8000 \
  -e GEMINI_API_KEY=your_gemini_api_key \
  -e MONGODB_URL="mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority" \
  -e DATABASE_NAME=kuberi_gold \
  alwaysahad/kuberi-gold-app
```

Then open http://localhost:8000 in your browser.

> **Note:** Replace `your_gemini_api_key` and the MongoDB connection string with your actual credentials.

## Development

To run in development mode with auto-reload:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## License

MIT License
