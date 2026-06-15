from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class Scan(SQLModel, table=True):
    """A saved security scan request.

    Developer note:
    This table acts like the main case file for one assessment. Detailed web
    findings and network services are stored in related tables.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    target_url: str = Field(index=True)
    status: str = Field(default="created", index=True)
    normalized_url: Optional[str] = Field(default=None)
    hostname: Optional[str] = Field(default=None, index=True)
    http_status_code: Optional[int] = Field(default=None)
    uses_https: bool = Field(default=False)
    redirects_to_https: bool = Field(default=False)
    risk_score: int = Field(default=0, index=True)
    risk_level: str = Field(default="unknown", index=True)
    report_path: Optional[str] = Field(default=None)
    error_message: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = Field(default=None)


class Finding(SQLModel, table=True):
    """A web or application security issue found during a scan."""

    id: Optional[int] = Field(default=None, primary_key=True)
    scan_id: int = Field(foreign_key="scan.id", index=True)
    title: str
    category: str = Field(index=True)
    severity: str = Field(index=True)
    description: str
    evidence: str
    recommendation: str
    owasp_reference: str = Field(default="OWASP Top 10")


class NetworkService(SQLModel, table=True):
    """An open network service discovered by Nmap."""

    id: Optional[int] = Field(default=None, primary_key=True)
    scan_id: int = Field(foreign_key="scan.id", index=True)
    port: int
    protocol: str = "tcp"
    state: str = "open"
    service_name: str = "unknown"
    product: Optional[str] = None
    version: Optional[str] = None
