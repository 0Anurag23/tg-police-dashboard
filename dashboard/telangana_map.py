import folium
import json
import os
 
# District name in this dict must match EXACTLY what's in the GeoJSON 'district' field
# so the choropleth tooltip works correctly.
# Names here also used for tag/title matching in articles.
 
TELANGANA_DISTRICTS = {
    "Adilabad":                  (19.5032, 78.5500),
    "Hyderabad":                 (17.4001, 78.4713),
    "Jagitial":                  (18.7896, 78.8983),
    "Jangoan":                   (17.7273, 79.2819),
    "Jayashankar":               (18.4836, 79.8368),
    "Jogulamba Gadwal":          (16.0661, 77.8152),
    "Kamareddy":                 (18.2940, 78.0554),
    "Karimnagar":                (18.3946, 79.2021),
    "Khammam":                   (17.1964, 80.3660),
    "Kumuram Bheem Asifabad":    (19.3493, 79.3741),
    "Mahabubabad":               (17.6398, 79.9104),
    "Mahabubnagar":              (16.7713, 77.9852),
    "Mancherial":                (19.0366, 79.4576),
    "Medak":                     (17.9603, 78.2382),
    "Medchal Malkajgiri":        (17.5176, 78.5471),
    "Mulugu":                    (18.2157, 80.3076),
    "Nagarkurnool":              (16.4390, 78.5592),
    "Nalgonda":                  (16.8881, 79.0507),
    "Narayanpet":                (16.6979, 77.5813),
    "Nirmal":                    (19.1149, 78.3294),
    "Nizamabad":                 (18.6896, 78.2678),
    "Peddapalli":                (18.6251, 79.4220),
    "Rajanna Sircilla":          (18.4118, 78.7548),
    "Ranga Reddy":               (17.1525, 78.4194),
    "Sangareddy":                (17.8013, 77.9395),
    "Siddipet":                  (18.0356, 78.8662),
    "Suryapet":                  (17.1960, 79.7103),
    "Vikarabad":                 (17.2269, 77.7705),
    "Wanaparthy":                (16.3011, 78.0480),
    "Warangal Rural":            (17.9218, 79.7022),
    "Warangal Urban":            (18.0207, 79.5036),
    "Yadadri Bhuvanagiri":       (17.4256, 78.9897),
    "Bhadradri Kothagudem":      (17.6864, 80.7178),
}
 
# Aliases: maps old/alternate names from article tags → canonical GeoJSON names
# This lets articles tagged "Rangareddy" or "Hanamkonda" still match correctly
DISTRICT_ALIASES = {
    "rangareddy":        "Ranga Reddy",
    "ranga reddy":       "Ranga Reddy",
    "medchal":           "Medchal Malkajgiri",
    "malkajgiri":        "Medchal Malkajgiri",
    "kumuram bheem":     "Kumuram Bheem Asifabad",
    "asifabad":          "Kumuram Bheem Asifabad",
    "jogulamba":         "Jogulamba Gadwal",
    "gadwal":            "Jogulamba Gadwal",
    "hanamkonda":        "Warangal Urban",
    "warangal":          "Warangal Urban",
    "jagtial":           "Jagitial",
    "jangaon":           "Jangoan",
    "mahbubnagar":       "Mahabubnagar",
    "yadadri":           "Yadadri Bhuvanagiri",
    "bhadradri":         "Bhadradri Kothagudem",
    "kothagudem":        "Bhadradri Kothagudem",
    "jayashankar bhupalpally": "Jayashankar",
    "narayanpet":        "Narayanpet",
}
 
 
def resolve_district(name: str) -> str | None:
    """Return canonical district name, checking aliases too."""
    lower = name.lower().strip()
    # Direct match
    for d in TELANGANA_DISTRICTS:
        if d.lower() == lower:
            return d
    # Alias match
    return DISTRICT_ALIASES.get(lower)
 
 
def extract_districts_from_text(text: str) -> list:
    """Find all district mentions in a string (tags, title, summary)."""
    if not text:
        return []
    found = []
    text_lower = text.lower()
 
    # Check aliases first (longer names first to avoid partial matches)
    for alias in sorted(DISTRICT_ALIASES, key=len, reverse=True):
        if alias in text_lower:
            canonical = DISTRICT_ALIASES[alias]
            if canonical not in found:
                found.append(canonical)
 
    # Then check canonical names
    for district in TELANGANA_DISTRICTS:
        if district.lower() in text_lower and district not in found:
            found.append(district)
 
    return found
 
 
def build_district_counts(df) -> dict:
    counts = {d: 0 for d in TELANGANA_DISTRICTS}
    for _, row in df.iterrows():
        combined = " ".join([
            str(row.get("tags", "") or ""),
            str(row.get("title", "") or ""),
        ])
        districts = extract_districts_from_text(combined)
        for d in districts:
            if d in counts:
                counts[d] += 1
    return counts
 
 
def get_color(count, max_count):
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
    counts = build_district_counts(df)
    max_count = max(counts.values()) if counts else 1

    m = folium.Map(
        location=[17.5, 79.0],
        zoom_start=7,
        tiles="CartoDB positron",
        width="100%",
        height=500,
    )

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    geojson_path = os.path.join(BASE_DIR, "data", "telangana_districts.geojson")

    with open(geojson_path, "r") as f:
        geojson_data = json.load(f)

    # Add article counts to GeoJSON properties
    for feature in geojson_data["features"]:
        district_name = feature["properties"].get("district", "")
        # Try to match district name
        count = 0
        for our_district, our_count in counts.items():
            if our_district.lower() in district_name.lower() or district_name.lower() in our_district.lower():
                count = our_count
                break
        feature["properties"]["article_count"] = count

    def style_function(feature):
        count = feature["properties"].get("article_count", 0)
        color = get_color(count, max_count)
        return {
            "fillColor": color,
            "color": "#1e3a8a",
            "weight": 1.8,
            "fillOpacity": 0.7,
        }

    def highlight_function(feature):
        return {
            "fillColor": "#fbbf24",
            "color": "#1d4ed8",
            "weight": 3,
            "fillOpacity": 0.9,
        }

    folium.GeoJson(
        geojson_data,
        name="Telangana Districts",
        style_function=style_function,
        highlight_function=highlight_function,
        tooltip=folium.GeoJsonTooltip(
            fields=["district", "article_count"],
            aliases=["District:", "Articles:"],
            sticky=True,
            labels=True,
            style="""
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 6px 10px;
                font-size: 13px;
                font-weight: 500;
            """,
        ),
    ).add_to(m)

    m.fit_bounds([[15.8, 77.0], [19.9, 81.2]])

    legend_html = """
    <div style="position:fixed;bottom:30px;left:30px;z-index:1000;
                background:white;padding:10px 15px;border-radius:8px;
                border:1px solid #ccc;font-size:12px;box-shadow:2px 2px 6px rgba(0,0,0,0.2)">
        <b>📰 Articles per District</b><br><br>
        <span style="background:#08306b;padding:2px 14px;color:white;border-radius:3px">██</span> High<br>
        <span style="background:#2171b5;padding:2px 14px;color:white;border-radius:3px">██</span> Medium<br>
        <span style="background:#6baed6;padding:2px 14px;color:white;border-radius:3px">██</span> Low<br>
        <span style="background:#f7fbff;padding:2px 14px;color:#333;border-radius:3px;border:1px solid #ccc">██</span> None
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    return m