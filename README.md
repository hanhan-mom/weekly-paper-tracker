# Weekly paper tracker

Local Chrome, Edge, and Brave history is checked every Sunday at 9 PM (local time). A macOS `launchd` job writes Monday–Sunday lists, asks the installed GitHub Copilot CLI for **draft** summary points and a main takeaway from available paper-body sections, commits the results, and pushes to this public repository. The following run revisits the prior week to catch late Sunday visits. Closed tabs are included; private browsing, deleted history, other devices, and non-Chromium browsers are not.

**Privacy:** Only recognized public paper URLs are written to the repository. Raw history databases, browser profiles, downloaded PDF bodies, tokens, and Copilot prompts are not committed. Titles, reading candidates, generated notes, and any notes you add **are public**. Paper text sent to Copilot is from public papers only. No unreviewed third-party extensions or scripts are installed.

The [weeks](weeks) directory holds editable reading checklists; check `[x]` only after reading. The [papers](papers) directory holds generated drafts and a `My notes` section for your own understanding. A browser visit is not proof of reading. Where a full paper cannot be extracted or summarization fails, the report explicitly says **summary pending**; the next run retries. Drafts are based on selected introduction, evaluation, and conclusion sections of a PDF, not on a complete human reading of the paper; verify their claims before citing.

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

The scanner deliberately uses an allowlist of public research sites in `scripts/checkpoint.py`. Add a new public source there after reviewing it; unsupported sites are not silently treated as papers, and PDFs without accessible main text stay pending. The historical September 17–23 list is archived separately because it overlaps two Monday–Sunday weeks.
