import datetime as dt
import email.utils
import json
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from html import unescape
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
FEED = DATA / "latest.json"
OUTPUT = DATA / "daily-research.json"
REPORT = REPORTS / "daily-research.md"
GOOGLE_CAREERS = "https://www.google.com/about/careers/applications/jobs/results/?q=" + quote("software engineer") + "&location=" + quote("India")
FEEDS = [
    ("Google SWE hiring and India roles", "https://news.google.com/rss/search?q=" + quote('Google software engineer jobs India') + "&hl=en-IN&gl=IN&ceid=IN:en"),
    ("Google engineering and hiring updates", "https://news.google.com/rss/search?q=" + quote('Google engineering hiring software careers') + "&hl=en-IN&gl=IN&ceid=IN:en"),
    ("Software engineering interview preparation", "https://news.google.com/rss/search?q=" + quote('software engineering interview preparation DSA system design') + "&hl=en-IN&gl=IN&ceid=IN:en"),
    ("India software engineering openings", "https://news.google.com/rss/search?q=" + quote('software engineer backend full stack jobs India') + "&hl=en-IN&gl=IN&ceid=IN:en"),
]
RESOURCES = [
    ("Google hiring preparation guide", "https://careers.google.com/stories/applying-to-google/", "Official guidance on Google's hiring process."),
    ("Google Careers India SWE search", GOOGLE_CAREERS, "Official live search; confirm status and requirements on each listing."),
    ("LeetCode study plans", "https://leetcode.com/studyplan/", "Structured practice for coding patterns."),
    ("NeetCode roadmap", "https://neetcode.io/roadmap", "Topic-based DSA sequence and revision."),
    ("System Design Primer", "https://github.com/donnemartin/system-design-primer", "Open-source system design study guide."),
]

def fetch(url, timeout=18):
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; CareerHQResearch/1.0)", "Accept": "application/rss+xml, application/xml, text/html"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.status, response.read().decode("utf-8", errors="replace")

def clean(value):
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", value or ""))).strip()

def read_feed(label, url):
    entry = {"topic": label, "source": url, "status": "unavailable", "items": [], "error": ""}
    try:
        status, body = fetch(url)
        entry["http_status"] = status
        root = ET.fromstring(body)
        cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=21)
        blocked_terms = ("facebook", "instagram", "tiktok", "youtube shorts")
        for node in root.findall(".//item"):
            title = clean(node.findtext("title", ""))
            link = (node.findtext("link", "") or "").strip()
            published = clean(node.findtext("pubDate", ""))
            description = clean(node.findtext("description", ""))
            if not title or not link or any(term in title.lower() for term in blocked_terms):
                continue
            try:
                published_date = email.utils.parsedate_to_datetime(published)
                if published_date.tzinfo is None:
                    published_date = published_date.replace(tzinfo=dt.timezone.utc)
                if published_date.astimezone(dt.timezone.utc) < cutoff:
                    continue
            except (TypeError, ValueError, OverflowError):
                if not published:
                    continue
            entry["items"].append({"title": title[:240], "url": link, "published": published, "summary": description[:300]})
            if len(entry["items"]) >= 5:
                break
        entry["status"] = "checked"
    except Exception as exc:
        entry["error"] = type(exc).__name__
    return entry

def main():
    DATA.mkdir(exist_ok=True)
    REPORTS.mkdir(exist_ok=True)
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    result = {"checked_at": now.isoformat(), "timezone": "UTC", "google_careers_url": GOOGLE_CAREERS, "feeds": [read_feed(label, url) for label, url in FEEDS], "resources": RESOURCES}
    try:
        status, body = fetch(GOOGLE_CAREERS)
        result["google_careers_check"] = {"status": "checked", "http_status": status, "page_title_detected": "careers" if "career" in body.lower() else "unknown", "message": "Official search page responded. This does not confirm that any specific role is open."}
    except Exception as exc:
        result["google_careers_check"] = {"status": "unavailable", "message": "Official search page check failed: " + type(exc).__name__ + ". Open the official search URL directly."}
    result["news_item_count"] = sum(len(feed["items"]) for feed in result["feeds"])
    OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["# Daily Career Research", "", "Updated: " + now.isoformat() + " UTC", "", "> Daily research leads from items published in the last 21 days, not guaranteed vacancies. Verify roles and claims on the linked source before acting.", "", "## Google Careers", "", "[" + GOOGLE_CAREERS + "](" + GOOGLE_CAREERS + ")", "", result["google_careers_check"]["message"], ""]
    for feed in result["feeds"]:
        lines.extend(["## " + feed["topic"], "", "Source: " + feed["source"], ""])
        if feed["items"]:
            for item in feed["items"]:
                suffix = " — " + item["published"] if item["published"] else ""
                lines.append("- [" + item["title"].replace("[", "\\[").replace("]", "\\]") + "](" + item["url"] + ")" + suffix)
                if item["summary"]:
                    lines.append("  " + item["summary"])
        else:
            lines.append("No items could be retrieved on this run. Status: " + feed["status"] + (", error: " + feed["error"] if feed["error"] else "") + ".")
        lines.append("")
    lines.extend(["## Stable study resources", ""])
    for title, url, summary in RESOURCES:
        lines.append("- [" + title + "](" + url + ") — " + summary)
    lines.extend(["", "## Today's action", "", "Spend 45 minutes on one Java DSA problem, 15 minutes reviewing a previous mistake, 15 minutes on Java/backend or system design, and 10 minutes checking official roles. Log actual study time and blockers in Career HQ.", ""])
    report = "\n".join(lines)
    REPORT.write_text(report, encoding="utf-8")
    try:
        latest = json.loads(FEED.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        latest = {}
    if not isinstance(latest, dict):
        latest = {}
    if not isinstance(latest.get("reports"), dict):
        latest["reports"] = {}
    latest["reports"]["daily-research"] = {"title": "Daily Career Research", "updated_at": now.isoformat(), "markdown": report, "path": "reports/daily-research.md", "mode": "live-rss-research", "live_check": {"status": result["google_careers_check"]["status"], "checked_at": now.isoformat(), "news_item_count": result["news_item_count"]}}
    latest["last_updated"] = now.isoformat()
    FEED.write_text(json.dumps(latest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Daily research completed:", result["news_item_count"], "news items; Google Careers:", result["google_careers_check"]["status"])

if __name__ == "__main__":
    main()
