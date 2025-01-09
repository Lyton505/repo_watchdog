import requests
import os

ACCESS_TOKEN = os.environ['Z_EMAIL_ACCESS_TOKEN']
ACCOUNT_ID = os.environ['Z_ACCOUNT_ID']
API_BASE_URL = f"https://mail.zoho.com/api/accounts/{ACCOUNT_ID}/messages"


def send_email(to_email, subject, content):
    headers = {
        "Authorization": f"Zoho-oauthtoken {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "fromAddress": os.environ['Z_EMAIL_FROM_ADDRESS'],
        "toAddress": to_email,
        "subject": subject,
        "content": content
    }
    response = requests.post(API_BASE_URL, json=data, headers=headers)
    if response.status_code == 200:
        print("Email sent successfully!")
    else:
        print("Failed to send email:", response.json())