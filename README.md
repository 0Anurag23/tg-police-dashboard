# 🚔 Telangana Police News Dashboard

> An AI-powered live news aggregator and analytics dashboard for Telangana Police news — built with crewAI, Qwen2.5, and Streamlit.

## 🌐 Live Demo
**[→ View Live Dashboard](https://tg-police-news.streamlit.app/)**

---

## 📌 Problem Statement
Tracking Telangana Police news across multiple sources (The Hindu, Deccan Chronicle, Siasat Daily, etc.) is time-consuming and scattered. This project automates collection, categorization, and summarization of all TG Police news into a single searchable dashboard — updated every 6 hours automatically.

---

## ✨ Features
- **Multi-source scraping** — aggregates from 37 Google News RSS feeds (6 general + 31 district-specific)
- **AI categorization** — automatically labels each article as Crime, Drugs, Recruitment, Awards, Infrastructure, or Awareness
- **AI summarization** — generates a 3-line factual summary per article using Qwen2.5:7b
- **Tag extraction** — pulls district names, crime types, and key topics
- **Interactive district map** — all 33 Telangana districts with color-coded article intensity
- **Live dashboard** — searchable, filterable news feed with charts and pagination
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
| Web scraping | Google News RSS + newspaper3k | Collect articles from 37 feeds |
| AI pipeline | crewAI + Qwen2.5:7b (Ollama) | Categorize, summarize, tag |
| Database (local) | SQLite | Development storage |
| Database (cloud) | Supabase PostgreSQL | Production storage |
| Dashboard | Streamlit + Plotly | Visualization and analytics |
| District map | Folium + GeoJSON | Interactive Telangana district heatmap |
| Scheduler | schedule (Python) | Auto-refresh every 6hrs |
| Deployment | Streamlit Cloud | Free public hosting |

---

## 📁 Project Structure

```
tg-police-dashboard/
├── agents/
│   ├── scraper_agent.py          # RSS scraper — 37 feeds, source extraction
│   └── article_fetcher.py        # Full article text fetcher (newspaper3k)
├── db/
│   └── database.py               # SQLAlchemy models + save/dedup functions
├── pipeline/
│   └── crew_pipeline.py          # crewAI agents (categorizer, summarizer, tagger)
├── dashboard/
│   ├── app.py                    # Streamlit dashboard with pagination + filters
│   ├── telangana_map.py          # Folium district map with GeoJSON boundaries
│   ├── requirements.txt          # Cloud deployment dependencies
│   └── data/
│       └── telangana_districts.geojson  # All 33 district boundaries
├── data/
│   └── news.db                   # Local SQLite database (gitignored)
├── main.py                       # Manual scrape trigger
├── scheduler.py                  # Auto scheduler (runs every 6 hours)
├── migrate_to_supabase.py        # One-time migration: SQLite → Supabase
├── requirements.txt              # Full local dependencies
├── SETUP.md                      # Local setup guide
└── .gitignore
```

---

## 🔄 How It Works

```
Google News RSS (37 feeds — general + all 33 districts)
        ↓
scraper_agent.py → extracts title, URL, date, source, body
        ↓
article_fetcher.py → fetches full article text (newspaper3k)
        ↓
crew_pipeline.py → 3 crewAI agents run on each article:
        • Categorizer agent   → labels category
        • Summarizer agent    → writes 3-line summary
        • Tag Extractor agent → pulls district + keywords
        ↓
SQLite (local) → migrate_to_supabase.py → Supabase PostgreSQL
        ↓
Streamlit Dashboard → displays with map, filters, search, pagination
```

---

## 🗺️ District Map
The dashboard includes an interactive Telangana district map:
- All **33 districts** with accurate GeoJSON boundaries
- Color intensity based on article count (darker = more articles)
- Hover to see district name and article count
- Click a district to filter the news feed to that district
- Yellow highlight on hover

---

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
- [x] Google News RSS scraping (37 feeds — 6 general + 31 district-specific)
- [x] crewAI pipeline (categorize, summarize, tag)
- [x] Streamlit dashboard with charts, filters, search
- [x] Pagination (20 articles per page with prev/next navigation)
- [x] Auto-scheduler (every 6 hours)
- [x] Supabase cloud database
- [x] Streamlit Cloud deployment
- [x] Telangana 33-district interactive map with GeoJSON boundaries
- [x] Real newspaper source names (150+ sources tracked)
- [ ] Telegram daily digest alerts

---

## 📝 License
MIT License — free to use and modify.