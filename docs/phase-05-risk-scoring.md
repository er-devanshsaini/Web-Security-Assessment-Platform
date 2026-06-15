# Phase 5: Risk Scoring Engine

## Objective

Prioritize vulnerabilities by calculating a simple risk score from severity and
network exposure.

## What Recruiters Learn

- You understand vulnerability prioritization.
- You can convert technical findings into decision-friendly risk levels.
- You know scoring should be explainable, not mysterious.

## Files And Modules

- `backend/app/services/risk.py`: calculates score and risk level.
- `backend/app/services/scan_runner.py`: applies scoring after checks complete.

## Code Notes

- Severity values map to points: high findings count more than low findings.
- Open services add a small exposure score.
- The final score is capped at 100.
- Risk levels are `informational`, `low`, `medium`, `high`, and `critical`.

## Interview Questions

1. Why is vulnerability prioritization important?
2. How would CVSS differ from this project scoring model?
3. Why should scoring be explainable to stakeholders?

## Common Mistakes

- Making every finding high severity.
- Hiding scoring rules from users.
- Ignoring exposed services when estimating risk.

## Security Considerations

- The score is a triage aid, not a formal compliance grade.
- Network exposure is weighted lightly to avoid overclaiming risk.

## Resume Bullet Points

- Built an explainable risk scoring engine for security findings and exposed services.
- Added severity-based prioritization to guide remediation order.

## Expected Recruiter Impression

This phase shows judgment, which is what internship reviewers look for beyond syntax.

## GitHub Commit Message

```text
feat: add risk scoring and finding prioritization
```
