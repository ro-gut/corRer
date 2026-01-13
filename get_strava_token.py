import requests

client_id = "195827"
client_secret = "131350dba2490dca752c837f92cd6f01a33cb6b8"
code = "66803cf92ddf88ecb5dbf26df5bb0afafeb6c3f6"

response = requests.post(
    "https://strava.com/oauth/token",
    data={
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code"
    }
)

data = response.json()
print(data)