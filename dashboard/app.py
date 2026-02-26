# dashboard/app.py
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

# ------------------------
# Load CSVs
# ------------------------
CSV_PATH = "data/training_plan.csv"
df = pd.read_csv(CSV_PATH)
df.columns = [c.strip() for c in df.columns]

weekend_col = "Weekend Long Run!"


# -----------------------
# Load Strava Activities

STRAVA_CSV_PATH = "strava_activities.csv"
try:
    strava_df = pd.read_csv(STRAVA_CSV_PATH)
except FileNotFoundError:
    strava_df = pd.DataFrame()


# ------------------------
# Parse date ranges
# ------------------------
def parse_range(date_range):        # usually a string like "2025-12-02 to 2025-12-08"
    if pd.isna(date_range):
        return None, None  # if empty / NaN -> returns nothing
    parts = date_range.strip().split("to") # strip string
    if len(parts) != 2: # incase the format is wrong
        return None, None
    start_dt = datetime.strptime(parts[0].strip(), "%Y-%m-%d").date()
    end_dt   = datetime.strptime(parts[1].strip(), "%Y-%m-%d").date()
    return start_dt, end_dt

# Map weeks to their date ranges and workouts
weeks = [] # to store 1 dict per train. week
for idx, row in df.iterrows():
    start_dt, end_dt = parse_range(row["Date Range"]) #get start/end_dt
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

# ----------- Strava stats For now:

if not strava_df.empty:
    st.markdown("---")
    st.subheader("Strava Activities!")
    st.dataframe(strava_df)
else:
    st.info("No activities found.")