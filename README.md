# Big Tech Career HQ

A mobile-friendly personal dashboard and scheduled GitHub Actions career agents for Google-first preparation, daily career research, job checks, and progress reviews.

## Dashboard

After enabling GitHub Pages with **Settings → Pages → Build and deployment → Source: GitHub Actions**, the dashboard should publish at:

https://smythraj.github.io/big-tech-career-agents/

## Six-month roadmap\n\nSee [ROADMAP.md](ROADMAP.md) for the 16 October 2026–16 April 2027 plan, monthly milestones, daily study rhythm, weekly scorecard, and readiness gates. This is a target plan, not a guarantee of a job offer.\n\n## Included workflows

- Daily Study Coach — daily at 9:00 PM India Standard Time.
- Weekly Career Review — Sunday at 7:00 PM India Standard Time.
- Big Tech Job Scout — daily at 8:00 AM India Standard Time.\n- Daily Career Research — daily at 8:30 AM India Standard Time; gathers news-search leads, checks the official Google Careers page, and publishes study resources.
- System Design Coach — Wednesday at 8:30 PM India Standard Time.

Schedules use UTC and GitHub may delay scheduled workflows during high load. You can manually run a workflow from the Actions tab.

## Optional AI reports

Without a repository secret named OPENAI_API_KEY, agents write clearly labeled fallback briefs. To enable AI-generated reports, open **Settings → Secrets and variables → Actions → New repository secret**, name it OPENAI_API_KEY, and paste your API key there. API use may incur charges. Never put keys in source files or the dashboard.

Optional repository variable: `OPENAI_MODEL = gpt-4.1-mini`. AI-personalized coaching requires `OPENAI_API_KEY`; progress-aware scheduled coaching additionally requires `CAREER_GIST_TOKEN` and `CAREER_GIST_ID` configured as described above. The fallback mode is not an AI model and must be treated as a structured starter brief.

## Privacy and limitations

The repository is public so the GitHub Pages site can be hosted on GitHub Free. Source files and reports are therefore public. Do not commit personal/private information or secrets. The dashboard stores working data in the current browser and includes optional private GitHub Gist sync. In the dashboard, enter a GitHub Personal Access Token (classic) with only the `gist` scope and select Upload / update cloud backup. The dashboard creates a private Gist and remembers only its ID locally; the token is not saved by the page. On each device, enter the token and use the same Gist ID to sync. Treat the token as a password and revoke it in GitHub settings if exposed. To let scheduled agents read your progress, add repository secret `CAREER_GIST_TOKEN` with that same gist-scoped token and repository variable `CAREER_GIST_ID` with the private Gist ID. Without those settings, scheduled reports must not claim to know your personal progress.

The job scout now attempts a live fetch of the official Google Careers India software-engineering search page, records the check timestamp and extracted official links in `data/google-jobs.json`, and labels extraction failures explicitly. A successful page fetch is not a guarantee that a role remains open; open each official listing and reconfirm availability and eligibility before applying. Other employers' listings are not yet automatically verified.

## Workflows

Open https://github.com/smythraj/big-tech-career-agents/actions to manually start any agent. Review the run logs if deployment fails.
