# Scheduled Report Bot

Scheduled Report Bot helps teams get a reliable daily view of sales without manually reviewing spreadsheets: it reads the provided synthetic order data, validates and summarizes revenue by region, writes a Markdown report, and runs automatically on weekdays through GitHub Actions.

## Quick start

Requires Python 3.12 or newer.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
scheduled-report-bot
```

The default settings are in [`config.json`](config.json), and the sample input is in [`data/sample_sales.csv`](data/sample_sales.csv). The generated report is written to `reports/daily-summary.md`.

Run the test suite with:

```powershell
python -m unittest discover -s tests -v
```

The GitHub Actions workflow runs the report on weekdays at 09:30 UTC and uploads the generated Markdown file as a workflow artifact. It can also be started manually from the Actions tab.

## Project board

The planned feature backlog and Todo / In progress / Done board are documented in [`docs/project-board.md`](docs/project-board.md). The issue descriptions are available as templates under [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/); they can be used to create the corresponding GitHub issues.
