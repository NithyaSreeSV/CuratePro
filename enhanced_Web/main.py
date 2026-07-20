from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from fetcher import UniversalWebFetcher
from summarizer import PostSummarizer

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CurationRequest(BaseModel):
    url: str
    tone: str
    format_style: str

@app.post("/enhanced_Web/api/curate")
@app.post("/api/curate")
async def curate_content(request: CurationRequest):
    try:
        fetcher = UniversalWebFetcher(request.url)
        summarizer = PostSummarizer()
        
        article = fetcher.fetch_web_content()
        
        draft = summarizer.generate_draft(
            article_title=article['title'], 
            article_context=article['summary'], 
            tone=request.tone,
            format_style=request.format_style
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

    port = int(os.environ.get("PORT", 8001))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
