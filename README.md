# Weekly paper tracker

Local Chrome, Edge, and Brave history is checked every Friday at 11 AM (local time). A macOS `launchd` job runs the local history collector, which considers paper candidates from **any HTTPS website**. The [weekly-paper-checkpoint skill](.github/skills/weekly-paper-checkpoint/SKILL.md) guides Copilot's classification and drafting of summary points and a main takeaway from publicly accessible paper-body sections. The job writes Monday–Sunday lists, commits the results, and pushes to this public repository. Each Friday run refreshes the prior week as well as the current one, so visits after the previous Friday's checkpoint are picked up on the following Friday. Closed tabs are included; private browsing, deleted history, other devices, and non-Chromium browsers are not.

**Privacy:** Only sanitized URLs for papers with publicly fetchable bodies and successful paper classification are written to the repository. Unknown sites are not silently ignored: inaccessible, ambiguous, or non-paper candidates remain in the Git-ignored local `.review-queue/` directory, never in GitHub. Raw history databases, browser profiles, downloaded PDF bodies, tokens, and Copilot prompts are not committed. Titles, published reading candidates, generated notes, and any notes you add **are public**. Paper excerpts sent to Copilot come only from pages fetched without browser credentials. No unreviewed third-party extensions or scripts are installed.

The [weeks](weeks) directory holds editable reading checklists; check `[x]` only after reading. The [papers](papers) directory holds generated drafts and a `My notes` section for your own understanding. A browser visit is not proof of reading. When a full body cannot be extracted, inspect the local `.review-queue/YYYY-MM-DD.json`; failed fetches retry on the next run. Non-paper classifications are cached locally; remove an entry from that file to reconsider it. Drafts use selected introduction, evaluation, and conclusion sections of a public PDF or HTML paper, not a complete human reading; verify their claims before citing.

Before running on a fresh clone, create `.excluded-urls` at the repo root, with one full public paper URL per line (an empty file is valid). This local file is required, is ignored by Git, and prevents those URLs from being published in the public weekly reports.

To preview a week without network requests or writes:

```sh
python3 scripts/checkpoint.py --week 2026-09-21 --dry-run
```

To run immediately, including the current and previous week:

```sh
sh scripts/run-weekly.sh
```

Install the local job with `python3 scripts/install_launch_agent.py`. The resulting launcher is at `~/Library/LaunchAgents/com.hanhan-mom.weekly-paper-tracker.plist`. It requires a signed-in `gh` and `copilot`, Python 3, and `pdftotext` already on this Mac; it runs when the Mac is awake and your user session is logged in. Errors are logged at `~/Library/Logs/weekly-paper-tracker.log`. To inspect the job, run `launchctl print gui/$(id -u)/com.hanhan-mom.weekly-paper-tracker`.

There is no website allowlist: the collector screens candidate links, rejects private network addresses and credential-bearing queries, fetches pages without login, and lets the skill classify the body. It does not execute downloaded scripts. The historical September 17–23 list is archived separately because it overlaps two Monday–Sunday weeks.
