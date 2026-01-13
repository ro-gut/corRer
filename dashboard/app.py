# dashboard/app.py
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

# ------------------------
# Load CSV
# ------------------------
CSV_PATH = "data/training_plan.csv"
df = pd.read_csv(CSV_PATH)
df.columns = [c.strip() for c in df.columns]

# try weekend column variants
weekend_col_candidates = ["Weekend Long Run!", "Weekend Long Run", "Weekend Long Run !"]
weekend_col = next((c for c in weekend_col_candidates if c in df.columns), None)
if weekend_col is None:
    weekend_col = df.columns[3] if len(df.columns) > 3 else None

# ------------------------
# Parse date ranges
# ------------------------
def parse_range(date_range):
    if pd.isna(date_range):
        return None, None
    parts = date_range.strip().split("to")
    if len(parts) != 2:
        return None, None
    start_dt = datetime.strptime(parts[0].strip(), "%Y-%m-%d").date()
    end_dt   = datetime.strptime(parts[1].strip(), "%Y-%m-%d").date()
    return start_dt, end_dt

# Map weeks to their date ranges and workouts
weeks = []
for idx, row in df.iterrows():
    start_dt, end_dt = parse_range(row["Date Range"])
    if not start_dt or not end_dt:
        continue
    weeks.append({
        "week": row["Week"],
        "start": start_dt,
        "end": end_dt,
        "Tue Run": row.get("Tue Run", ""),
        "Thu Run": row.get("Thu Run", ""),
        weekend_col: row.get(weekend_col, ""),
        "Notes": row.get("Notes", "")
    })

# ------------------------
# Sidebar: Diagnostics + Week Selector
# ------------------------
st.sidebar.title("Diagnostics")
st.sidebar.write(f"CSV rows: {len(df)}")
st.sidebar.write(f"Weeks parsed: {len(weeks)}")

week_names = [w["week"] for w in weeks]
selected_week = st.sidebar.selectbox("Select Week", week_names)
week_data = next(w for w in weeks if w["week"] == selected_week)

# ------------------------
# Render Week Workouts
# ------------------------
st.title(f"🏃 Training — {week_data['week']}")
st.markdown(f"**Dates:** {week_data['start'].strftime('%d %b %Y')} → {week_data['end'].strftime('%d %b %Y')}")
st.markdown(f"**Notes:** {week_data['Notes']}")

st.markdown("---")
cols = st.columns(3)

# Display Tue, Thu, Weekend workouts
workouts = [("Tue Run", week_data["Tue Run"]), ("Thu Run", week_data["Thu Run"]), (weekend_col, week_data[weekend_col])]
for col, (label, workout) in zip(cols, workouts):
    with col:
        key = f"{week_data['week']}_{label}"
        st.checkbox(f"{label}\n{workout}", key=key)

# ------------------------
# Minimal styling helper (optional)
# ------------------------
def workout_color(text):
    t = str(text).lower()
    if "interval" in t: return "#e63946"
    if "tempo" in t: return "#ff8800"
    if "race" in t: return "#7028ff"
    if "easy" in t: return "#0077b6"
    if "long" in t: return "#2a9d8f"
    return "#6c757d"
