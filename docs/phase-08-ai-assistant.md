# Phase 8: AI Security Assistant

## Objective

Provide human-readable explanations and remediation suggestions for scan results.

## What Recruiters Learn

- You can turn technical findings into analyst-friendly language.
- You understand how AI features should support, not replace, security judgment.
- You can design an assistant feature that works locally without leaking data.

## Files And Modules

- `backend/app/services/assistant.py`: creates summaries and prioritized remediation steps.
- `backend/app/api/routes/scans.py`: exposes `/api/scans/{scan_id}/assistant`.
- `frontend/src/main.jsx`: displays assistant output.

## Code Notes

- The assistant is deterministic and local.
- It summarizes severity mix, top categories, risk score, and network exposure.
- It prioritizes the highest severity remediation items first.

## Interview Questions

1. Why might a local assistant be safer than sending findings to an external API?
2. How would you validate AI-generated security advice?
3. What guardrails should an AI security assistant have?

## Common Mistakes

- Letting AI invent vulnerabilities not supported by evidence.
- Sending sensitive scan data to third-party services without consent.
- Using vague remediation advice.

## Security Considerations

- The assistant only summarizes stored findings.
- It does not claim exploitability beyond available evidence.
- A future OpenAI integration should redact secrets and require explicit opt-in.

## Resume Bullet Points

- Built an AI-style assistant that explains findings and generates remediation plans.
- Designed assistant output around evidence-backed security recommendations.

## Expected Recruiter Impression

This phase shows that you can apply AI carefully in a security workflow.

## GitHub Commit Message

```text
feat: add security assistant explanations
```
