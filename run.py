import os
import json
import requests
import pandas as pd
from datetime import datetime
import smtplib
from email.message import EmailMessage

import pygsheets
from google.oauth2.service_account import Credentials

template_str = ""


# Load service account JSON from env var
service_account_info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
creds = Credentials.from_service_account_info(service_account_info, scopes=[
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
])

# Authorize pygsheets with explicit credentials
client = pygsheets.authorize(custom_credentials=creds)


def mod(row: int):
    sheet_id = "15ozBzfMIiUXrjuABo_pzlPQ-YaSYcTI_yZlJsDNoQM0"
    spreadsht = client.open_by_key(sheet_id)
    worksht = spreadsht.worksheet("title", "Sheet1")
    worksht.update_value(f'D{row}', '0')

def gsheet_to_df(sheet_url_or_id: str):
    import re
    import pandas as pd

    match = re.search(r"/d/([a-zA-Z0-9-_]+)", sheet_url_or_id)
    sheet_id = match.group(1) if match else sheet_url_or_id
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

    # 👇 one-liner that avoids saving to a file
    return pd.read_csv(csv_url)


def is_not_in_past(date_string: str) -> bool:
    try:
        input_date = datetime.strptime(date_string, "%Y%m%d")
        current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return input_date >= current_date
    except ValueError:
        return False

def send(sender_email, sender_password, recipient_email, subject, body):
    try:
        msg = EmailMessage()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.set_content(body)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def post(thedate: str, theid: int, theblock: str) -> bool:
    def get_urls_by_date(data: dict, date: str) -> list:
        for item in data.get("results", []):
            if item["date"] == date and item["block_letter"] == block:
                return item["url"]

    blocks_2025 = "https://ion.tjhsst.edu/api/blocks"
    cookies = {'sessionid': os.environ.get("ION_SESSIONID", "")}

    response = requests.get(blocks_2025, cookies=cookies)
    response.raise_for_status()
    data = response.json()

    urls = get_urls_by_date(data, thedate)
    day_block = f"{urls}?format=json"

    response_day_block = requests.get(day_block, cookies=cookies)
    response_day_block.raise_for_status()
    day_block_data = response_day_block.json()

    activity = day_block_data.get("activities", {}).get(theid) or day_block_data.get("activities", {}).get(int(theid))
    if activity:
        roster = activity.get("roster", {})
        count, capacity = roster.get("count", 0), roster.get("capacity", 0)
        spots_available = capacity - count
        global template_str
        template_str = f"Club '{activity.get('name')}' has {spots_available} spots (Filled: {count}, Capacity: {capacity})"
        print(template_str)
        return spots_available > 0
    return False

def run():
    
    # if "GOOGLE_SERVICE_ACCOUNT_JSON" not in os.environ:
    #     raise RuntimeError("Missing GOOGLE_SERVICE_ACCOUNT_JSON in environment!")
    
    # service_account_info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
    # client = pygsheets.authorize(service_account_info=service_account_info)

    # if your sheet URL is fixed, hardcode here
    df = gsheet_to_df("https://docs.google.com/spreadsheets/d/15ozBzfMIiUXrjuABo_pzlPQ-YaSYcTI_yZlJsDNoQM0/edit?usp=sharing")
    

    for index, row in df.iterrows():
        if row['D'] == 1:
            status = post(row['C'], str(row['A']), row['B'])
            if is_not_in_past(row['C']):
                mod(index+1)
            elif status:
                send(
                    sender_email=os.environ.get("SENDER_EMAIL"),
                    sender_password=os.environ.get("SENDER_PASSWORD"),
                    recipient_email=os.environ.get("RECIPIENT_EMAIL"),
                    subject="IONITE - Spot Available!",
                    body=f"{template_str}\n\nLog: {index+1}, ID: {row['A']}, Block: {row['B']}, Date: {row['C']}, Status: {status}"
                )
                mod(index+1)
    print("Operation Success")
    return {"success": True}
