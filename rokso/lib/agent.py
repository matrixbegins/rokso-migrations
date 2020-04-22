import sys, click
from .configManager import ConfigManager
from .dbManager import DBManager
from .migrationManager import MigrationManager
import json
import os


json_dict = {}
initial_dirs = ["migration"]

def custom_exit(CODE, ex, message = " "):

    print("[#] Oooo... snap     \_(-_-)_/ ")
    print(ex)
    print(message)
    exit(CODE)

def get_cwd():
    print("cwd:: ", os.getcwd())
    return os.getcwd()

def init_setup(dbhost, dbname, dbusername, dbpassword, projectpath):
    """
        This function will check/create the config.json in project root.
        then it'll check/create the revision table in database
    """
    cwd = get_cwd()

    json_dict = { "host": dbhost, "database": dbname, "user": dbusername, "password": dbpassword }

    try:
        CMobj = ConfigManager()
        CMobj.init(json_dict, projectpath)
    except Exception as e:
        print(e)
        custom_exit(1, e, "Issues while creating migration directory.")

    config = CMobj.get_config(cwd)
    # print(config)


def db_status():
    """
    Checks all the migrations processed so far from database
    then checks all pending migrations.
    """

    db = DBManager(ConfigManager().get_config(get_cwd()).get("database"))
    return db.get_database_state()


def create_db_migration(tablename, filename):
    mg = MigrationManager(get_cwd() + os.path.sep + 'migration')

    mg.create_migration_file(tablename, filename)


def rollback_db_migration(version):
    pass


def reverse_enginner_db():
    """
        1. finds all the tabels in database
        2. extract the table definition for each table from DB
        3. create the migration files under "migrations" dir located in project root.
    """
    print("starting rev eng:: ")

    mg = MigrationManager(get_cwd() + os.path.sep + 'migration')

    # mg.import_migration_files()

    # mg.import_single_migration( 'table2', 'create_table2.py')

    print(mg.get_all_migration_files())

    # if not db_status():
    #     print("ERROR::!")
    # else:
    #     pass
