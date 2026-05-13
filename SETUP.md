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

Keep this running in a separate terminal.

---

## 6. Configure Environment Variables

Create a `.env` file in project root:

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

---

## 9. Run AI Processing Pipeline

```bash
python pipeline/crew_pipeline.py
```

---

## 10. Launch Dashboard

```bash
streamlit run dashboard/app.py
```

---

## 11. Run Scheduler (Optional)

Runs scraping + processing every 6 hours.

```bash
python scheduler.py
```

---

# ☁️ Cloud Deployment

## Database Migration

Migrate local SQLite data to Supabase:

```bash
python migrate_to_supabase.py
```

---

## Streamlit Deployment

Deploy using Streamlit Cloud:

1. Push repo to GitHub
2. Open https://share.streamlit.io
3. Connect repository
4. Add secret:

```env
SUPABASE_PASSWORD=your_supabase_password
```

---

## Notes

- Run all commands from project root
- Ollama must be running before pipeline execution
- Scheduler also requires Ollama
- GeoJSON district file is included:

```bash
dashboard/data/telangana_districts.geojson
```