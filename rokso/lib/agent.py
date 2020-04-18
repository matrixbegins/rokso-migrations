import sys, click
from .configManager import ConfigManager
from .dbManager import DBManager
from .migrationManager import MigrationManager


def init_setup(dbhost, dbname, dbusername, dbpassword, projectpath):
    """
        This function will check/create the config.json in project root.
        then it'll check/create the revision table in database
    """
    pass


def db_status():
    """
    Checks all the migrations processed so far from database
    then checks all pending migrations.
    """
    pass


def create_db_migration(tablename, filename):
    pass


def rollback_db_migration(version):
    pass


def reverse_enginner_db():
    """
        1. finds all the tabels in database
        2. extract the table definition for each table from DB
        3. create the migration files under "migrations" dir located in project root.
    """
    pass


