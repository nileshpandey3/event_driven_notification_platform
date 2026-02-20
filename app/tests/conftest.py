"""
The conftest.py file serves as a means of providing fixtures for an entire directory.
Fixtures defined in a conftest.py can be used
by any test in that package without needing to import them
(pytest will automatically discover them).
"""
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
