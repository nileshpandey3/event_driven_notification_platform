import pytest
from alembic import command
from alembic.config import Config

@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    """
    Apply Alembic migrations before any tests run.
    Ensures CI and local DB schema are identical.
    """
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
