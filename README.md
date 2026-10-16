# Big Tech Career HQ

A free, Google-first preparation dashboard hosted on GitHub Pages with scheduled Python agents. The core study curriculum, DSA challenges, system-design exercises, mock scorecards, progress tracking, and career-search checklists work without an OpenAI API key.

## Dashboard

https://smythraj.github.io/big-tech-career-agents/

## What is useful without an API key

- **Daily Study Coach:** rotates through a built-in 30-problem Java DSA curriculum, links to the practice problem, and gives a timed 90-minute solve/explain/test/review plan.
- **System Design Coach:** rotates through practical mid/senior interview scenarios with APIs, data models, architecture prompts, reliability risks, trade-offs, and a 20-point self-review rubric.
- **Weekly Career Review:** gives three concrete weekly targets and a scorecard for actual study, re-solves, mock practice, and applications.
- **Big Tech Job Scout:** provides official careers links and an application verification checklist. It never claims a role is open unless individual listings can be extracted and then manually reconfirmed.
- **Daily Career Research:** collects recent news-search leads and free learning resources. News leads are not verified vacancies.
- **Mock interview scorecards:** record problem solving, communication, complexity/trade-offs, and testing from 1–5 each. The dashboard shows the average score out of 20.
- **Preparation execution score:** summarizes recent study consistency, completed DSA practice entries, mock scores, and application-pipeline hygiene. It is a progress indicator only, not a probability of getting hired.
- **Study log, tasks, job pipeline, JSON backup, and optional private Gist sync:** keep your practice and next actions organized. Data remains in the current browser unless you export it or configure cloud sync.

## Six-month roadmap

See [ROADMAP.md](ROADMAP.md) for the plan from 16 October 2026 through 16 April 2027, monthly milestones, daily study rhythm, weekly scorecard, and readiness gates. An offer is a goal, not a guarantee.

## Scheduled workflows

- Daily Study Coach — 9:00 PM IST.
- Big Tech Job Scout — 8:00 AM IST.
- Daily Career Research — 8:30 AM IST.
- System Design Coach — Wednesday at 8:30 PM IST.
- Weekly Career Review — Sunday at 7:00 PM IST.

GitHub may delay scheduled workflows. You can manually start any workflow from [Actions](https://github.com/smythraj/big-tech-career-agents/actions).

## Optional AI reports

The built-in curriculum does not require an API key. If you add a repository secret named `OPENAI_API_KEY`, the four coaching workflows can instead request AI-generated reports. API usage may incur charges. Never place keys in source files or the dashboard. The free curriculum remains available without this secret.

## Optional progress-aware scheduled coaching

The dashboard can sync tasks, study logs, mock scorecards and job pipeline data to a private GitHub Gist. To let scheduled agents read your progress, configure repository secret `CAREER_GIST_TOKEN` using a token with only the `gist` scope and repository variable `CAREER_GIST_ID` with your private Gist ID. Without this optional setup, scheduled agents use the built-in curriculum and do not claim to know your personal progress.

## Privacy and limitations

GitHub Pages is hosted from a public repository, so repository source files and committed reports are public. Never commit personal data, job application notes, tokens, passwords, or API keys. Use the private Gist only for personal progress. A token entered in the dashboard is used for that page session and is not saved by the page; keep it private and revoke it if exposed.

A successful HTTP response from Google Careers only confirms that the search page responded. If the checker cannot extract individual listings, no vacancy has been verified. Open each employer's official listing to confirm current status, location, level, minimum qualifications, and eligibility before applying.

## Regular-use routine

1. Open the dashboard and read the Daily Study Coach challenge.
2. Attempt one problem in Java under a timer; explain the invariant and complexity.
3. Test edge cases and record the real outcome and blocker.
4. Complete one system-design or backend drill according to the weekly plan.
5. Record a mock scorecard after timed practice.
6. Review official roles and update each role's next action.
7. On Sunday, review the weekly report and choose three measurable priorities.

Consistency, deliberate practice, feedback, suitable applications, and interview performance can improve readiness, but no dashboard or routine can guarantee a 90% chance of receiving a Google offer.
