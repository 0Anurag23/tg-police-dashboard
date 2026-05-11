# 🚔 Telangana Police News Dashboard

> An AI-powered live news aggregator and analytics dashboard for Telangana Police news — built with crewAI, Qwen2.5, and Streamlit.

## 🌐 Live Demo
**[→ View Live Dashboard](https://tg-police-dashboard.streamlit.app)**

---

## 📌 Problem Statement
Tracking Telangana Police news across multiple sources (The Hindu, Deccan Chronicle, Siasat Daily, etc.) is time-consuming and scattered. This project automates collection, categorization, and summarization of all TG Police news into a single searchable dashboard — updated every 6 hours automatically.

---

## ✨ Features
- **Multi-source scraping** — aggregates from 6 Google News RSS feeds
- **AI categorization** — automatically labels each article as Crime, Drugs, Recruitment, Awards, Infrastructure, or Awareness
- **AI summarization** — generates a 3-line factual summary per article using Qwen2.5:7b
- **Tag extraction** — pulls district names, crime types, and key topics
- **Live dashboard** — searchable, filterable news feed with charts
- **Auto-refresh** — scheduler runs every 6 hours automatically
- **Cloud database** — articles stored in Supabase PostgreSQL

---

## 🗂️ Categories Tracked
| Category | Description |
|---|---|
| Crime | Arrests, FIRs, investigations |
| Drugs | NDPS Act cases, drug busts |
| Recruitment | Police job notifications |
| Awards | Officer recognitions |
| Infrastructure | Station construction, equipment |
| Awareness | Community programs, campaigns |

---

## 🛠️ Tech Stack
| Component | Tool | Purpose |
|---|---|---|
| Web scraping | Google News RSS + newspaper3k | Collect articles |
| Browser automation | browser-use + Playwright | Dynamic site scraping |
| AI pipeline | crewAI + Qwen2.5:7b (Ollama) | Categorize, summarize, tag |
| Database (local) | SQLite | Development storage |
| Database (cloud) | Supabase PostgreSQL | Production storage |
| Dashboard | Streamlit + Plotly | Visualization |
| Scheduler | schedule (Python) | Auto-refresh every 6hrs |
| Deployment | Streamlit Cloud | Free public hosting |

---

## 📁 Project Structure

```

tg-police-dashboard/
├── agents/
│   ├── scrapper_agent.py      # RSS scraper with source extraction
│   └── article_fetcher.py     # Full article text fetcher
├── db/
│   └── database.py            # SQLAlchemy models + save functions
├── pipeline/
│   └── crew_pipeline.py       # crewAI agents (categorizer, summarizer, tagger)
├── dashboard/
│   ├── app.py                 # Streamlit dashboard
│   └── requirements.txt       # Cloud deployment dependencies
├── data/
│   └── news.db                # Local SQLite database (gitignored)
├── main.py                    # Manual scrape trigger
├── scheduler.py               # Auto scheduler (runs every 6 hours)
├── migrate_to_supabase.py     # One-time migration: SQLite → Supabase
├── requirements.txt           # Full local dependencies
├── SETUP.md                   # Local setup guide
└── .gitignore

```

## 🔄 How It Works
```

Google News RSS (6 feeds)
↓
scrapper_agent.py → extracts title, URL, date, source, body
↓
article_fetcher.py → fetches full article text (newspaper3k)
↓
crew_pipeline.py → 3 crewAI agents run on each article:
• Categorizer agent  → labels category
• Summarizer agent   → writes 3-line summary
• Tag Extractor agent → pulls district + keywords
↓
Supabase PostgreSQL → stores all processed articles
↓
Streamlit Dashboard → displays with filters, search, charts

```

## 📊 Sample Output

**Input Article:**
> Hyderabad Police bust major drug racket in Secunderabad

**AI Output:**
```json
{
  "category": "Drugs",
  "summary": "Hyderabad Police conducted raids in Secunderabad and arrested 5 suspects in connection with a major drug trafficking operation. The accused were found with contraband worth ₹15 lakhs. Cases have been filed under NDPS Act.",
  "tags": "Hyderabad, Secunderabad, Drugs, NDPS Act, Arrest"
}
```

---

## 🚀 Quick Start
See **[SETUP.md](SETUP.md)** for full local setup instructions.

```bash
git clone https://github.com/0Anurag23/tg-police-dashboard.git
cd tg-police-dashboard
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
ollama pull qwen2.5:7b-instruct
python main.py
streamlit run dashboard/app.py
```

---

## 🗺️ Roadmap
- [x] Google News RSS scraping (6 feeds)
- [x] crewAI pipeline (categorize, summarize, tag)
- [x] Streamlit dashboard with charts and filters
- [x] Auto-scheduler (every 6 hours)
- [x] Supabase cloud database
- [x] Streamlit Cloud deployment
- [ ] Twitter/X scraping via browser-use
- [ ] Telangana district map visualization
- [ ] Telegram daily digest alerts
- [ ] Direct source scraping (Deccan Chronicle, Hans India)

---

## 📝 License
MIT License — free to use and modify.