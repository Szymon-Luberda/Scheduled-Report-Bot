from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Sequence


REQUIRED_COLUMNS = {"date", "region", "revenue"}


@dataclass(frozen=True)
class ReportConfig:
    report_title: str
    input_file: Path
    output_file: Path
    enabled: bool


def _resolve_path(value: object, key: str, config_dir: Path) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Configuration value '{key}' must be a non-empty path.")
    path = Path(value)
    return path if path.is_absolute() else config_dir / path


def load_config(config_path: Path) -> ReportConfig:
    config_dir = config_path.resolve().parent
    values = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(values, dict):
        raise ValueError("Configuration must be a JSON object.")

    title = values.get("report_title")
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Configuration value 'report_title' must be a non-empty string.")

    enabled = values.get("enabled", True)
    if not isinstance(enabled, bool):
        raise ValueError("Configuration value 'enabled' must be true or false.")

    return ReportConfig(
        report_title=title.strip(),
        input_file=_resolve_path(values.get("input_file"), "input_file", config_dir),
        output_file=_resolve_path(values.get("output_file"), "output_file", config_dir),
        enabled=enabled,
    )


def render_report(
    input_file: Path,
    report_title: str,
    generated_at: datetime | None = None,
) -> str:
    revenue_by_region: dict[str, Decimal] = {}
    dates: list[date] = []
    order_count = 0
    total_revenue = Decimal("0")

    with input_file.open(encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames is None:
            raise ValueError(f"Input file '{input_file}' is missing a CSV header.")
        missing_columns = REQUIRED_COLUMNS.difference(reader.fieldnames)
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"Input file '{input_file}' is missing required columns: {missing}.")

        for row_number, row in enumerate(reader, start=2):
            try:
                order_date = date.fromisoformat(row["date"].strip())
                region = row["region"].strip()
                revenue = Decimal(row["revenue"].strip())
            except (AttributeError, InvalidOperation, ValueError) as error:
                raise ValueError(f"Invalid date, region, or revenue on CSV row {row_number}.") from error

            if not region:
                raise ValueError(f"Region is empty on CSV row {row_number}.")
            if not revenue.is_finite() or revenue < 0:
                raise ValueError(f"Revenue must be a finite, non-negative number on CSV row {row_number}.")

            dates.append(order_date)
            total_revenue += revenue
            revenue_by_region[region] = revenue_by_region.get(region, Decimal("0")) + revenue
            order_count += 1

    if order_count == 0:
        raise ValueError(f"Input file '{input_file}' contains no order rows.")

    timestamp = generated_at or datetime.now(timezone.utc)
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    timestamp = timestamp.astimezone(timezone.utc)

    lines = [
        f"# {report_title}",
        "",
        f"Generated: {timestamp:%Y-%m-%d %H:%M:%S UTC}",
        f"Reporting period: {min(dates).isoformat()} to {max(dates).isoformat()}",
        f"Orders analyzed: {order_count}",
        f"Total revenue: ${total_revenue:,.2f}",
        "",
        "## Revenue by region",
        "",
        "| Region | Revenue |",
        "| --- | ---: |",
    ]
    lines.extend(
        f"| {region} | ${amount:,.2f} |"
        for region, amount in sorted(revenue_by_region.items())
    )
    return "\n".join(lines) + "\n"


def run(config: ReportConfig) -> Path | None:
    if not config.enabled:
        print("Report generation is disabled in the configuration.")
        return None

    report = render_report(config.input_file, config.report_title)
    config.output_file.parent.mkdir(parents=True, exist_ok=True)
    config.output_file.write_text(report, encoding="utf-8")
    print(f"Report written to {config.output_file}")
    return config.output_file


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a sales summary report.")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config.json"),
        help="Path to the JSON configuration file (default: config.json).",
    )
    args = parser.parse_args(argv)
    run(load_config(args.config))
    return 0
