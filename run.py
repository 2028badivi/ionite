import os, json
import requests
import pygsheets
import pandas as pd
from datetime import datetime
from email.message import EmailMessage
import smtplib

template_str = ""

def get_client():
    creds_dict = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
    return pygsheets.authorize(service_account_env_dict=creds_dict)

def mod(row: int):
    client = get_client()
    spreadsht = client.open("IONITE")
    worksht = spreadsht.worksheet("title", "Sheet1")
    worksht.update_value(f'D{row}', '0')

def gsheet_to_csv(sheet_url_or_id: str, output_filename: str = "output.csv"):
    import re
    match = re.search(r"/d/([a-zA-Z0-9-_]+)", sheet_url_or_id)
    if match:
        sheet_id = match.group(1)
    else:
        sheet_id = sheet_url_or_id
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    df = pd.read_csv(csv_url)
    df.to_csv(output_filename, index=False)
    return df

def is_not_in_past(date_string):
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
    except Exception as e:
        print(f"Failed to send email: {e}")

def post(thedate: str, theid: int, theblock: str) -> bool:
    blocks_2025 = f"https://ion.tjhsst.edu/api/blocks"
    cookies = {'sessionid': os.environ["ION_SESSIONID"]}

    response = requests.get(blocks_2025, cookies=cookies)
    response.raise_for_status()
    data = response.json()

    def get_urls_by_date(data: dict, date: str) -> str:
        for item in data.get("results", []):
            if item["date"] == date and item["block_letter"] == theblock:
                return item["url"]

    url = get_urls_by_date(data, thedate)
    if not url:
        return False

    response_day_block = requests.get(f"{url}?format=json", cookies=cookies)
    response_day_block.raise_for_status()
    day_block_data = response_day_block.json()

    activity = day_block_data.get("activities", {}).get(str(theid))
    if not activity:
        return False

    global template_str
    count = activity.get("roster", {}).get("count", 0)
    capacity = activity.get("roster", {}).get("capacity", 0)
    spots_available = capacity - count
    template_str = f"Club '{activity.get('name')}' has {spots_available} spots available"

    return spots_available > 0

def run():
    df = gsheet_to_csv(
        'https://docs.google.com/spreadsheets/d/15ozBzfMIiUXrjuABo_pzlPQ-YaSYcTI_yZlJsDNoQM0/edit?usp=sharing',
        "my_data.csv"
    )

    for index, row in df.iterrows():
        if row['D'] == 1:
            status = post(row['C'], str(row['A']), row['B'])
            if is_not_in_past(row['C']):
                mod(index+1)
            elif status:
                send(
                    sender_email=os.environ["SENDER_EMAIL"],
                    sender_password=os.environ["SENDER_PASSWORD"],
                    recipient_email=os.environ["RECIPIENT_EMAIL"],
                    subject="IONITE - Spot Available!",
                    body=f"{template_str}\n\nIONITE Log: {index+1}, ID: {row['A']}, Block: {row['B']}, date: {row['C']}, status: {status}"
                )
                mod(index+1)
    return "Operation Success"

# Vercel entrypoint
def handler(request):
    try:
        msg = run()
        return { "statusCode": 200, "body": msg }
    except Exception as e:
        return { "statusCode": 500, "body": str(e) }
