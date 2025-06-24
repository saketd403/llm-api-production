from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import os
import logging
from dotenv import load_dotenv
import uvicorn

from summarizer_service import SummarizerService
from schema_classes import SummarizeResponse, SummarizeRequest

logger = logging.getLogger(__name__)

def setup_logging():

    file_handler = logging.FileHandler('main.log',mode='w',encoding='utf-8')
    console_handler = logging.StreamHandler()
    
    # Create formatters and add it to handlers
    log_format = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    file_handler.setFormatter(log_format)
    console_handler.setFormatter(log_format)
    
    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, console_handler]   
    )

load_dotenv()

# This dictionary will hold our singleton service instance
app_state = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup logging
    setup_logging()
    # This code runs on startup
    logger.info("Application startup...")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set in environment. Application cannot start.")
    
    app_state["summarizer_service"] = SummarizerService(api_key=api_key)
    logger.info("Summarizer service initialized.")
    yield
    # This code runs on shutdown
    logger.info("Application shutdown...")
    app_state.clear()


app = FastAPI(lifespan=lifespan)

@app.get("/health", status_code=200)
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}
   
@app.post("/summarize", response_model=SummarizeResponse)
async def summarize(request: SummarizeRequest):
    service = app_state.get("summarizer_service")
    if not service:
        raise HTTPException(status_code=503, detail="Service not available. Please try again later.")
    
    try:
        summary = await service.asummarize(request.text)
        return SummarizeResponse(summary=summary)
    except Exception as e:
        # It's better to log the full exception here for debugging
        logger.error(f"Error occured while processing request:\n{str(e)}")
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {e}")
    

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)