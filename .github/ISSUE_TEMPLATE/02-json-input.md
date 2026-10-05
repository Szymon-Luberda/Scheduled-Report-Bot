---
name: Support JSON input data
about: Accept JSON order files as an alternative to CSV.
title: "[Feature] Read orders from JSON files"
labels: enhancement
assignees: ""
---

## Goal

Allow the bot to read the same order fields from a JSON input file as well as CSV.

## Acceptance criteria

- Choose CSV or JSON based on an explicit configuration setting or file extension.
- Validate that each order has a date, region, and numeric revenue.
- Keep the existing CSV behavior unchanged.
- Add tests for valid JSON, missing fields, and malformed JSON.
