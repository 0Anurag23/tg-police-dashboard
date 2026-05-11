# 🚔 Telangana Police News Dashboard

A live news aggregator and analytics dashboard for Telangana Police news, powered by AI.

## 🌐 Live Demo
[View Dashboard](https://tg-police-dashboard.streamlit.app)

## 📌 What it does
- Scrapes 600+ Telangana Police news articles from 6 Google News feeds
- Uses crewAI + Qwen2.5:7b (local LLM) to categorize, summarize and tag each article
- Displays everything in a live Streamlit dashboard with filters, search and charts
- Auto-refreshes every 6 hours via a scheduler

## 🗂️ Categories tracked
- Crime, Drugs, Recruitment, Awards, Infrastructure, Awareness, Other

## 🛠️ Tech Stack
| Component | Tool |
|---|---|
| Web scraping | Google News RSS + newspaper3k |
| AI pipeline | crewAI + Qwen2.5:7b via Ollama |
| Database (local) | SQLite |
| Database (cloud) | Supabase PostgreSQL |
| Dashboard | Streamlit + Plotly |
| Scheduler | APScheduler |
| Deployment | Streamlit Cloud |

## 📁 Project Structure
```
tg-police-dashboard/
├── agents/
│   ├── scrapper_agent.py      # RSS scraper
│   └── article_fetcher.py     # Full article text fetcher
├── db/
│   └── database.py            # Database models
├── pipeline/
│   └── crew_pipeline.py       # crewAI agents
├── dashboard/
│   ├── app.py                 # Streamlit dashboard
│   └── requirements.txt       # Cloud dependencies
├── data/
│   └── news.db                # Local SQLite database
├── main.py                    # Manual scrape trigger
├── scheduler.py               # Auto scheduler
└── requirements.txt           # Local dependencies
```

## 🚀 Quick Start
See [SETUP.md](SETUP.md) for full setup instructions.