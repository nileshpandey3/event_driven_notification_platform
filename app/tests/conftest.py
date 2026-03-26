"""
Configuration file in the Pytest framework used to define
fixtures, hooks, and plugins that are automatically discovered
and shared across multiple test files within a directory and its subdirectories
"""

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy_utils import create_database, database_exists

from app.core.config import TEST_DATABASE_URL


@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    """
    Apply Alembic migrations before any tests run.
    Ensures CI and local DB schema are identical.
    """

    assert (
        "test" in TEST_DATABASE_URL
    ), f"Refusing to wipe non-test database: {TEST_DATABASE_URL}"

    # Create Test db if it doesn't exist already
    if not database_exists(TEST_DATABASE_URL):
        create_database(TEST_DATABASE_URL)

    engine = create_engine(TEST_DATABASE_URL, future=True)

    # Ensure database is fully reset
    # and migrated to head before running tests.
    with engine.connect() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public AUTHORIZATION app_user"))
        conn.commit()

    alembic_cfg = Config("alembic.ini")

    # Make sure alembic uses test db
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)

    command.upgrade(alembic_cfg, "head")

    yield
    engine.dispose()
