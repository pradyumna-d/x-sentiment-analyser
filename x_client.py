"""Tweepy wrapper for X API v2 recent search."""
import tweepy
from typing import List, Dict, Optional
from config import BEARER_TOKEN


class XClient:
    """Simple wrapper for X API v2 recent search."""
    
    def __init__(self):
        self.client = tweepy.Client(bearer_token=BEARER_TOKEN)
    
    def search_recent(
        self, 
        query: str, 
        count: int = 10, 
        lang: Optional[str] = None
    ) -> List[Dict]:
        """
        Search recent tweets using X API v2.
        
        Args:
            query: Search keyword or hashtag
            count: Number of tweets (max 20)
            lang: Language code (optional)
        
        Returns:
            List of tweet dictionaries with id, text, author_id, created_at
        """
        max_results = min(count, 20)
        tweet_fields = ["created_at", "author_id"]
        expansions = ["author_id"]
        user_fields = ["username"]
        
        try:
            response = self.client.search_recent_tweets(
                query=query,
                max_results=max_results,
                tweet_fields=tweet_fields,
                expansions=expansions,
                user_fields=user_fields,
                lang=lang
            )
            
            if not response.data:
                return []
            
            tweets = []
            users = {}
            if response.includes and "users" in response.includes:
                users = {u.id: u.username for u in response.includes["users"]}
            
            for tweet in response.data:
                tweets.append({
                    "id": tweet.id,
                    "text": tweet.text,
                    "author": users.get(tweet.author_id, "unknown"),
                    "created_at": tweet.created_at.isoformat() if tweet.created_at else None
                })
            
            return tweets
        except tweepy.TooManyRequests:
            raise
        except Exception as e:
            raise Exception(f"X API error: {str(e)}")

