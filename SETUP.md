# 🛠️ Setup Guide

---

## Prerequisites
Install the following before starting:
- Python 3.11+
- Git
- Ollama → https://ollama.com

---

## 1. Clone Repository
```bash
git clone https://github.com/0Anurag23/tg-police-dashboard.git
cd tg-police-dashboard
```

---

## 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

---

## 4. Pull AI Model
```bash
ollama pull qwen2.5:7b-instruct
```

---

## 5. Start Ollama
```bash
ollama serve
```
Keep this running in a separate terminal whenever you run the pipeline.

---

## 6. Configure Environment Variables
Create a `.env` file in the project root:
```env
SUPABASE_PASSWORD=your_supabase_password
```

---

## 7. Initialize Database
```bash
python db/database.py
```

---

## 8. Scrape Articles
```bash
python main.py
```
This fetches articles from all 37 RSS feeds and saves them to `data/news.db`.

---

## 9. Enrich Articles (Optional but Recommended)
Fetches full article text for better AI summaries:
```bash
python agents/article_fetcher.py
```

---

## 10. Run AI Processing Pipeline
Categorizes, summarizes and tags all unprocessed articles:
```bash
python pipeline/crew_pipeline.py
```
This can take 30-60 minutes depending on number of articles.

---

## 11. Migrate to Supabase (Cloud)
Copy processed articles from local SQLite to Supabase PostgreSQL:
```bash
python migrate_to_supabase.py
```

---

## 12. Launch Dashboard
```bash
streamlit run dashboard/app.py
```
Opens at `http://localhost:8501`

---

## 13. Run Scheduler (Optional)
Runs the full pipeline automatically every 6 hours:
```bash
python scheduler.py
```
Requires Ollama to be running.

---

## 📋 Daily Workflow Summary
Every 6 hours (automatic via scheduler.py):

python main.py                      ← scrape new articles
python agents/article_fetcher.py    ← enrich with full text
python pipeline/crew_pipeline.py    ← AI categorize + summarize
python migrate_to_supabase.py       ← sync to cloud database

---

## ☁️ Cloud Deployment

### Supabase Setup
1. Create a free account at **supabase.com**
2. Create a new project
3. Get connection string from Settings → Database
4. Add `SUPABASE_PASSWORD` to your `.env` file
5. Run `python migrate_to_supabase.py` to populate the cloud database

### Streamlit Cloud Deployment
1. Push your repo to GitHub
2. Go to **share.streamlit.io**
3. Click **New app**
4. Select your repository
5. Set main file path: `dashboard/app.py`
6. Click **Advanced settings** → **Secrets** → add:
```toml
SUPABASE_PASSWORD = "your_supabase_password"
```
7. Click **Deploy**

---

## 📝 Notes
- Run all commands from the project root directory
- Ollama must be running before executing the pipeline
- The scheduler also requires Ollama to be running
- The GeoJSON district file is included in the repo at `dashboard/data/telangana_districts.geojson`
- The local `data/news.db` is gitignored — never committed to GitHub
- The `.env` file is gitignored — never committed to GitHub