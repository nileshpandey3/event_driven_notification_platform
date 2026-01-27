import os
from logging.config import fileConfig

from alembic import context

from app.core.config import DATABASE_URL
from db.base import Base
from models.user_preferences import UserPreferences
from models.users import Users


def get_pgres_db_url():
    url = os.getenv(DATABASE_URL)
    if not url:
        return '{DATABASE_URL} env var is not set'
    return url

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option('sqlalchemy.url', get_pgres_db_url())

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
