import requests

client_id = "195827"
client_secret = "131350dba2490dca752c837f92cd6f01a33cb6b8"
code = "60057a02df3f15cfc792f0004d2d98424c06b1f4"

response = requests.post(
    "https://www.strava.com/oauth/token",
    data={
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code"
    }
)

print("Status code:", response.status_code)
print("Raw response:")
print(response.text)