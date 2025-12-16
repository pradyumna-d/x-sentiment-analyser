# X Sentiment API

A minimal, production-ready FastAPI backend for on-demand sentiment analysis of recent X (Twitter) posts using the free X API v2 tier.

## Features

- REST JSON API endpoints only (no frontend)
- On-demand X API calls (preserves free tier limits)
- Sentiment analysis using `cardiffnlp/twitter-roberta-base-sentiment-latest`
- CPU-based inference (no GPU required)
- Clean, minimal codebase (< 250 lines)

## Getting a Free X Bearer Token

1. Go to [https://developer.twitter.com/](https://developer.twitter.com/)
2. Sign in with your X (Twitter) account
3. Navigate to the **Developer Portal** → **Projects & Apps**
4. Create a new **Project** (or use an existing one)
5. Create a new **App** within your project
6. Go to **Keys and tokens** tab
7. Under **Bearer Token**, click **Generate** (or **Regenerate** if you already have one)
8. Copy the Bearer Token immediately (it's only shown once)

**Note:** The free tier provides 100 requests/month. This API only calls X when endpoints are hit, making it perfect for the free tier.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create a `.env` file** in the project root:
   ```bash
   BEARER_TOKEN=your_bearer_token_here
   ```
   
   **Example `.env` file:**
   ```
   BEARER_TOKEN=your_bearer_token_here
   ```

3. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`

## API Endpoints

### GET `/`
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "message": "X Sentiment API ready"
}
```

### GET `/api/search`
Search recent tweets and perform sentiment analysis.

**Query Parameters:**
- `q` (required): Search keyword or hashtag (e.g., "python" or "#AI")
- `count` (optional, default 10, max 20): Number of tweets to analyze
- `lang` (optional): Language code (e.g., "en")

**Example Requests:**
```bash
curl "http://localhost:8000/api/search?q=python&count=15"
curl "http://localhost:8000/api/search?q=%23AI&lang=en"
```

**Response:**
```json
{
  "query": "python",
  "total_results": 12,
  "tweets": [
    {
      "id": "123456789",
      "author": "username",
      "text": "original tweet text...",
      "cleaned_text": "text used for analysis",
      "sentiment": "POSITIVE",
      "confidence": 0.97,
      "created_at": "2025-11-26T12:34:56Z"
    }
  ],
  "summary": {
    "positive": 7,
    "negative": 3,
    "neutral": 2
  }
}
```

**Error Responses:**
- `400`: Missing or invalid query parameter
- `429`: X API rate limit exceeded (includes `Retry-After` header)
- `500`: Internal server error

## Project Structure

```
├── main.py              # FastAPI app + all routes
├── x_client.py          # Tweepy wrapper for X API
├── sentiment.py         # Sentiment analyzer singleton
├── config.py            # Environment variable loading
├── requirements.txt     # Python dependencies
├── README.md           
└── .env                
```

## Notes

- The sentiment model is loaded once at startup for optimal performance
- Tweets are cleaned (URLs, @mentions, #hashtags removed) before analysis
- The API searches tweets from the last 7 days (X API v2 limitation)
- All sentiment analysis runs on CPU (no GPU required)

