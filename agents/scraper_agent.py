from datetime import datetime
import requests, re
from xml.etree import ElementTree

def clean_html(text):
    """Strip HTML tags and entities from text."""
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

SOURCES = [
    {
        "name": "google_news_tg_police",
        "url": "https://news.google.com/rss/search?q=Telangana+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "google_news_tg_police_hyderabad",
        "url": "https://news.google.com/rss/search?q=TS+Police+Hyderabad&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "google_news_tg_crime",
        "url": "https://news.google.com/rss/search?q=Telangana+crime+arrest&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "google_news_hyd_police",
        "url": "https://news.google.com/rss/search?q=Hyderabad+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "google_news_tg_drugs",
        "url": "https://news.google.com/rss/search?q=Telangana+drugs+NDPS&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "google_news_tg_recruitment",
        "url": "https://news.google.com/rss/search?q=Telangana+Police+recruitment&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    }
]

def scrape_rss(feed_url, source_name):
    print(f"📡 Fetching RSS: {feed_url[:60]}...")
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(feed_url, headers=headers, timeout=15)
    root = ElementTree.fromstring(resp.content)
    
    articles = []
    for item in root.findall(".//item"):
        title = item.findtext("title", "").strip()
        url   = item.findtext("link", "").strip()
        date  = item.findtext("pubDate", datetime.now().strftime("%Y-%m-%d"))
        desc = clean_html(item.findtext("description", "")).strip()
        
        if title and url:
            articles.append({
                "title": title,
                "url": url,
                "date": date,
                "body": desc,
                "source": source_name
            })
    return articles

def scrape_all():
    all_articles = []
    seen_urls = set()
    
    for source in SOURCES:
        try:
            articles = scrape_rss(source["url"], source["source"])
            for a in articles:
                if a["url"] not in seen_urls:
                    seen_urls.add(a["url"])
                    all_articles.append(a)
            print(f"  Got {len(articles)} articles from {source['name']}")
        except Exception as e:
            print(f"  Failed {source['name']}: {e}")
    
    return all_articles

if __name__ == "__main__":
    articles = scrape_all()
    print(f"\nTotal unique articles: {len(articles)}")
    for a in articles[:5]:
        print(f"  → {a['title'][:70]}")