from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import news, chat

app = FastAPI(title="Kids Activity Runner API", version="1.0.0")

origins = [
    "http://localhost:8501",
    "https://your-streamlit-app-name.streamlit.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# registering the routers in main
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(news.router, prefix="/api", tags=["news"])



@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "kids-activity-runner",
        "version": "1.0.0"
    }