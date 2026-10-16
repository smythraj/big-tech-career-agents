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
    "daily-coach": ("Daily Study Coach", "daily-coach.md", "Complete a 60–90 minute session: one Java DSA problem, explain complexity aloud, review one weak concept, and log the result. Start with Valid Anagram if no progress is recorded. Ask for actual progress rather than assuming tasks were completed."),
    "weekly-review": ("Weekly Career Review", "weekly-review.md", "Review the week honestly: solved DSA problems, re-solves, weak topics, Java/backend, system design, mock interviews, behavioral stories, applications and referrals. Ask for missing progress; identify three priorities for next week."),
    "job-scout": ("Big Tech Job Scout", "job-scout.md", "Prepare a job-search brief for Google first, then Atlassian, Microsoft, Meta, Adobe, Salesforce, Intuit and Walmart Global Tech. Target SWE II/III, Senior SWE, Backend and Full Stack roles in India. Without live search access, provide official career search links and verification steps, never claim specific vacancies are open."),
    "system-design": ("System Design Coach", "system-design.md", "Provide one practical system-design lesson for a mid/senior software engineer: clarify requirements, estimate scale, define APIs/data model, draw components, explain trade-offs, failure modes and observability. End with a 10-minute practice prompt.")
}
def generate(title, instruction):
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        return f"# {title}\n\nGenerated: {dt.datetime.now(dt.timezone.utc).isoformat()} UTC\n\n> Fallback mode: OPENAI_API_KEY is not configured. This report is a starter brief, not an AI-generated or live-verified result.\n\n## Today's plan\n\n{instruction}\n\n## Record actual progress\n\n- What did you complete?\n- How many focused minutes did you spend?\n- What blocked you or needs a re-solve?\n\n## Next action\n\nChoose one measurable action and record its result in the dashboard.\n"
    payload = json.dumps({"model":os.environ.get("OPENAI_MODEL","gpt-4.1-mini"),"input":"You are a practical Big Tech software-engineering career coach. Be concise, honest, and actionable. Do not invent user progress, live vacancies, or completed actions.\nTask: "+instruction}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/responses",data=payload,headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"},method="POST")
    with urllib.request.urlopen(req,timeout=90) as response:
        data=json.loads(response.read().decode())
    text=data.get("output_text","").strip()
    if not text:
        for item in data.get("output",[]):
            for part in item.get("content",[]):
                if part.get("type")=="output_text":
                    text+=part.get("text","")
    return f"# {title}\n\nGenerated: {dt.datetime.now(dt.timezone.utc).isoformat()} UTC\n\n{text.strip()}\n"
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--agent",choices=AGENTS,required=True)
    args=parser.parse_args()
    title,filename,instruction=AGENTS[args.agent]
    REPORTS.mkdir(exist_ok=True)
    DATA.mkdir(exist_ok=True)
    report=generate(title,instruction)
    (REPORTS/filename).write_text(report,encoding="utf-8")
    latest_path=DATA/"latest.json"
    try:
        latest=json.loads(latest_path.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError):
        latest={}
    latest[args.agent]={"title":title,"generated_at":dt.datetime.now(dt.timezone.utc).isoformat(),"report":f"reports/{filename}","mode":"ai" if os.environ.get("OPENAI_API_KEY") else "fallback"}
    latest_path.write_text(json.dumps(latest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(f"Updated {filename}")
if __name__=="__main__":
    main()
