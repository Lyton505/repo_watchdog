import requests
import os
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path('./.env')
load_dotenv(dotenv_path=dotenv_path)

ACCESS_TOKEN = os.getenv('Z_EMAIL_ACCESS_TOKEN')
REFRESH_TOKEN = os.getenv('Z_REFRESH_TOKEN')
CLIENT_ID = os.getenv('Z_CLIENT_ID')
CLIENT_SECRET = os.getenv('Z_CLIENT_SECRET')
TOKEN_URL = "https://accounts.zoho.com/oauth/v2/token"
ACCOUNT_ID = os.getenv('Z_ACCOUNT_ID')
API_BASE_URL = f"https://mail.zoho.com/api/accounts/{ACCOUNT_ID}/messages"

print(ACCESS_TOKEN)

def send_email(to_email, subject, content):
    headers = {
        "Authorization": f"Zoho-oauthtoken {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "fromAddress": os.getenv('Z_EMAIL_FROM_ADDRESS'),
        "toAddress": to_email,
        "subject": subject,
        "content": content
    }
    response = requests.post(API_BASE_URL, json=data, headers=headers)

    if response.status_code == 401 or response.status_code == 404:  # Access token expired
        print("Access token expired. Refreshing...")
        refresh_access_token()  # Refresh token
        headers["Authorization"] = f"Zoho-oauthtoken {ACCESS_TOKEN}"
        response = requests.post(API_BASE_URL, json=data, headers=headers)

    if response.status_code == 200:
        print("Email sent successfully!")
    else:
        print("Failed to send email:", response.json())


def refresh_access_token():
    global ACCESS_TOKEN
    payload = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
    }

    response = requests.post(TOKEN_URL, data=payload)
    if response.status_code == 200:
        token_data = response.json()
        ACCESS_TOKEN = token_data["access_token"]
        # Update the .env file with the new access token
        with open(dotenv_path, "r") as file:
            lines = file.readlines()
        with open(dotenv_path, "w") as file:
            for line in lines:
                if line.startswith("Z_EMAIL_ACCESS_TOKEN"):
                    file.write(f"Z_EMAIL_ACCESS_TOKEN={ACCESS_TOKEN}\n")
                else:
                    file.write(line)
        print("Access token refreshed successfully!")
    else:
        print("Failed to refresh token:", response.json())
        raise Exception("Unable to refresh token")