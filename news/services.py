import requests
from django.conf import settings


class MarketauxService:
    """Service class to interact with Marketaux API"""
    
    BASE_URL = "https://api.marketaux.com/v1/news/all"
    API_TOKEN = "Uxs697fzFjP4WCcYScFzuwXoRyjrH5eD687MwGl2"
    
    @classmethod
    def get_news(cls, symbols=None, limit=10):
        """
        Fetch news from Marketaux API
        
        Args:
            symbols: Comma-separated stock symbols (e.g., "TSLA,AMZN,MSFT")
            limit: Number of results to return
            
        Returns:
            dict: API response with news data
        """
        params = {
            "api_token": cls.API_TOKEN,
            "filter_entities": "true",
            "language": "en",
            "limit": limit,
        }
        
        if symbols:
            params["symbols"] = symbols
        else:
            params["symbols"] = "TSLA,AMZN,MSFT"
        
        try:
            response = requests.get(cls.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            error_msg = f"Error fetching news: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                error_msg += f" (Status: {e.response.status_code}, Body: {e.response.text})"
            print(error_msg)
            return {"meta": {}, "data": [], "error": error_msg}
    
    @classmethod
    def get_sentiment_class(cls, score):
        """Return CSS class based on sentiment score"""
        if score is None:
            return "neutral"
        if score >= 0.5:
            return "positive"
        elif score <= -0.3:
            return "negative"
        return "neutral"

    @classmethod
    def get_market_sentiment(cls):
        """
        Fetch market sentiment aggregation
        """
        url = "https://api.marketaux.com/v1/entity/stats/aggregation"
        params = {
            "api_token": cls.API_TOKEN,
            "countries": "us",
            "group_by": "country",
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching sentiment: {e}")
            return {"data": []}
