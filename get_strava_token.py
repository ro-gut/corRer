import requests

client_id = "195827"
client_secret = "131350dba2490dca752c837f92cd6f01a33cb6b8"
code = "ecb6b9ccd9485447dccb8ff818f8b449f979306a"

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