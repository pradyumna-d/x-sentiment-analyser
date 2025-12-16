"""Sentiment analyzer using Hugging Face model."""
import re
from typing import Dict, Tuple
from transformers import pipeline


class SentimentAnalyzer:
    """Singleton sentiment analyzer for tweet sentiment."""
    
    _instance = None
    _model = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._model is None:
            self._model = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=-1  # CPU
            )
            SentimentAnalyzer._model = self._model
    
    def clean_tweet(self, text: str) -> str:
        """
        Clean tweet text by removing URLs, @mentions, #hashtags, extra whitespace.
        
        Args:
            text: Original tweet text
        
        Returns:
            Cleaned text
        """
        # Remove URLs
        text = re.sub(r'http\S+|www\.\S+', '', text)
        # Remove @mentions
        text = re.sub(r'@\w+', '', text)
        # Remove #hashtags (but keep the word)
        text = re.sub(r'#(\w+)', r'\1', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text.strip()
    
    def analyze(self, text: str) -> Tuple[str, float]:
        """
        Analyze sentiment of cleaned text.
        
        Args:
            text: Text to analyze
        
        Returns:
            Tuple of (sentiment_label, confidence_score)
        """
        if not text:
            return "NEUTRAL", 0.5
        
        cleaned = self.clean_tweet(text)
        if not cleaned:
            return "NEUTRAL", 0.5
        
        result = self._model(cleaned)[0]
        label = result["label"].upper()
        score = result["score"]
        
        # Map model labels to our format
        # distilbert-sst-2 uses "POSITIVE" and "NEGATIVE" labels
        if "POSITIVE" in label or label == "POS" or label == "LABEL_1":
            return "POSITIVE", score
        elif "NEGATIVE" in label or label == "NEG" or label == "LABEL_0":
            return "NEGATIVE", score
        else:
            # Default to neutral if label doesn't match
            return "NEUTRAL", score

