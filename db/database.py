from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.orm import declarative_base, Session
from email.utils import parsedate_to_datetime
import datetime, hashlib, os

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"
    id       = Column(String, primary_key=True)
    title    = Column(String)
    url      = Column(String, unique=True)
    source   = Column(String)
    body     = Column(Text)
    date     = Column(DateTime, default=datetime.datetime.utcnow)
    category = Column(String, default="Uncategorized")
    summary  = Column(Text, default="")
    tags     = Column(String, default="")

DB_PATH = os.path.join(os.path.dirname(__file__), "../data/news.db")
engine  = create_engine(f"sqlite:///{DB_PATH}")

def init_db():
    Base.metadata.create_all(engine)
    print("Database ready at data/news.db")

def save_article(data: dict):
    uid = hashlib.md5(data["url"].encode()).hexdigest()

    # Convert date string to datetime object
    date = data.get("date")
    if isinstance(date, str):
        try:
            date = parsedate_to_datetime(date)
        except:
            date = datetime.datetime.utcnow()

    with Session(engine) as session:
        if session.get(Article, uid):
            return False
        session.add(Article(
            id=uid,
            title=data.get("title", ""),
            url=data.get("url", ""),
            source=data.get("source", ""),
            body=data.get("body", ""),
            date=date,
            category=data.get("category", "Uncategorized"),
            summary=data.get("summary", ""),
            tags=data.get("tags", ""),
        ))
        session.commit()
        return True

if __name__ == "__main__":
    init_db()