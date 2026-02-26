import requests
import pandas as pd

# Your current access token from get_strava_token.py
ACCESS_TOKEN = "fc1b1aea4e603bf4af6e53a9674815bc4d80c084"

url = "https://www.strava.com/api/v3/athlete/activities"
params = {
    "per_page": 50,  # number of activities per request
    "page": 1
}
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

response = requests.get(url, headers=headers, params=params)

print("Status code:", response.status_code)
print("Raw response:", response.text[:500])  # print first 500 chars for sanity check

if response.status_code == 200:
    data = response.json()
    # Save as CSV
    df = pd.DataFrame(data)
    df.to_csv("strava_activities.csv", index=False)
    print("Saved activities to strava_activities.csv")