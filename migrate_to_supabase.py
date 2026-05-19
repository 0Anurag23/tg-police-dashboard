import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from db.database import Article, Base, engine as sqlite_engine

# Your Supabase connection string
SUPABASE_URL = "postgresql://postgres.enhuqacwlmsudqlalxle:UsingaDatabase%4011@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"

# Create Supabase engine
supabase_engine = create_engine(SUPABASE_URL)

# Create tables in Supabase
Base.metadata.create_all(supabase_engine)
print("✅ Tables created in Supabase")

# Copy all articles from SQLite to Supabase
with Session(sqlite_engine) as sqlite_session:
    articles = sqlite_session.query(Article).all()
    print(f"📰 Found {len(articles)} articles in SQLite")

with Session(supabase_engine) as supabase_session:
    saved = 0
    for article in articles:
        existing = supabase_session.get(Article, article.id)
        if not existing:
            supabase_session.add(Article(
                id=article.id,
                title=article.title,
                url=article.url,
                source=article.source,
                body=article.body,
                date=article.date,
                category=article.category,
                summary=article.summary,
                tags=article.tags,
            ))
            saved += 1
    supabase_session.commit()
    print(f"✅ Migrated {saved} articles to Supabase!")