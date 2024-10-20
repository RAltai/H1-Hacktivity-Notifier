import os, json, requests
from datetime import datetime
from typing import Dict, List, Any
from requests.auth import HTTPBasicAuth

USER_NAME = os.environ.get("H1_USER_NAME")
API_TOKEN = os.environ.get("H1_API_TOKEN")
WEBHOOK_URL = os.environ.get("GOOGLE_CHAT_WEBHOOK_URL")
OUTPUT_FILE = "hacktivity_output.json"

if not USER_NAME or not API_TOKEN:
    print("Error: H1_USER_NAME and H1_API_TOKEN environment variables must be set.")
    exit(1)

def parse_date(date_string: str) -> datetime:
    return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")

def get_hacktivity_data() -> Dict[str, Any]:
    url = "https://api.hackerone.com/v1/hackers/hacktivity"
    params = {
        "page[size]": 100,
        "page[number]": 1,
        "queryString": "disclosed:true"
    }
    try:
        response = requests.get(
            url,
            headers={"Accept": "application/json"},
            auth=HTTPBasicAuth(USER_NAME, API_TOKEN),
            params=params
        )
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return {}

    data = response.json().get("data", [])
    formatted_data = {item["attributes"]["disclosed_at"]: item for item in data}
    return formatted_data

def load_existing_entries() -> Dict[str, Any]:
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r") as file:
            return json.load(file)
    return {}

def alert(new_report: Dict[str, Any]) -> None:
    if not WEBHOOK_URL:
        print("Error: GOOGLE_CHAT_WEBHOOK_URL environment variable must be set.")
        return
    
    for disclosed_at, report_data in new_report.items():
        title = report_data["attributes"]["title"]
        url = report_data["attributes"]["url"]

        h1_logo_url = "https://www.hackerone.com/themes/hacker_one/images/branding/h1-logo.png"

        card_message = {
            "cards": [
                {
                    "header": {
                        "title": "Hacktivity Disclosed Report",
                        "imageUrl": h1_logo_url,
                        "imageStyle": "IMAGE"
                    },
                    "sections": [
                        {
                            "widgets": [
                                {
                                    "textParagraph": {
                                        "text": f"<b><font size=\"15\">{title}</font></b>"
                                    }
                                },
                                {
                                    "buttons": [
                                        {
                                            "textButton": {
                                                "text": "View Report",
                                                "onClick": {
                                                    "openLink": {
                                                        "url": url
                                                    }
                                                }
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        headers = {'Content-Type': 'application/json; charset=UTF-8'}

        try:
            response = requests.post(
                WEBHOOK_URL,
                headers=headers,
                data=json.dumps(card_message)
            )
            response.raise_for_status()
            print("Alert sent successfully.")
        except requests.RequestException as e:
            print(f"Error sending message to Google Chat: {e}")


def main():
    print("Starting H1 Hacktivity Bot!")
    data = get_hacktivity_data()
    print("Obtained Hacktivity Data...")
    existing_entries = load_existing_entries()
    print("Obtained Existing Records Data...")
    new_entries = []

    if existing_entries:
        print("Found Entries...")
        existing_dates = [parse_date(dt) for dt in existing_entries.keys()]
        latest_entry_date = max(existing_dates)

        for disclosed_at, item in data.items():
            disclosed_date = parse_date(disclosed_at)
            if disclosed_date > latest_entry_date:
                new_entries.append({disclosed_at: item})
                existing_entries[disclosed_at] = item

        for entry in new_entries:
            alert(entry)
    else:
        print("First Run, Hacktivity Data Was Stored...")
        existing_entries = data
        new_entries = [{k: v} for k, v in data.items()]

    print("Storing Data...")
    with open(OUTPUT_FILE, "w") as file:
        json.dump(existing_entries, file, indent=4)

    

if __name__ == "__main__":
    main()
