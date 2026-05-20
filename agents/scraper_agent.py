from datetime import datetime
import requests, re
from xml.etree import ElementTree

def extract_source_name(title: str) -> str:
    """Extract newspaper name from Google News title format: 'Headline - Source Name'"""
    if ' - ' in title:
        return title.split(' - ')[-1].strip()
    return "Google News"

def clean_html(text):
    """Strip HTML tags and entities from text."""
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

SOURCES = [
    # Existing general feeds
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
    },

    # ── District specific feeds ──────────────────────────────────
    {
        "name": "district_warangal_Urban",
        "url": "https://news.google.com/rss/search?q=Warangal+Urban+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_Warangal_rural",
        "url": "https://news.google.com/rss/search?q=Warangal+Rural+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_karimnagar",
        "url": "https://news.google.com/rss/search?q=Karimnagar+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_nizamabad",
        "url": "https://news.google.com/rss/search?q=Nizamabad+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_khammam",
        "url": "https://news.google.com/rss/search?q=Khammam+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_nalgonda",
        "url": "https://news.google.com/rss/search?q=Nalgonda+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_mahbubnagar",
        "url": "https://news.google.com/rss/search?q=Mahbubnagar+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_adilabad",
        "url": "https://news.google.com/rss/search?q=Adilabad+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_medak",
        "url": "https://news.google.com/rss/search?q=Medak+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_rangareddy",
        "url": "https://news.google.com/rss/search?q=Rangareddy+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_siddipet",
        "url": "https://news.google.com/rss/search?q=Siddipet+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_sangareddy",
        "url": "https://news.google.com/rss/search?q=Sangareddy+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_mancherial",
        "url": "https://news.google.com/rss/search?q=Mancherial+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_jagtial",
        "url": "https://news.google.com/rss/search?q=Jagtial+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_peddapalli",
        "url": "https://news.google.com/rss/search?q=Peddapalli+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_kamareddy",
        "url": "https://news.google.com/rss/search?q=Kamareddy+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_nirmal",
        "url": "https://news.google.com/rss/search?q=Nirmal+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_suryapet",
        "url": "https://news.google.com/rss/search?q=Suryapet+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_nagarkurnool",
        "url": "https://news.google.com/rss/search?q=Nagarkurnool+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_wanaparthy",
        "url": "https://news.google.com/rss/search?q=Wanaparthy+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_jogulamba",
        "url": "https://news.google.com/rss/search?q=Jogulamba+Gadwal+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_vikarabad",
        "url": "https://news.google.com/rss/search?q=Vikarabad+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_mahabubabad",
        "url": "https://news.google.com/rss/search?q=Mahabubabad+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_jangaon",
        "url": "https://news.google.com/rss/search?q=Jangaon+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_bhadradri",
        "url": "https://news.google.com/rss/search?q=Bhadradri+Kothagudem+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_mulugu",
        "url": "https://news.google.com/rss/search?q=Mulugu+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_jayashankar",
        "url": "https://news.google.com/rss/search?q=Jayashankar+Bhupalpally+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_narayanpet",
        "url": "https://news.google.com/rss/search?q=Narayanpet+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_yadadri",
        "url": "https://news.google.com/rss/search?q=Yadadri+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_kumuram_bheem",
        "url": "https://news.google.com/rss/search?q=Kumuram+Bheem+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_medchal",
        "url": "https://news.google.com/rss/search?q=Medchal+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
    {
        "name": "district_rajanna_sircilla",
        "url": "https://news.google.com/rss/search?q=Rajanna+Sircilla+Police&hl=en-IN&gl=IN&ceid=IN:en",
        "source": "Google News"
    },
]

def scrape_rss(feed_url, source_name):
    print(f"📡 Fetching RSS: {feed_url[:60]}...")
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(feed_url, headers=headers, timeout=15)
    root = ElementTree.fromstring(resp.content)
    
    articles = []
    for item in root.findall(".//item"):
        raw_title = item.findtext("title", "").strip()
        title = raw_title.split(' - ')[0].strip() if ' - ' in raw_title else raw_title
        source_name = extract_source_name(raw_title)
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