from crewai import Agent, Task, Crew, LLM
from sqlalchemy.orm import Session
from db.database import engine, Article

# Connect crewAI to your local Qwen model
llm = LLM(model="ollama/qwen2.5:7b-instruct", base_url="http://localhost:11434")

# ── Agent 1: Categorizer ──────────────────────────────────────────
categorizer = Agent(
    role="News Categorizer",
    goal="Categorize Telangana Police news articles into one of these: Crime, Drugs, Recruitment, Awards, Infrastructure, Awareness, Other",
    backstory="You are an expert at reading police news and instantly knowing what category it belongs to.",
    llm=llm,
    verbose=False,
)

# ── Agent 2: Summarizer ───────────────────────────────────────────
summarizer = Agent(
    role="News Summarizer",
    goal="Write a clean 3-line summary of a news article",
    backstory="You are a news editor who writes crisp, accurate summaries for busy readers.",
    llm=llm,
    verbose=False,
)

# ── Agent 3: Tag Extractor ────────────────────────────────────────
tagger = Agent(
    role="Tag Extractor",
    goal="Extract relevant tags from a news article like district names, keywords, and people mentioned",
    backstory="You extract searchable keywords from news articles to help readers find related stories.",
    llm=llm,
    verbose=False,
)

def process_article(title: str, body: str):
    """Run one article through all 3 agents and return results."""

    task_categorize = Task(
        description=f"""
        Read this Telangana Police news article and return ONLY one category word.
        Choose from: Crime, Drugs, Recruitment, Awards, Infrastructure, Awareness, Other
        
        Title: {title}
        Body: {body[:500]}
        
        Reply with just the category word. Nothing else.
        """,
        expected_output="One word category from: Crime, Drugs, Recruitment, Awards, Infrastructure, Awareness, Other",
        agent=categorizer,
    )

    task_summarize = Task(
        description=f"""
        Write a 3-line summary of this Telangana Police news article.
        Be factual and concise. No fluff.
        
        Title: {title}
        Body: {body[:1000]}
        
        Reply with exactly 3 lines. Nothing else.
        """,
        expected_output="A 3-line factual summary of the article",
        agent=summarizer,
    )

    task_tag = Task(
        description=f"""
        Extract 3-5 tags from this Telangana Police news article.
        Tags should be: district names, crime types, or key topics.
        
        Title: {title}
        Body: {body[:500]}
        
        Reply with tags separated by commas. Example: Hyderabad, Drugs, NDPS Act
        Nothing else.
        """,
        expected_output="3-5 comma separated tags",
        agent=tagger,
    )

    crew = Crew(
        agents=[categorizer, summarizer, tagger],
        tasks=[task_categorize, task_summarize, task_tag],
        verbose=False,
    )

    result = crew.kickoff()
    outputs = [t.output.raw.strip() for t in crew.tasks]

    return {
        "category": outputs[0] if len(outputs) > 0 else "Other",
        "summary":  outputs[1] if len(outputs) > 1 else "",
        "tags":     outputs[2] if len(outputs) > 2 else "",
    }

def run_pipeline(limit: int = 200):
    """Process unprocessed articles from the database."""
    with Session(engine) as session:
        articles = (
            session.query(Article)
            .filter(Article.summary == "")
            .limit(limit)
            .all()
        )

        print(f"Processing {len(articles)} articles with crewAI + Qwen...")

        for i, article in enumerate(articles):
            print(f"\n[{i+1}/{len(articles)}] {article.title[:60]}...")
            try:
                result = process_article(article.title, article.body)
                article.category = result["category"]
                article.summary  = result["summary"]
                article.tags     = result["tags"]
                session.commit()
                print(f"  Category: {result['category']}")
                print(f"  Tags: {result['tags']}")
            except Exception as e:
                print(f"  Failed: {e}")
                continue

        print(f"\n Pipeline complete!")

  
def reprocess_enriched(limit: int = 20):
    """Reprocess articles that now have full text."""
    with Session(engine) as session:
        articles = (
            session.query(Article)
            .filter(Article.summary != "")
            .filter(Article.body.isnot(None))
            .all()
        )
        enriched = [a for a in articles if len(a.body) > 300][:limit]
        print(f"🔄 Reprocessing {len(enriched)} enriched articles...")

        for i, article in enumerate(enriched):
            print(f"\n[{i+1}/{len(enriched)}] {article.title[:60]}...")
            try:
                result = process_article(article.title, article.body)
                article.category = result["category"]
                article.summary  = result["summary"]
                article.tags     = result["tags"]
                session.commit()
                print(f"  ✅ Category: {result['category']}")
                print(f"  📝 Summary: {result['summary'][:80]}...")
            except Exception as e:
                print(f"  ❌ Failed: {e}")
                continue

        print(f"\n✨ Reprocessing complete!")


if __name__ == "__main__":
    run_pipeline(limit=500)

# if __name__ == "__main__":
#     reprocess_enriched(limit=20)