# 🚔 Telangana Police News Dashboard

An AI-powered live news aggregation and analytics dashboard for Telangana Police-related news.

Built using **crewAI**, **Qwen2.5**, **Ollama**, **Supabase**, and **Streamlit**.

---

## 🌐 Live Demo

👉 **Dashboard:** [View Live Dashboard](https://tg-police-news.streamlit.app/)

---

## 📌 Problem Statement

Tracking Telangana Police news across multiple sources is fragmented and time-consuming.

This project automates:

- News collection from multiple trusted sources
- AI-based categorization and summarization
- District-wise tagging and analytics
- Visualization through an interactive dashboard

The system updates automatically every **6 hours**.

---

## ✨ Features

- 📰 **Multi-source scraping**
  - Aggregates from 6 Google News RSS feeds

- 🤖 **AI categorization**
  - Automatically classifies articles into:
    - Crime
    - Drugs
    - Recruitment
    - Awards
    - Infrastructure
    - Awareness

- 📝 **AI summarization**
  - Generates concise 3-line summaries using `Qwen2.5:7b`

- 🏷️ **Tag extraction**
  - Extracts:
    - District names
    - Crime types
    - Key topics

- 🗺️ **Interactive district map**
  - Visualizes all **33 Telangana districts**
  - Click any district to filter articles

- 📊 **Dashboard analytics**
  - Searchable news feed
  - Charts
  - Filters
  - Heatmaps

- ⏰ **Automated scheduler**
  - Runs every 6 hours

- ☁️ **Cloud database**
  - Supabase PostgreSQL integration

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
| Web Scraping | Google News RSS + newspaper3k | Collect articles |
| AI Pipeline | crewAI + Qwen2.5 (Ollama) | Categorization + summarization + tagging |
| Local Database | SQLite | Development storage |
| Cloud Database | Supabase PostgreSQL | Production storage |
| Dashboard | Streamlit + Plotly + Folium | Visualization |
| District Map | Folium + GeoJSON | Telangana district heatmap |
| Scheduler | schedule (Python) | Automated refresh |
| Deployment | Streamlit Cloud | Public hosting |

---

## 📁 Project Structure

```bash
tg-police-dashboard/
├── agents/
│   ├── scraper_agent.py
│   └── article_fetcher.py
├── db/
│   └── database.py
├── pipeline/
│   └── crew_pipeline.py
├── dashboard/
│   ├── app.py
│   ├── telangana_map.py
│   ├── data/
│   │   └── telangana_districts.geojson
│   └── requirements.txt
├── data/
│   └── news.db
├── main.py
├── scheduler.py
├── migrate_to_supabase.py
├── requirements.txt
├── SETUP.md
└── .gitignore
```

---

## 🔄 Workflow

```text
Google News RSS (6 feeds)
        ↓
scraper_agent.py
        ↓
article_fetcher.py
        ↓
crew_pipeline.py
   ├── Categorizer
   ├── Summarizer
   └── Tag Extractor
        ↓
Supabase PostgreSQL
        ↓
Streamlit Dashboard
```

---

## 🗺️ District Map Features

The dashboard includes an interactive Telangana district map with:

- Bubble size proportional to article count
- Color intensity based on article frequency
- Click-to-filter functionality
- Accurate district centroids from GeoJSON geometry

---

## 📊 Sample Output

### Input

```text
Hyderabad Police bust major drug racket in Secunderabad
```

### AI Output

```json
{
  "category": "Drugs",
  "summary": "Hyderabad Police conducted raids in Secunderabad and arrested 5 suspects in connection with a major drug trafficking operation. The accused were found with contraband worth ₹15 lakhs. Cases have been filed under NDPS Act.",
  "tags": "Hyderabad, Secunderabad, Drugs, NDPS Act, Arrest"
}
```

---

## 🚀 Quick Start

See [SETUP.md](SETUP.md) for full setup instructions.

```bash
git clone https://github.com/0Anurag23/tg-police-dashboard.git
cd tg-police-dashboard

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
ollama pull qwen2.5:7b-instruct

python main.py
streamlit run dashboard/app.py
```

---

## 🗺️ Roadmap

- [x] Google News RSS scraping
- [x] crewAI processing pipeline
- [x] Streamlit dashboard
- [x] Auto scheduler
- [x] Supabase cloud database
- [x] Streamlit Cloud deployment
- [x] Telangana 33-district map

---

## 📝 License

MIT License

Free to use and modify.