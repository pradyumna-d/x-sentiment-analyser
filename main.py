"""FastAPI application for X sentiment analysis."""
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import tweepy
from x_client import XClient
from sentiment import SentimentAnalyzer

app = FastAPI(title="X Sentiment API", version="1.0.0")

# Configure CORS to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients (singleton pattern for sentiment analyzer)
x_client = XClient()
sentiment_analyzer = SentimentAnalyzer()


@app.get("/")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "X Sentiment API ready"}


@app.get("/api/search")
async def search_tweets(
    q: str = Query(..., description="Search keyword or hashtag"),
    count: int = Query(10, ge=1, le=20, description="Number of tweets (max 20)"),
    lang: Optional[str] = Query(None, description="Language code (e.g., 'en')")
):
    """
    Search recent tweets and perform sentiment analysis.
    
    Returns tweets with sentiment labels and confidence scores.
    """
    try:
        # Fetch tweets from X API
        tweets = x_client.search_recent(query=q, count=count, lang=lang)
        
        # Analyze sentiment for each tweet
        results = []
        summary = {"positive": 0, "negative": 0, "neutral": 0}
        
        for tweet in tweets:
            sentiment, confidence = sentiment_analyzer.analyze(tweet["text"])
            cleaned_text = sentiment_analyzer.clean_tweet(tweet["text"])
            
            results.append({
                "id": str(tweet["id"]),
                "author": tweet["author"],
                "text": tweet["text"],
                "cleaned_text": cleaned_text,
                "sentiment": sentiment,
                "confidence": round(confidence, 2),
                "created_at": tweet["created_at"]
            })
            
            summary[sentiment.lower()] += 1
        
        return {
            "query": q,
            "total_results": len(results),
            "tweets": results,
            "summary": summary
        }
    
    except tweepy.TooManyRequests:
        return JSONResponse(
            status_code=429,
            content={"error": "X API rate limit exceeded"},
            headers={"Retry-After": "900"}  # 15 minutes
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

