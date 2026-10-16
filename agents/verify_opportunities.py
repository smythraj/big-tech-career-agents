import datetime as dt
import html
import json
import re
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "current-opportunities.json"

class TextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)

def fetch_text(url):
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; CareerHQOpportunityVerifier/1.0)", "Accept": "text/html"})
    with urllib.request.urlopen(request, timeout=25) as response:
        body = response.read().decode("utf-8", errors="replace")
        parser = TextParser()
        parser.feed(body)
        visible = re.sub(r"\s+", " ", html.unescape(" ".join(parser.parts))).strip()
        return response.status, visible

def normalize(value):
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()

def main():
    data = json.loads(PATH.read_text(encoding="utf-8"))
    checked = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    for item in data.get("opportunities", []):
        title = item.get("title", "")
        try:
            status, text = fetch_text(item["url"])
            normalized_text = normalize(text)
            normalized_title = normalize(title)
            if "job not found" in normalized_text and normalized_title not in normalized_text:
                state = "not_found"
                detail = "The page responded, but its content indicates the job may have been removed."
            elif normalized_title and normalized_title in normalized_text:
                state = "title_found"
                detail = "The official page contains the role title. Confirm the Apply option and eligibility manually."
            else:
                state = "manual_check"
                detail = "The page responded, but automated text matching could not confirm the role title."
            item["automated_check"] = {"checked_at": checked, "http_status": status, "status": state, "detail": detail}
        except Exception as exc:
            item["automated_check"] = {"checked_at": checked, "http_status": None, "status": "unavailable", "detail": "Automated check failed: " + type(exc).__name__ + ". Open the official page manually."}
    data["last_automated_check"] = checked
    data["verification_note"] = "Automated checks only inspect official page responses and title text. A reachable page is not proof that applications are still open; click through and confirm the Apply option, location, level, and eligibility."
    PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for item in data.get("opportunities", []):
        status = item.get("automated_check", {}).get("status", "unknown")
        print(item.get("company"), item.get("title"), status)

if __name__ == "__main__":
    main()
