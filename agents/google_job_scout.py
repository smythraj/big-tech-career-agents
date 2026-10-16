import datetime as dt
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, urljoin

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
FEED = DATA / "latest.json"
REPORT = REPORTS / "job-scout.md"
SEARCH_URL = "https://www.google.com/about/careers/applications/jobs/results/?q=" + quote("software engineer") + "&location=" + quote("India")

class JobLinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.current = None

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            attrs = dict(attrs)
            href = attrs.get("href", "")
            if "/about/careers/applications/jobs/results/" in href or re.search(r"/jobs/results/[^/?]+", href):
                self.current = {"url": urljoin("https://www.google.com", href), "title": ""}

    def handle_data(self, data):
        if self.current is not None:
            self.current["title"] += data

    def handle_endtag(self, tag):
        if tag == "a" and self.current is not None:
            item = {"title": " ".join(self.current["title"].split()), "url": self.current["url"]}
            if len(item["title"]) > 8 and item["title"].lower() not in {"learn more", "read more", "view job"}:
                self.links.append(item)
            self.current = None

def main():
    DATA.mkdir(exist_ok=True)
    REPORTS.mkdir(exist_ok=True)
    stamp = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    result = {"checked_at": stamp, "source": SEARCH_URL, "status": "unavailable", "http_status": None, "jobs": [], "message": ""}
    request = urllib.request.Request(SEARCH_URL, headers={"User-Agent": "Mozilla/5.0 (compatible; CareerHQJobScout/1.0)", "Accept": "text/html"})
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            html = response.read().decode("utf-8", errors="replace")
            result["http_status"] = response.status
        parser = JobLinkParser()
        parser.feed(html)
        unique = {}
        for item in parser.links:
            unique[item["url"]] = item
        result["jobs"] = list(unique.values())[:30]
        result["status"] = "checked"
        result["message"] = "The official Google Careers search page returned HTTP 200. Open each result and reconfirm it is still open, in the intended location, and suitable before applying."
        if not result["jobs"]:
            result["message"] = "The official Google Careers page returned HTTP 200, but no individual job links could be extracted. Page rendering may have changed; no vacancy is claimed."
    except Exception as exc:
        result["message"] = "Live verification failed: " + type(exc).__name__ + ". No vacancy is claimed. Open the official search page directly."
    (DATA / "google-jobs.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report = REPORT.read_text(encoding="utf-8") if REPORT.exists() else "# Big Tech Job Scout\n"
    marker = "## Live Google Careers check"
    report = report.split(marker)[0].rstrip()
    report += "\n\n" + marker + "\n\nChecked at: " + stamp + " UTC\n\nOfficial source: " + SEARCH_URL + "\n\n" + result["message"] + "\n"
    if result["jobs"]:
        report += "\n" + "\n".join("- [" + item["title"].replace("[", "\\[") + "](" + item["url"] + ")" for item in result["jobs"]) + "\n"
    report += "\nThese are links found on the official search page at the timestamp above, not a guarantee that a role remains open. Confirm on the linked employer page before applying.\n"
    REPORT.write_text(report, encoding="utf-8")
    try:
        latest = json.loads(FEED.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        latest = {"reports": {}}
    latest.setdefault("reports", {})
    entry = latest["reports"].setdefault("job-scout", {"title": "Big Tech Job Scout", "path": "reports/job-scout.md", "mode": "free-fallback"})
    entry["title"] = "Big Tech Job Scout"
    entry["updated_at"] = stamp
    entry["markdown"] = report
    entry["path"] = "reports/job-scout.md"
    entry["live_check"] = {"status": result["status"], "checked_at": stamp, "result_count": len(result["jobs"]), "source": SEARCH_URL}
    latest["last_updated"] = stamp
    FEED.write_text(json.dumps(latest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Google Careers check status:", result["status"], "extracted links:", len(result["jobs"]))

if __name__ == "__main__":
    main()
