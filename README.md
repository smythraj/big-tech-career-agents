# Big Tech Career HQ

A mobile-friendly personal dashboard and four GitHub Actions career-coaching workflows.

## Dashboard

After enabling GitHub Pages with **Settings → Pages → Build and deployment → Source: GitHub Actions**, the dashboard should publish at:

https://smythraj.github.io/big-tech-career-agents/

## Included workflows

- Daily Study Coach — daily at 9:00 PM India Standard Time.
- Weekly Career Review — Sunday at 7:00 PM India Standard Time.
- Big Tech Job Scout — Monday at 8:00 AM India Standard Time.
- System Design Coach — Wednesday at 8:30 PM India Standard Time.

Schedules use UTC and GitHub may delay scheduled workflows during high load. You can manually run a workflow from the Actions tab.

## Optional AI reports

Without a repository secret named OPENAI_API_KEY, agents write clearly labeled fallback briefs. To enable AI-generated reports, open **Settings → Secrets and variables → Actions → New repository secret**, name it OPENAI_API_KEY, and paste your API key there. API use may incur charges. Never put keys in source files or the dashboard.

Optional repository variable: OPENAI_MODEL = gpt-4.1-mini.

## Privacy and limitations

The repository is public so the GitHub Pages site can be hosted on GitHub Free. Source files and reports are therefore public. Do not commit personal/private information or secrets. The dashboard's checklist, study sessions and application pipeline are stored in the current browser's local storage and do not automatically sync across devices.

The job scout workflow does not have live web search. It provides official career-site links and a verification checklist; it does not claim current vacancies are open. Verify jobs on employers' official pages.

## Workflows

Open https://github.com/smythraj/big-tech-career-agents/actions to manually start any agent. Review the run logs if deployment fails.
