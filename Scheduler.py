import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import schedule
import time
import subprocess
import sys
import os

sys.path.append('/opt/ai-projects/23-TG-Police-News')

from agents.scraper_agent import scrape_all
from agents.article_fetcher import enrich_articles_in_db
from pipeline.crew_pipeline import run_pipeline
from db.database import init_db

def run_full_pipeline():
    """Full cycle: scrape → enrich → process → done."""
    print("\n" + "="*50)
    print("🔄 Starting scheduled pipeline run...")
    print("="*50)

    # Step 1 — Scrape new articles
    print("\n📡 Step 1: Scraping new articles...")
    from db.database import save_article
    articles = scrape_all()
    saved = sum(1 for a in articles if save_article(a))
    print(f"✅ {saved} new articles scraped and saved")

    # Step 2 — Enrich with full text
    print("\n📰 Step 2: Fetching full article text...")
    enrich_articles_in_db(limit=50)

    # Step 3 — Process with crewAI
    print("\n🤖 Step 3: Running crewAI pipeline...")
    run_pipeline(limit=100)

    print("\n✨ Scheduled run complete!")
    print("="*50)

# Run immediately on start
run_full_pipeline()

# Then schedule every 6 hours
schedule.every(6).hours.do(run_full_pipeline)

print("\n⏰ Scheduler running — pipeline will refresh every 6 hours")
print("Press Ctrl+C to stop\n")

while True:
    schedule.run_pending()
    time.sleep(60)