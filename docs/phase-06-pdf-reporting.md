# Phase 6: PDF Reporting

## Objective

Generate downloadable PDF reports with executive summary, technical findings,
network services, and remediation recommendations.

## What Recruiters Learn

- You can turn scan output into stakeholder-ready reporting.
- You understand the difference between executive and technical audiences.
- You can produce artifacts that belong in a real assessment workflow.

## Files And Modules

- `backend/app/services/reporting.py`: generates PDF reports with ReportLab.
- `backend/app/api/routes/scans.py`: exposes report download endpoint.
- `reports/`: stores generated PDF files locally.

## Code Notes

- `SimpleDocTemplate` creates a basic PDF document.
- `Paragraph` and `Spacer` keep report sections readable.
- The report filename includes the scan ID.
- The API returns reports with `FileResponse`.

## Interview Questions

1. What should be in an executive summary?
2. Why should reports include evidence and remediation?
3. How would you protect report files in production?

## Common Mistakes

- Writing only technical details with no business summary.
- Omitting remediation steps.
- Exposing reports without authentication in a real deployment.

## Security Considerations

- This portfolio version has no login yet.
- Production report downloads should require authorization.
- Reports should avoid storing sensitive response bodies.

## Resume Bullet Points

- Added PDF report generation for scan summaries, findings, and remediation guidance.
- Implemented downloadable assessment artifacts through FastAPI.

## Expected Recruiter Impression

This phase makes the project feel like a real security workflow, not just a script.

## GitHub Commit Message

```text
feat: generate downloadable security assessment reports
```
