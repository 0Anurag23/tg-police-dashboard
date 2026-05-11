import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy.orm import Session
from db.database import engine, Article

# ── Page config ──────────────────────────────────────────────────
st.set_page_config(
    page_title="TG Police News Dashboard",
    page_icon="🚔",
    layout="wide"
)

st.title(" Telangana Police News Dashboard")
st.caption("Live news aggregator — powered by crewAI + Qwen2.5")

# ── Load data ─────────────────────────────────────────────────────
@st.cache_data(ttl=300)  # refresh every 5 minutes
def load_articles():
    with Session(engine) as session:
        articles = session.query(Article).filter(
            Article.summary != ""
        ).order_by(Article.date.desc()).all()
        return pd.DataFrame([{
            "id":       a.id,
            "title":    a.title,
            "url":      a.url,
            "source":   a.source,
            "date":     a.date,
            "category": a.category,
            "summary":  a.summary,
            "tags":     a.tags,
        } for a in articles])

df = load_articles()

# ── Top metrics ───────────────────────────────────────────────────
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Articles", len(df))
col2.metric("Categories", df["category"].nunique())
col3.metric("Sources", df["source"].nunique())
col4.metric("Latest", df["date"].max().strftime("%d %b %Y") if len(df) > 0 else "N/A")

st.markdown("---")

# ── Charts row ────────────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Articles by Category")
    cat_counts = df["category"].value_counts().reset_index()
    cat_counts.columns = ["Category", "Count"]
    fig = px.bar(
        cat_counts, x="Category", y="Count",
        color="Category", text="Count",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(showlegend=False, height=300, margin=dict(t=10))
    st.plotly_chart(fig, width='stretch')

with col_right:
    st.subheader("Articles Over Time")
    df["day"] = pd.to_datetime(df["date"]).dt.date
    last_30 = pd.Timestamp.now() - pd.Timedelta(days=30)
    time_counts = df[pd.to_datetime(df["date"]) >= last_30].groupby("day").size().reset_index(name="Count")
    # df["day"] = pd.to_datetime(df["date"]).dt.date
    # time_counts = df.groupby("day").size().reset_index(name="Count")
    fig2 = px.line(
        time_counts, x="day", y="Count",
        markers=True, color_discrete_sequence=["#2563eb"]
    )
    fig2.update_layout(height=300, margin=dict(t=10))
    st.plotly_chart(fig2, width='stretch')

st.markdown("---")

# ── Filters ───────────────────────────────────────────────────────
st.subheader(" Filter & Search")
col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    all_cats = ["All"] + sorted(df["category"].dropna().unique().tolist())
    selected_cat = st.selectbox("Category", all_cats)

with col_f2:
    search = st.text_input("Search headlines", placeholder="e.g. Hyderabad, drugs, arrest...")

with col_f3:
    sort_by = st.selectbox("Sort by", ["Newest first", "Oldest first"])

# Apply filters
filtered = df.copy()
if selected_cat != "All":
    filtered = filtered[filtered["category"] == selected_cat]
if search:
    filtered = filtered[
        filtered["title"].str.contains(search, case=False, na=False) |
        filtered["tags"].str.contains(search, case=False, na=False) |
        filtered["summary"].str.contains(search, case=False, na=False)
    ]
if sort_by == "Oldest first":
    filtered = filtered.sort_values("date", ascending=True)

st.caption(f"Showing {len(filtered)} articles")
st.markdown("---")

# ── News cards ────────────────────────────────────────────────────
for _, row in filtered.iterrows():
    with st.container():
        col_main, col_meta = st.columns([4, 1])

        with col_main:
            st.markdown(f"### [{row['title']}]({row['url']})")
            st.markdown(f"{row['summary']}")
            if row["tags"]:
                tags = row["tags"].split(",")
                tag_html = " ".join([
                    f'<span style="background:#e0f2fe;color:#0369a1;padding:2px 8px;border-radius:12px;font-size:12px;margin:2px">{t.strip()}</span>'
                    for t in tags
                ])
                st.markdown(tag_html, unsafe_allow_html=True)

        with col_meta:
            cat_colors = {
                "Crime": "", "Drugs": "", "Recruitment": "",
                "Awards": "", "Infrastructure": "",
                "Awareness": "", "Other": ""
            }
            icon = cat_colors.get(row["category"], "")
            st.markdown(f"**{icon} {row['category']}**")
            st.caption(f" {row['date'].strftime('%d %b %Y')}")
            st.caption(f" {row['source']}")

        st.markdown("---")