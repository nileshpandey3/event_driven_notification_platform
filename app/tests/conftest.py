"""
Configuration file in the Pytest framework used to define
fixtures, hooks, and plugins that are automatically discovered
and shared across multiple test files within a directory and its subdirectories
"""

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text

from app.core.config import DATABASE_URL


@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    """
    Apply Alembic migrations before any tests run.
    Ensures CI and local DB schema are identical.
    """

    engine = create_engine(DATABASE_URL)

    # Ensure database is fully reset
    # and migrated to head before running tests.
    with engine.connect() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
        conn.commit()

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    yield
    engine.dispose()
