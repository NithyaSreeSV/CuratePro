from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from news_fetcher import NewsFetcher
from post_summarizer import PostSummarizer

load_dotenv()

app = FastAPI(title="LinkedIn Content Curator API")

# Enable CORS so our frontend can securely talk to the backend engine
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows local file viewing/frontend testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the expected JSON format for incoming data
class CurationRequest(BaseModel):
    feed_url: str
    tone: str

@app.post("/api/curate")
async def curate_content(request: CurationRequest):
    try:
        # Reusing our core OOP classes inside the web route
        fetcher = NewsFetcher(request.feed_url)
        summarizer = PostSummarizer()
        
        # 1. Fetching the article data
        article = fetcher.fetch_latest_article()
        
        # 2. Piping the content to Gemini with the requested tone
        draft = summarizer.generate_draft(
            article_title=article['title'], 
            article_context=article['summary'], 
            tone=request.tone
        )
        
        return {
            "status": "success",
            "title": article['title'],
            "source_link": article['link'],
            "draft": draft
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def serve_frontend():
    return FileResponse("frontend/index.html")


if __name__ == "__main__":
    import uvicorn
    import os
    # Dynamically read the port assigned by Render, defaulting to 8000 locally
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)