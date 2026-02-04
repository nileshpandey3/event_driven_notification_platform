"""
Verify that migration has successfully resulted in the expected updates to the DB
"""

import pytest
from sqlalchemy import inspect

from db.engine import engine


@pytest.mark.migrations
class TestMigrations:
    """
    Verify that migrations are successfully implemented
    and verify all different use cases for the migrations
    """

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

    def __str__(self) -> str:
        return self.__class__.__name__

    def test_table_creation(self):
        """
        Verify that expected tables are created successfully as
        a result of the migration
        """
        required_tables = ["users", "user_preferences", "alembic_version"]

        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()

        for table in required_tables:
            assert table in existing_tables
