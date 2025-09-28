import requests
import pygsheets
import pandas as pd
from datetime import datetime

template_str = ""

# Initialize Google Sheets client
client = pygsheets.authorize(service_account_file="ionite-472813-3f097b8874d0.json")


def mod(row: int):
    """Mark a row as 0 in the Google Sheet."""
    spreadsht = client.open("IONITE")
    worksht = spreadsht.worksheet("title", "Sheet1")
    worksht.update_value(f'D{row}', '0')


def gsheet_to_csv(sheet_url_or_id: str, output_filename: str = "output.csv"):
    """Download Google Sheet as CSV and save locally."""
    import re

    # If full URL provided, extract the sheet ID
    match = re.search(r"/d/([a-zA-Z0-9-_]+)", sheet_url_or_id)
    if match:
        sheet_id = match.group(1)
    else:
        sheet_id = sheet_url_or_id

    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

    # Read directly into pandas
    df = pd.read_csv(csv_url)

    # Save to CSV
    df.to_csv(output_filename, index=False)
    print(f"✅ Saved Google Sheet as {output_filename}")
    return df


def is_not_in_past(date_string: str) -> bool:
    """Check if a YYYYMMDD date is today or in the future."""
    try:
        input_date = datetime.strptime(date_string, "%Y%m%d")
        current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return input_date >= current_date
    except ValueError:
        return False


def send(sender_email, sender_password, recipient_email, subject, body):
    """Send an email using Gmail SMTP."""
    import smtplib
    from email.message import EmailMessage
    try:
        msg = EmailMessage()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.set_content(body)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)

        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")


def post(thedate: str, theid: int, theblock: str) -> bool:
    """Check ION block for availability."""
    def get_urls_by_date(data: dict, date: str):
        for item in data.get("results", []):
            if item["date"] == date and item["block_letter"] == block:
                return item["url"]

    blocks_2025 = "https://ion.tjhsst.edu/api/blocks"
    cookies = {'sessionid': "85eiw0hfytqvhdnk056tnz5p711zakdm"}

    response = requests.get(blocks_2025, cookies=cookies)
    response.raise_for_status()
    data = response.json()

    block = theblock
    urls = get_urls_by_date(data, thedate)
    if not urls:
        return False

    day_block = f"{urls}?format=json"
    response_day_block = requests.get(day_block, cookies=cookies)
    response_day_block.raise_for_status()
    day_block_data = response_day_block.json()

    activities = day_block_data.get("activities", {})
    activity = activities.get(theid) or activities.get(int(theid))

    if activity:
        roster = activity.get("roster", {})
        count = roster.get("count", 0)
        capacity = roster.get("capacity", 0)
        spots_available = capacity - count

        global template_str
        template_str = (f"Club '{activity.get('name')}' has {spots_available} spots available "
                        f"(Filled: {count}, Capacity: {capacity})")

        print(template_str)
        return spots_available > 0
    return False


def run():
    """Main script entry point."""
    df = gsheet_to_csv(
        'https://docs.google.com/spreadsheets/d/15ozBzfMIiUXrjuABo_pzlPQ-YaSYcTI_yZlJsDNoQM0/edit?usp=sharing',
        "my_data.csv"
    )

    df = pd.read_csv('my_data.csv', names=list('ABCD'), header=None)

    logs = []
    for index, row in df.iterrows():
        if row['D'] == 1:
            status = post(row['C'], str(row['A']), row['B'])
            log_entry = f"Row {index+1}: ID={row['A']} Block={row['B']} Date={row['C']} Status={status}"
            print(log_entry)

            if is_not_in_past(row['C']):
                mod(index + 1)
            elif status:
                send(
                    sender_email="2028badivi@gmail.com",
                    sender_password="khbx ydgt mnyt giuv",  # ⚠️ move this to env vars in production!
                    recipient_email="2028badivi@gmail.com",
                    subject="IONITE - Spot Available!",
                    body=f"{template_str}\n\nLog: {log_entry}"
                )
                mod(index + 1)

            logs.append(log_entry)

    return {"status": "success", "logs": logs}
