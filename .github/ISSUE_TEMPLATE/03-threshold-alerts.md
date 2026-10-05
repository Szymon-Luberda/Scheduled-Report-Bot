---
name: Highlight revenue thresholds
about: Surface regions whose revenue reaches a configured threshold.
title: "[Feature] Highlight revenue threshold breaches"
labels: enhancement
assignees: ""
---

## Goal

Use a configurable revenue threshold to call attention to regions that meet or exceed it.

## Acceptance criteria

- Read an optional non-negative threshold from the JSON configuration.
- Mark qualifying regions clearly in the generated report.
- Preserve the current report format when no threshold is configured.
- Add tests for below-threshold, equal-to-threshold, and above-threshold values.
