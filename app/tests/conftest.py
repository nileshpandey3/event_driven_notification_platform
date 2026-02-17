"""
Configuration file in the Pytest framework used to define
fixtures, hooks, and plugins that are automatically discovered
and shared across multiple test files within a directory and its subdirectories
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
