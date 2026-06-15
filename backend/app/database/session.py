from collections.abc import Generator

from sqlalchemy import text
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings
from app.database import models


engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    connect_args={"check_same_thread": False}
    if settings.database_url.startswith("sqlite")
    else {},
)


def create_database_tables() -> None:
    """Create database tables for local development."""
    SQLModel.metadata.create_all(engine)
    add_missing_scan_columns_for_sqlite()


def add_missing_scan_columns_for_sqlite() -> None:
    """Keep the Phase 1 SQLite database usable after later schema additions."""
    if not settings.database_url.startswith("sqlite"):
        return

    columns_to_add = {
        "normalized_url": "VARCHAR",
        "hostname": "VARCHAR",
        "http_status_code": "INTEGER",
        "uses_https": "BOOLEAN DEFAULT 0",
        "redirects_to_https": "BOOLEAN DEFAULT 0",
        "risk_score": "INTEGER DEFAULT 0",
        "risk_level": "VARCHAR DEFAULT 'unknown'",
        "report_path": "VARCHAR",
        "error_message": "VARCHAR",
        "completed_at": "DATETIME",
    }

    with engine.begin() as connection:
        existing_columns = {
            row[1] for row in connection.execute(text("PRAGMA table_info(scan)")).fetchall()
        }

        for column_name, column_type in columns_to_add.items():
            if column_name not in existing_columns:
                connection.execute(text(f"ALTER TABLE scan ADD COLUMN {column_name} {column_type}"))


def get_session() -> Generator[Session, None, None]:
    """Provide a database session to API routes."""
    with Session(engine) as session:
        yield session


_ = models
