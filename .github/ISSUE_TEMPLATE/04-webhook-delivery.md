---
name: Deliver reports to a webhook
about: Send completed reports to a configured team webhook.
title: "[Feature] Deliver generated reports to a webhook"
labels: enhancement
assignees: ""
---

## Goal

Optionally deliver a generated report to a team channel through a webhook.

## Acceptance criteria

- Read the webhook URL from a GitHub Actions secret, never from committed configuration.
- Send the report only when webhook delivery is enabled.
- Fail the workflow clearly if delivery is requested but fails.
- Add tests using a mocked HTTP response and document secret setup.
