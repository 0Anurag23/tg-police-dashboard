# 🛠️ Setup Guide

## Prerequisites
- Python 3.11+
- Ollama installed (https://ollama.com)
- Git

## 1. Clone the repository
```bash
git clone https://github.com/0Anurag23/tg-police-dashboard.git
cd tg-police-dashboard
```

## 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

## 4. Pull the AI model
```bash
ollama pull qwen2.5:7b-instruct
```

## 5. Set up environment
Create a `.env` file in the project root:
```
# No API keys required - this project runs fully locally using Ollama
```

## 6. Initialize database
```bash
python db/database.py
```

## 7. Scrape articles
```bash
python main.py
```

## 8. Process with crewAI
```bash
python pipeline/crew_pipeline.py
```

## 9. Run dashboard locally
```bash
streamlit run dashboard/app.py
```

## 10. Auto scheduler
Runs scrape + process automatically every 6 hours:
```bash
python scheduler.py
```

## ☁️ Cloud Setup
- **Database:** Supabase PostgreSQL — run `migrate_to_supabase.py` to migrate local data
- **Hosting:** Streamlit Cloud — connect your GitHub repo at share.streamlit.io
- **Secrets:** Add `SUPABASE_PASSWORD` in Streamlit Cloud advanced settings

## 📝 Notes
- Ollama must be running (`ollama serve`) before running the pipeline
- All commands must be run from the project root directory
- The scheduler needs Ollama running to process new articles