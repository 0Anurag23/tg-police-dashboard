from agents.scraper_agent import scrape_all
from db.database import init_db, save_article

def main():
    init_db()
    print("🔍 Scraping TG Police news...")
    articles = scrape_all()
    print(f"Found {len(articles)} articles")

    saved = 0
    skipped = 0
    for article in articles:
        if save_article(article):
            saved += 1
        else:
            skipped += 1

    print(f"\nDone! {saved} new articles saved, {skipped} duplicates skipped.")
    print(f"Database: data/news.db")

if __name__ == "__main__":
    main()