import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from db.database import Article, Base
from urllib.parse import quote_plus

# ── Page config ──────────────────────────────────────────────────
st.set_page_config(
    page_title="TG Police News Dashboard",
    page_icon="🚔",
    layout="wide"
)

# ── Database connection ───────────────────────────────────────────
import os
from dotenv import load_dotenv
load_dotenv()

try:
    # Production — Streamlit Cloud secrets
    password = quote_plus(st.secrets["SUPABASE_PASSWORD"])
except:
    # Local — .env file
    password = quote_plus(os.getenv("SUPABASE_PASSWORD", ""))

SUPABASE_URL = f"postgresql://postgres.enhuqacwlmsudqlalxle:{password}@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
engine = create_engine(SUPABASE_URL)

# ── Category colors and icons ─────────────────────────────────────
CAT_ICONS = {
    "Crime": "🔴",
    "Drugs": "🟠",
    "Recruitment": "🟢",
    "Awards": "🏆",
    "Infrastructure": "🔵",
    "Awareness": "🟡",
    "Other": "⚪",
    "Uncategorized": "⚫"
}

CAT_COLORS = {
    "Crime": "#ef4444",
    "Drugs": "#f97316",
    "Recruitment": "#22c55e",
    "Awards": "#eab308",
    "Infrastructure": "#3b82f6",
    "Awareness": "#a855f7",
    "Other": "#6b7280",
    "Uncategorized": "#9ca3af"
}

# ── Load data ─────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_articles():
    with Session(engine) as session:
        articles = session.query(Article).filter(
            Article.summary != "",
            Article.category != "Uncategorized"
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

# Fix category names
df["category"] = df["category"].replace({
    "Crimes Drugs": "Drugs",
    "crimes drugs": "Drugs",
})

# ── Header ────────────────────────────────────────────────────────
st.title("🚔 Telangana Police News Dashboard")
st.caption("Live news aggregator — powered by crewAI + Qwen2.5 | Auto-refreshes every 6 hours")

# ── Top metrics ───────────────────────────────────────────────────
st.markdown("---")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("📰 Total Articles", len(df))
col2.metric("🗂️ Categories", df["category"].nunique())
col3.metric("📡 Sources", df["source"].nunique())
col4.metric("📅 Latest", pd.to_datetime(df["date"]).max().strftime("%d %b %Y") if len(df) > 0 else "N/A")
col5.metric("🆕 Today", len(df[pd.to_datetime(df["date"]).dt.date == pd.Timestamp.now().date()]))
st.markdown("---")

# ── Charts ────────────────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📊 Articles by Category")
    cat_counts = df["category"].value_counts().reset_index()
    cat_counts.columns = ["Category", "Count"]
    colors = [CAT_COLORS.get(c, "#6b7280") for c in cat_counts["Category"]]
    fig = px.bar(
        cat_counts, x="Category", y="Count",
        color="Category",
        color_discrete_map=CAT_COLORS,
        text="Count"
    )
    fig.update_layout(showlegend=False, height=300, margin=dict(t=10))
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, width="stretch")

with col_right:
    st.subheader("📈 Articles Over Time (Last 30 Days)")
    df["day"] = pd.to_datetime(df["date"]).dt.date
    last_30 = pd.Timestamp.now() - pd.Timedelta(days=30)
    time_counts = df[pd.to_datetime(df["date"]) >= last_30].groupby("day").size().reset_index(name="Count")
    fig2 = px.line(
        time_counts, x="day", y="Count",
        markers=True,
        color_discrete_sequence=["#3b82f6"]
    )
    fig2.update_layout(height=300, margin=dict(t=10))
    st.plotly_chart(fig2, width="stretch")

st.markdown("---")

# ── Top Sources ───────────────────────────────────────────────────
st.subheader("📡 Top News Sources")
source_counts = df["source"].value_counts().head(8).reset_index()
source_counts.columns = ["Source", "Count"]
fig3 = px.bar(
    source_counts, x="Count", y="Source",
    orientation="h",
    color_discrete_sequence=["#3b82f6"],
    text="Count"
)
fig3.update_layout(height=250, margin=dict(t=10))
fig3.update_traces(textposition="outside")
st.plotly_chart(fig3, width="stretch")

st.markdown("---")

# ── District Map ─────────────────────────────────────────────────
st.subheader("🗺️ Telangana District News Map")
st.caption("Bubble size = number of articles mentioning that district. Click a district to filter news.")

from streamlit_folium import st_folium
from dashboard.telangana_map import create_district_map

map_fig = create_district_map(df)
map_data = st_folium(map_fig, width="100%", height=500, key="district_map")

# Persist selected district across reruns
if "selected_district" not in st.session_state:
    st.session_state.selected_district = None

# Detect clicked district
if map_data and map_data.get("last_object_clicked_tooltip"):
    tooltip = str(map_data["last_object_clicked_tooltip"]).upper()

    for district in create_district_map.__globals__["TELANGANA_DISTRICTS"].keys():
        if district.upper() in tooltip:
            # Toggle selection
            if st.session_state.selected_district == district:
                st.session_state.selected_district = None
            else:
                st.session_state.selected_district = district
            break

selected_district = st.session_state.selected_district

# Show selected district + clear button
col_map1, col_map2 = st.columns([3, 1])

with col_map1:
    if selected_district:
        st.info(f"📍 Filtered to: **{selected_district}**")

with col_map2:
    if st.button("❌ Clear Filter"):
        st.session_state.selected_district = None
        st.rerun()

st.markdown("---")

# ── Filters ───────────────────────────────────────────────────────
st.subheader("🔍 Filter & Search")
col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    all_cats = ["All"] + sorted(df["category"].dropna().unique().tolist())
    cat_counts_dict = df["category"].value_counts().to_dict()
    cat_options = ["All"] + [f"{c} ({cat_counts_dict.get(c, 0)})" for c in sorted(df["category"].dropna().unique().tolist())]
    selected_cat_display = st.selectbox("Category", cat_options)
    selected_cat = "All" if selected_cat_display == "All" else selected_cat_display.split(" (")[0]

with col_f2:
    search = st.text_input("Search headlines", placeholder="e.g. Hyderabad, drugs, arrest...")

with col_f3:
    sort_by = st.selectbox("Sort by", ["Newest first", "Oldest first"])

# Apply filters
filtered = df.copy()
if selected_cat != "All":
    filtered = filtered[filtered["category"] == selected_cat]

# Filter by district if map was clicked
if selected_district:
    filtered = filtered[
        filtered["tags"].str.contains(selected_district, case=False, na=False) |
        filtered["title"].str.contains(selected_district, case=False, na=False)
    ]
if search:
    filtered = filtered[
        filtered["title"].str.contains(search, case=False, na=False) |
        filtered["tags"].str.contains(search, case=False, na=False) |
        filtered["summary"].str.contains(search, case=False, na=False)
    ]
if sort_by == "Oldest first":
    filtered = filtered.sort_values("date", ascending=True)

# ── Pagination ────────────────────────────────────────────────────
ARTICLES_PER_PAGE = 20
total = len(filtered)
total_pages = max(1, (total + ARTICLES_PER_PAGE - 1) // ARTICLES_PER_PAGE)

# Initialize page in session state
if "current_page" not in st.session_state:
    st.session_state.current_page = 1

# Reset to page 1 when filters change
filter_key = f"{selected_cat}_{search}_{sort_by}_{selected_district}"
if "last_filter_key" not in st.session_state:
    st.session_state.last_filter_key = filter_key
if st.session_state.last_filter_key != filter_key:
    st.session_state.current_page = 1
    st.session_state.last_filter_key = filter_key

# ── Top pagination controls ───────────────────────────────────────
st.markdown(f"Showing **{total}** articles | Page **{st.session_state.current_page}** of **{total_pages}**")

col_p1, col_p2, col_p3, col_p4, col_p5 = st.columns([1, 1, 2, 1, 1])

with col_p1:
    if st.button("⏮️ First", use_container_width=True):
        st.session_state.current_page = 1
        st.rerun()

with col_p2:
    if st.button("◀️ Prev", use_container_width=True):
        if st.session_state.current_page > 1:
            st.session_state.current_page -= 1
            st.rerun()

with col_p3:
    jump_page = st.number_input(
        "Go to page",
        min_value=1,
        max_value=total_pages,
        value=st.session_state.current_page,
        step=1,
        label_visibility="collapsed"
    )
    if jump_page != st.session_state.current_page:
        st.session_state.current_page = jump_page
        st.rerun()

with col_p4:
    if st.button("Next ▶️", use_container_width=True):
        if st.session_state.current_page < total_pages:
            st.session_state.current_page += 1
            st.rerun()

with col_p5:
    if st.button("Last ⏭️", use_container_width=True):
        st.session_state.current_page = total_pages
        st.rerun()

page = st.session_state.current_page
start = (page - 1) * ARTICLES_PER_PAGE
end = start + ARTICLES_PER_PAGE
page_df = filtered.iloc[start:end]

st.caption(f"Showing articles **{start+1}–{min(end, total)}** of **{total}**")
st.markdown("---")

# ── News cards ────────────────────────────────────────────────────
for _, row in page_df.iterrows():
    cat = row["category"]
    icon = CAT_ICONS.get(cat, "⚪")
    color = CAT_COLORS.get(cat, "#6b7280")

    with st.container():
        col_main, col_meta = st.columns([4, 1])

        with col_main:
            st.markdown(f"### [{row['title']}]({row['url']})")
            st.markdown(f"{row['summary']}")
            if row["tags"]:
                tags = row["tags"].split(",")
                tag_html = " ".join([
                    f'<span style="background:#e0f2fe;color:#0369a1;padding:2px 10px;border-radius:20px;font-size:12px;margin:2px;display:inline-block">{t.strip()}</span>'
                    for t in tags if t.strip()
                ])
                st.markdown(tag_html, unsafe_allow_html=True)

        with col_meta:
            st.markdown(
                f'<div style="background:{color}20;border-left:4px solid {color};padding:8px 12px;border-radius:4px">'
                f'<strong>{icon} {cat}</strong></div>',
                unsafe_allow_html=True
            )
            st.caption(f"📅 {pd.to_datetime(row['date']).strftime('%d %b %Y')}")
            st.caption(f"📡 {row['source']}")

        st.markdown("---")

# ── Bottom pagination controls ────────────────────────────────────
st.markdown(f"Page **{page}** of **{total_pages}**")
col_b1, col_b2, col_b3, col_b4, col_b5 = st.columns([1, 1, 2, 1, 1])

with col_b1:
    if st.button("⏮️ First ", use_container_width=True):
        st.session_state.current_page = 1
        st.rerun()

with col_b2:
    if st.button("◀️ Prev ", use_container_width=True):
        if st.session_state.current_page > 1:
            st.session_state.current_page -= 1
            st.rerun()

with col_b4:
    if st.button("Next ▶️ ", use_container_width=True):
        if st.session_state.current_page < total_pages:
            st.session_state.current_page += 1
            st.rerun()

with col_b5:
    if st.button("Last ⏭️ ", use_container_width=True):
        st.session_state.current_page = total_pages
        st.rerun()