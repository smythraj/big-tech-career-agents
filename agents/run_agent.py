import argparse
import datetime as dt
import json
import os
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
DATA = ROOT / "data"
AGENTS = {
    "daily-coach": ("Daily Study Coach", "daily-coach.md", "Build a practical 60–90 minute Google-first plan: one Java DSA problem, complexity explanation, review of one weak concept, and a short reflection. Do not claim the user completed work unless they reported it."),
    "weekly-review": ("Weekly Career Review", "weekly-review.md", "Review DSA solved and re-solved, weak topics, Java/backend, system design, mock interviews, behavioral stories, applications and referrals. Do not invent progress. End with three measurable priorities for next week."),
    "job-scout": ("Big Tech Job Scout", "job-scout.md", "Prepare a focused India job-search brief for Google first, then Atlassian, Microsoft, Meta, Adobe, Salesforce, Intuit and Walmart Global Tech. Target SWE II/III, Senior SWE, Backend and Full Stack. Without live search access, provide official career links and verification steps; never claim a vacancy is open."),
    "system-design": ("System Design Coach", "system-design.md", "Give one mid/senior system-design interview exercise: clarify requirements, estimate scale, define APIs/data model, architecture, failure modes, observability and trade-offs. End with a 10-minute practice prompt and self-review rubric.")
}
def now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
def generate(title, instruction):
    key = os.environ.get("OPENAI_API_KEY")
    stamp = now()
    if not key:
        return f"# {title}\n\nGenerated: {stamp} UTC\n\n> Free fallback mode. OPENAI_API_KEY is not configured. This is a generated starter brief, not live job verification or a claim about completed progress.\n\n## Plan\n\n{instruction}\n\n## Record actual progress\n\n- What did you complete?\n- How many focused minutes did you spend?\n- What blocked you or needs a re-solve?\n\n## Next action\n\nChoose one measurable next step and record the result in the dashboard.\n"
    payload = json.dumps({"model": os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"), "input": "You are a practical Big Tech software-engineering career coach. Be concise, honest, and actionable. Do not invent user progress, live vacancies, or completed actions.\nTask: " + instruction}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/responses", data=payload, headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=90) as response:
        data = json.loads(response.read().decode())
    result = data.get("output_text", "").strip()
    if not result:
        chunks = []
        for item in data.get("output", []):
            for part in item.get("content", []):
                if part.get("type") == "output_text":
                    chunks.append(part.get("text", ""))
        result = "\n".join(chunks).strip()
    if not result:
        raise RuntimeError("The AI API returned no text output.")
    return f"# {title}\n\nGenerated: {stamp} UTC\n\n{result}\n"
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", choices=AGENTS, required=True)
    args = parser.parse_args()
    title, filename, instruction = AGENTS[args.agent]
    REPORTS.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)
    report = generate(title, instruction)
    stamp = now()
    (REPORTS / filename).write_text(report, encoding="utf-8")
    latest_path = DATA / "latest.json"
    try:
        latest = json.loads(latest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        latest = {}
    if not isinstance(latest, dict):
        latest = {}
    latest.setdefault("reports", {})
    if not isinstance(latest["reports"], dict):
        latest["reports"] = {}
    latest["reports"][args.agent] = {
        "title": title,
        "updated_at": stamp,
        "markdown": report,
        "path": f"reports/{filename}",
        "mode": "ai" if os.environ.get("OPENAI_API_KEY") else "free-fallback"
    }
    latest["last_updated"] = stamp
    latest_path.write_text(json.dumps(latest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {filename} and data/latest.json")
if __name__ == "__main__":
    main()
