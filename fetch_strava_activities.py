import requests
import pandas as pd

# --- YOUR PERMANENT KEYS ---
CLIENT_ID = "195827"
CLIENT_SECRET = "131350dba2490dca752c837f92cd6f01a33cb6b8"
REFRESH_TOKEN = "d4a5db656c08d4b33e6d227aa7592f08f1d0dea7"

# --- STEP 1: GET A FRESH ACCESS TOKEN AUTOMATICALLY ---
auth_url = "https://www.strava.com/oauth/token"
auth_payload = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'refresh_token': REFRESH_TOKEN,
    'grant_type': 'refresh_token'
}

print("Refreshing token...")
auth_res = requests.post(auth_url, data=auth_payload)
new_access_token = auth_res.json()['access_token']

# --- STEP 2: FETCH THE ACTIVITIES ---
url = "https://www.strava.com/api/v3/athlete/activities"
headers = {'Authorization': f"Bearer {new_access_token}"}
params = {'per_page': 200, 'page': 1} # Increased to 200 to get more history

print("Fetching activities...")
response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)

    # Convert distance to KM
    df['distance'] = df['distance'] / 1000

    # Filter for Runs only
    df = df[df['type'] == 'Run']

    # Save to CSV
    df.to_csv("strava_activities.csv", index=False)
    print(f"Success! Saved {len(df)} runs to strava_activities.csv")
else:
    print(f"Failed! Status: {response.status_code}")