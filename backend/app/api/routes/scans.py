from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlmodel import Session, select

from app.database.models import Finding, NetworkService, Scan
from app.database.session import get_session
from app.schemas import AssistantResponse, ScanCreate, ScanDetail, ScanRead
from app.services.assistant import explain_scan
from app.services.scan_runner import run_scan

router = APIRouter(prefix="/scans", tags=["Scans"])


@router.post("", response_model=ScanRead)
def create_scan(payload: ScanCreate, session: Session = Depends(get_session)) -> Scan:
    """Create and run a security scan."""
    scan = Scan(target_url=str(payload.target_url))
    session.add(scan)
    session.commit()
    session.refresh(scan)
    return run_scan(session, scan, payload.include_network_scan)


@router.get("", response_model=list[ScanRead])
def list_scans(session: Session = Depends(get_session)) -> list[Scan]:
    """Return scans ordered by newest first."""
    statement = select(Scan).order_by(Scan.id.desc())
    return list(session.exec(statement).all())


@router.get("/stats/summary")
def get_scan_stats(session: Session = Depends(get_session)) -> dict[str, object]:
    scans = list(session.exec(select(Scan)).all())
    completed = [scan for scan in scans if scan.status == "completed"]
    risk_counts: dict[str, int] = {}

    for scan in completed:
        risk_counts[scan.risk_level] = risk_counts.get(scan.risk_level, 0) + 1

    return {
        "total_scans": len(scans),
        "completed_scans": len(completed),
        "failed_scans": len([scan for scan in scans if scan.status == "failed"]),
        "risk_counts": risk_counts,
    }


@router.get("/{scan_id}", response_model=ScanDetail)
def get_scan(scan_id: int, session: Session = Depends(get_session)) -> ScanDetail:
    scan = session.get(Scan, scan_id)
    if scan is None:
        raise HTTPException(status_code=404, detail="Scan not found")

    findings = list(session.exec(select(Finding).where(Finding.scan_id == scan_id)).all())
    services = list(session.exec(select(NetworkService).where(NetworkService.scan_id == scan_id)).all())
    return ScanDetail(**scan.model_dump(), findings=findings, network_services=services)


@router.get("/{scan_id}/assistant", response_model=AssistantResponse)
def get_assistant_summary(scan_id: int, session: Session = Depends(get_session)) -> AssistantResponse:
    scan = session.get(Scan, scan_id)
    if scan is None:
        raise HTTPException(status_code=404, detail="Scan not found")

    findings = list(session.exec(select(Finding).where(Finding.scan_id == scan_id)).all())
    services = list(session.exec(select(NetworkService).where(NetworkService.scan_id == scan_id)).all())
    summary, remediation_plan = explain_scan(scan, findings, services)
    return AssistantResponse(scan_id=scan_id, summary=summary, remediation_plan=remediation_plan)


@router.get("/{scan_id}/report")
def download_report(scan_id: int, session: Session = Depends(get_session)) -> FileResponse:
    scan = session.get(Scan, scan_id)
    if scan is None or scan.report_path is None:
        raise HTTPException(status_code=404, detail="Report not found")

    report_path = Path(scan.report_path)
    if not report_path.exists():
        raise HTTPException(status_code=404, detail="Report file is missing")

    return FileResponse(
        path=report_path,
        filename=report_path.name,
        media_type="application/pdf",
    )
