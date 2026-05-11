import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from newspaper import Article as NewsArticle
import time
import requests
from newspaper import Article as NewsArticle
import time

def fetch_full_article(url: str) -> str:
    """Fetch full article text from a URL."""
    try:
        article = NewsArticle(url, request_timeout=10)
        article.download()
        article.parse()
        
        text = article.text.strip()
        
        # If newspaper3k got nothing, fall back to requests
        if not text or len(text) < 100:
            return fetch_fallback(url)
            
        return text[:3000]  # limit to 3000 chars to save tokens
    
    except Exception as e:
        print(f"     Could not fetch {url[:50]}: {e}")
        return ""

def fetch_fallback(url: str) -> str:
    """Simple fallback using requests + basic text extraction."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        # Strip HTML tags roughly
        import re
        text = re.sub(r'<[^>]+>', ' ', resp.text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:3000]
    except:
        return ""

def enrich_articles_in_db(limit: int = 20):
    """Fetch full text for articles that only have snippet bodies."""
    from sqlalchemy.orm import Session
    from db.database import engine, Article
    
    with Session(engine) as session:
        # Get articles with short bodies (snippets, not full text)
        articles = (
            session.query(Article)
            .filter(Article.body.isnot(None))
            .filter(Article.body != "")
            .all()
        )
        
        short_articles = [a for a in articles if len(a.body) < 300][:limit]
        print(f"Found {len(short_articles)} articles with short bodies to enrich")
        
        for i, article in enumerate(short_articles):
            print(f"[{i+1}/{len(short_articles)}] Fetching: {article.title[:55]}...")
            full_text = fetch_full_article(article.url)
            
            if full_text and len(full_text) > len(article.body):
                article.body = full_text
                session.commit()
                print(f"   Enriched ({len(full_text)} chars)")
            else:
                print(f"   Skipped (no better text found)")
            
            time.sleep(1)  # be polite, don't hammer servers
        
        print(f"\nEnrichment complete!")

if __name__ == "__main__":
    enrich_articles_in_db(limit=20)