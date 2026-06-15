import shutil
import subprocess
import xml.etree.ElementTree as ET

from backend.app.database.models import NetworkService
from backend.app.services.url_utils import is_private_or_local_hostname


def run_nmap_scan(scan_id: int, hostname: str) -> tuple[list[NetworkService], str | None]:
    """Run a conservative Nmap service scan and parse open TCP services."""
    if not hostname:
        return [], "No hostname was available for network scanning."

    if is_private_or_local_hostname(hostname):
        return [], "Local/private-looking hostnames are skipped by default."

    if shutil.which("nmap") is None:
        return [], "Nmap is not installed or not available on PATH."

    command = [
        "nmap",
        "-sV",
        "-T3",
        "--top-ports",
        "20",
        "-oX",
        "-",
        hostname,
    ]

    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return [], "Nmap scan timed out after 60 seconds."

    if completed.returncode not in {0, 1}:
        return [], completed.stderr.strip() or "Nmap scan failed."

    return parse_nmap_xml(scan_id, completed.stdout), None


def parse_nmap_xml(scan_id: int, xml_output: str) -> list[NetworkService]:
    """Parse Nmap XML into database-friendly service rows."""
    services: list[NetworkService] = []

    try:
        root = ET.fromstring(xml_output)
    except ET.ParseError:
        return services

    for port in root.findall(".//port"):
        state = port.find("state")
        if state is None or state.attrib.get("state") != "open":
            continue

        service = port.find("service")
        services.append(
            NetworkService(
                scan_id=scan_id,
                port=int(port.attrib["portid"]),
                protocol=port.attrib.get("protocol", "tcp"),
                state="open",
                service_name=service.attrib.get("name", "unknown") if service is not None else "unknown",
                product=service.attrib.get("product") if service is not None else None,
                version=service.attrib.get("version") if service is not None else None,
            )
        )

    return services
