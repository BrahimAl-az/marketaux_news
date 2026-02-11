import csv
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .services import MarketauxService


def index(request):
    """Main view to display stock news"""
    
    # Get symbols from query params or use defaults
    symbols = request.GET.get('symbols', 'TSLA,AMZN,MSFT')
    
    # Available symbols for filtering
    available_symbols = ['TSLA', 'AMZN', 'MSFT', 'AAPL', 'GOOGL', 'META', 'NVDA']
    
    # Fetch news from API
    response = MarketauxService.get_news(symbols=symbols)
    sentiment_response = MarketauxService.get_market_sentiment()
    sentiment_data = sentiment_response.get('data', [])
    market_sentiment = sentiment_data[0].get('sentiment_avg', 0) if sentiment_data else 0
    market_sentiment_class = MarketauxService.get_sentiment_class(market_sentiment)

    news_data = response.get('data', [])
    meta = response.get('meta', {})
    
    # Process news items to add sentiment classes
    for item in news_data:
        for entity in item.get('entities', []):
            entity['sentiment_class'] = MarketauxService.get_sentiment_class(
                entity.get('sentiment_score')
            )
    
    # Parse current symbols for active state
    current_symbols = [s.strip().upper() for s in symbols.split(',')]
    
    context = {
        'news_items': news_data,
        'market_sentiment': market_sentiment,
        'market_sentiment_class': market_sentiment_class,
        'meta': meta,
        'available_symbols': available_symbols,
        'current_symbols': current_symbols,
        'symbols_param': symbols,
        'error': response.get('error'),
    }
    
    return render(request, 'news/index.html', context)
