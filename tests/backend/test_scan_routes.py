from fastapi.testclient import TestClient

from backend.app.database.models import Finding, Scan
from backend.app.main import app


def test_scan_stats_endpoint_returns_counts() -> None:
    with TestClient(app) as client:
        response = client.get("/api/scans/stats/summary")

    assert response.status_code == 200
    assert "total_scans" in response.json()


def test_create_scan_endpoint_accepts_target(monkeypatch) -> None:
    def fake_run_scan(session, scan: Scan, include_network_scan: bool) -> Scan:
        scan.status = "completed"
        scan.normalized_url = "https://example.com"
        scan.hostname = "example.com"
        scan.http_status_code = 200
        scan.uses_https = True
        scan.redirects_to_https = False
        scan.risk_score = 10
        scan.risk_level = "low"
        session.add(scan)
        session.commit()
        session.refresh(scan)
        return scan

    monkeypatch.setattr("app.api.routes.scans.run_scan", fake_run_scan)

    with TestClient(app) as client:
        response = client.post(
            "/api/scans",
            json={"target_url": "https://example.com", "include_network_scan": False},
        )

    assert response.status_code == 200
    assert response.json()["status"] == "completed"
    assert response.json()["hostname"] == "example.com"


def test_scan_detail_serializes_findings(monkeypatch) -> None:
    def fake_run_scan(session, scan: Scan, include_network_scan: bool) -> Scan:
        scan.status = "completed"
        scan.normalized_url = "https://example.org"
        scan.hostname = "example.org"
        scan.risk_score = 20
        scan.risk_level = "low"
        session.add(
            Finding(
                scan_id=scan.id,
                title="Missing HSTS",
                category="Transport Security",
                severity="medium",
                description="HSTS is missing.",
                evidence="No Strict-Transport-Security header.",
                recommendation="Add HSTS.",
            )
        )
        session.add(scan)
        session.commit()
        session.refresh(scan)
        return scan

    monkeypatch.setattr("app.api.routes.scans.run_scan", fake_run_scan)

    with TestClient(app) as client:
        created = client.post(
            "/api/scans",
            json={"target_url": "https://example.org", "include_network_scan": False},
        ).json()
        response = client.get(f"/api/scans/{created['id']}")

    assert response.status_code == 200
    assert response.json()["findings"][0]["title"] == "Missing HSTS"
