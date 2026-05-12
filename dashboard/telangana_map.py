import folium
import json


TELANGANA_DISTRICTS = {
    "Hyderabad": (17.3850, 78.4867),
    "Rangareddy": (17.3753, 78.1734),
    "Medchal": (17.6300, 78.4800),
    "Sangareddy": (17.6257, 78.0865),
    "Vikarabad": (17.3336, 77.9035),
    "Medak": (18.0490, 78.2637),
    "Siddipet": (18.1018, 78.8521),
    "Kamareddy": (18.3200, 78.3400),
    "Nizamabad": (18.6725, 78.0941),
    "Nirmal": (19.0943, 78.3439),
    "Adilabad": (19.6641, 78.5320),
    "Kumuram Bheem": (19.2833, 79.5167),
    "Mancherial": (18.8714, 79.4596),
    "Peddapalli": (18.6152, 79.3772),
    "Jagtial": (18.7947, 78.9148),
    "Karimnagar": (18.4386, 79.1288),
    "Rajanna Sircilla": (18.3867, 78.8329),
    "Warangal": (17.9784, 79.5941),
    "Hanamkonda": (18.0165, 79.5288),
    "Jangaon": (17.7250, 79.1520),
    "Jayashankar": (18.1618, 80.0141),
    "Mulugu": (18.1950, 80.5500),
    "Bhadradri": (17.5965, 80.8914),
    "Khammam": (17.2473, 80.1514),
    "Mahabubabad": (17.5985, 80.0024),
    "Suryapet": (17.1400, 79.6200),
    "Nalgonda": (17.0575, 79.2671),
    "Yadadri": (17.0800, 78.9200),
    "Mahbubnagar": (16.7375, 77.9866),
    "Narayanpet": (16.7450, 77.4950),
    "Wanaparthy": (16.3650, 78.0600),
    "Nagarkurnool": (16.4800, 78.3200),
    "Jogulamba": (16.4100, 77.8200),
}

def extract_district_from_tags(tags: str) -> list:
    if not tags:
        return []
    found = []
    tags_lower = tags.lower()
    for district in TELANGANA_DISTRICTS.keys():
        if district.lower() in tags_lower:
            found.append(district)
    return found

def build_district_counts(df) -> dict:
    counts = {d: 0 for d in TELANGANA_DISTRICTS}
    for _, row in df.iterrows():
        districts = extract_district_from_tags(str(row.get("tags", "")))
        title = str(row.get("title", "")).lower()
        for district in TELANGANA_DISTRICTS.keys():
            if district.lower() in title and district not in districts:
                districts.append(district)
        for d in districts:
            if d in counts:
                counts[d] += 1
    return counts

def get_color(count, max_count):
    """Return color based on article count."""
    if max_count == 0:
        return "#f0f0f0"
    ratio = count / max_count
    if ratio == 0:
        return "#f7fbff"
    elif ratio < 0.1:
        return "#c6dbef"
    elif ratio < 0.3:
        return "#6baed6"
    elif ratio < 0.6:
        return "#2171b5"
    else:
        return "#08306b"

def create_district_map(df):
    """Create a folium map with district bubbles."""
    counts = build_district_counts(df)
    max_count = max(counts.values()) if counts else 1

    # Create folium map centered on Telangana
    m = folium.Map(
        location=[17.5, 79.0],
        zoom_start=7,
        tiles="CartoDB positron",
        width="100%",
        height=500,
    )


    import os

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    geojson_path = os.path.join(BASE_DIR, "data", "telangana_districts.geojson")

    with open(geojson_path, "r") as f:
        geojson_data = json.load(f)

    folium.GeoJson(
        geojson_data,
        name="Telangana Districts",
        style_function=lambda feature: {
            "fillColor": "#bfdbfe",
            "color": "#1e3a8a",
            "weight": 1.8,
            "fillOpacity": 0.12,
        },
        highlight_function=lambda feature: {
            "fillColor": "#60a5fa",
            "color": "#1d4ed8",
            "weight": 3,
            "fillOpacity": 0.30,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["D_N"],
            aliases=["District:"],
            sticky=False
        ),
    ).add_to(m)

    m.fit_bounds([
    [15.8, 77.0],   # southwest Telangana
    [19.9, 81.2],   # northeast Telangana
    ])

    # Add circle markers for each district
    for district, (lat, lon) in TELANGANA_DISTRICTS.items():
        count = counts.get(district, 0)
        color = get_color(count, max_count)
        radius = max(8, min(40, count * 0.5 + 8))

        folium.CircleMarker(
            location=[lat, lon],
            radius=radius,
            color="white",
            weight=1.5,
            fill=True,
            fill_color=color,
            fill_opacity=0.85,
            tooltip=folium.Tooltip(
                f"<b>{district}</b><br>📰 {count} articles",
                sticky=True
            ),
            popup=folium.Popup(
                f"<b>{district}</b><br>Articles: {count}",
                max_width=200
            ),
        ).add_to(m)

        # Add district name label
        folium.Marker(
            location=[lat, lon],
            icon=folium.DivIcon(
                html=f'''
                <div style="
                    font-size:9px;
                    font-weight:600;
                    color:#1f2937;
                    white-space:nowrap;
                    background:rgba(255,255,255,0.75);
                    padding:1px 4px;
                    border-radius:4px;
                ">
                    {district}
                </div>
                ''',
                icon_size=(100, 20),
                icon_anchor=(0, 0),
            )
        ).add_to(m)

    # Add legend
    legend_html = """
    <div style="position: fixed; bottom: 30px; left: 30px; z-index: 1000;
                background: white; padding: 10px 15px; border-radius: 8px;
                border: 1px solid #ccc; font-size: 12px; box-shadow: 2px 2px 6px rgba(0,0,0,0.2)">
        <b>📰 Articles</b><br>
        <span style="background:#08306b;padding:2px 10px;color:white;border-radius:3px">High</span><br>
        <span style="background:#2171b5;padding:2px 10px;color:white;border-radius:3px">Medium</span><br>
        <span style="background:#6baed6;padding:2px 10px;color:white;border-radius:3px">Low</span><br>
        <span style="background:#f7fbff;padding:2px 10px;color:#333;border-radius:3px;border:1px solid #ccc">None</span>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    return m