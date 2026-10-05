---
name: Add reporting-period filters
about: Let users choose which sales dates appear in the summary.
title: "[Feature] Filter the report by date range"
labels: enhancement
assignees: ""
---

## Goal

Allow a report run to include orders from a configurable start and end date instead of always summarizing the full input file.

## Acceptance criteria

- Support an optional start date and end date in the configuration.
- Exclude orders outside the selected range and report the effective period.
- Reject invalid dates and a start date later than the end date with a clear error.
- Add tests for inclusive boundaries and empty matching ranges.
