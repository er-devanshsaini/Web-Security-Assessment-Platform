from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class ScanCreate(BaseModel):
    target_url: HttpUrl = Field(
        description="Website URL to assess. Only scan systems you own or have permission to test."
    )
    include_network_scan: bool = Field(default=False)


class FindingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    category: str
    severity: str
    description: str
    evidence: str
    recommendation: str
    owasp_reference: str


class NetworkServiceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    port: int
    protocol: str
    state: str
    service_name: str
    product: str | None = None
    version: str | None = None


class ScanRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    target_url: str
    status: str
    normalized_url: str | None
    hostname: str | None
    http_status_code: int | None
    uses_https: bool
    redirects_to_https: bool
    risk_score: int
    risk_level: str
    report_path: str | None
    error_message: str | None


class ScanDetail(ScanRead):
    findings: list[FindingRead]
    network_services: list[NetworkServiceRead]


class AssistantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    scan_id: int
    summary: str
    remediation_plan: list[str]
