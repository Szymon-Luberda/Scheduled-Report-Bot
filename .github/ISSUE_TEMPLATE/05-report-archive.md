---
name: Archive historical reports
about: Keep dated report outputs for later review.
title: "[Feature] Archive generated reports by date"
labels: enhancement
assignees: ""
---

## Goal

Retain a dated report for each scheduled run instead of replacing a single output file.

## Acceptance criteria

- Include the report date in the output filename.
- Configure artifact retention in the workflow.
- Ensure manual reruns for the same date have a documented overwrite policy.
- Add tests for stable filenames and document how to retrieve archived reports.
