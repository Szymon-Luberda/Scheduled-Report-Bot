import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from scheduled_report_bot.reporting import load_config, render_report, run


class ReportingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        self.input_file = self.root / "orders.csv"
        self.input_file.write_text(
            "date,region,revenue\n"
            "2025-02-01,EU-West,125.50\n"
            "2025-02-02,EU-East,20\n"
            "2025-02-03,EU-West,4.25\n",
            encoding="utf-8",
        )

    def test_render_report_summarizes_orders_and_regions(self) -> None:
        report = render_report(
            self.input_file,
            "Test Summary",
            datetime(2025, 2, 4, 9, 30, tzinfo=timezone.utc),
        )

        self.assertIn("# Test Summary", report)
        self.assertIn("Reporting period: 2025-02-01 to 2025-02-03", report)
        self.assertIn("Orders analyzed: 3", report)
        self.assertIn("Total revenue: $149.75", report)
        self.assertIn("| EU-East | $20.00 |", report)
        self.assertIn("| EU-West | $129.75 |", report)

    def test_render_report_rejects_invalid_revenue(self) -> None:
        self.input_file.write_text(
            "date,region,revenue\n2025-02-01,EU-West,not-a-number\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "CSV row 2"):
            render_report(self.input_file, "Test Summary")

    def test_config_resolves_paths_relative_to_config_file(self) -> None:
        config_file = self.root / "settings" / "config.json"
        config_file.parent.mkdir()
        config_file.write_text(
            json.dumps({
                "report_title": "Configured Summary",
                "input_file": "../orders.csv",
                "output_file": "../reports/summary.md",
                "enabled": True,
            }),
            encoding="utf-8",
        )

        config = load_config(config_file)

        self.assertEqual(config.input_file, config_file.parent / "../orders.csv")
        self.assertEqual(config.output_file, config_file.parent / "../reports/summary.md")

    def test_run_writes_report_to_configured_output(self) -> None:
        config_file = self.root / "config.json"
        output_file = self.root / "nested" / "daily-summary.md"
        config_file.write_text(
            json.dumps({
                "report_title": "Daily Summary",
                "input_file": str(self.input_file),
                "output_file": str(output_file),
                "enabled": True,
            }),
            encoding="utf-8",
        )

        result = run(load_config(config_file))

        self.assertEqual(result, output_file)
        self.assertIn("Total revenue: $149.75", output_file.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
