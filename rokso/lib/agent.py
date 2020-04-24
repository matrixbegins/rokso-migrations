import sys, click, json, os, uuid
from .configManager import ConfigManager
from .dbManager import DBManager
from .migrationManager import MigrationManager
from tabulate import tabulate


json_dict = {}
initial_dirs = ["migration"]

def custom_exit(CODE, ex, message = " "):

    print("[#] Oooo... snap     \_(-_-)_/ ")
    print(ex)
    print( "✅", message)
    exit(CODE)

def get_cwd():
    print("working directory:: ", os.getcwd())
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

    db = DBManager(config.get("database"))
    db.create_version_table()


def db_status():
    """
    Checks all the migrations processed so far from database
    then checks all pending migrations.
    1. @TODO:: if referring filenames from database entries
        devise a way for OS's directory seperator to access files without a problem.
    """

    db = DBManager(ConfigManager().get_config(get_cwd()).get("database"))
    cols , data = db.get_database_state()

    print("Last few successful migrations: ")
    print(tabulate(data[-10:], headers=cols))
    
    error_files = []
    for file in data:
        if file[3] == "error":
            error_files.append(file[1])
            print(" ")
            print("[*] Below files are in failed state, Kindly fix those first")
            print("[.] {}".format(*error_files), sep = "\n")
            custom_exit(1, " ")

    mg = MigrationManager(get_cwd() + os.path.sep + 'migration')
    pending_migrations = mg.get_pending_migrations(data)
    print(pending_migrations)
    toshow = []
    for pending in pending_migrations:
        toshow.append((pending, 'NA', 'pending'))

    print("\nPending migrations for application: ")
    print(tabulate(toshow, headers=('filename', 'version', 'status')))


def create_db_migration(tablename, filename):
    mg = MigrationManager(get_cwd() + os.path.sep + 'migration')

    mg.create_migration_file(tablename, filename)


def apply_migration(migration_file_name):
    """
        Checks if any previous migration is in
    """
    version_no = str(uuid.uuid4())[:8]
    db = DBManager(ConfigManager().get_config(get_cwd()).get("database"))
    col, data = db.get_database_state()
    mg = MigrationManager(get_cwd() + os.path.sep + 'migration')
    if migration_file_name:
        # process single migration
        sql = mg.import_single_migration(migration_file_name)
        # print(sql)
        # @TODO:: check previous state of database if there is an existing migrations in error state then do not proceed.

        try:
            db.apply_migration(sql.get('apply'), migration_file_name, version_no)
        except Exception as ex:
            pass
        finally:
            print("✅ Your database is at revision# {}".format(version_no) )

    else:
        pending_migrations = mg.get_pending_migrations(data)

        for p_mig in pending_migrations:         
           
            sql = mg.import_single_migration(p_mig)

            try:
                 db.apply_migration(sql.get('apply'), p_mig, version_no)
            except Exception as ex:
                 pass
            finally:
                 print("Your database is at revision# {}".format(version_no) )



def rollback_db_migration(version):
    pass


def reverse_enginner_db():
    """
        1. finds all the tables in database
        2. extract the table definition for each table from DB
        3. create the migration files under "migrations" dir located in project root.
        4. make an entry in version table for that migration
        5. @TODO:: get an optional argument of list of table for which the data should also be dumped.
        6. @TODO:: create logic for stored procedures, functions and triggers.

    """
    mg = MigrationManager(get_cwd() + os.path.sep + 'migration')

    db = DBManager(ConfigManager().get_config(get_cwd()).get("database"))
    cols , data = db.get_database_state()

    if len(data) > 0:
        custom_exit(1, "It seems you already have some rokso migrations in your database. Reverse engineering is possible just after the project setup.")
    else:
        print("Starting reverse engineering")
        version_no = str(uuid.uuid4())[:8]
        headers, data = db.select_query("show tables;")
        print("I found {} tables in the database... ".format(len(data)))
        print(tabulate(data, headers=headers))

        for table in data:
            print('creating migration for table: ', table[0])
            if table[0] != db.revision_table:
                header, definition = db.get_table_definition(table[0])
                print(definition[0][0])
                # print(definition[0][1])
                migration_file_name = mg.create_migration_file_with_sql(table[0], definition[0][1])
                # now insert into the migration_version table
                db.insert_new_migration(migration_file_name, version_no, "complete" )

        print("✅ Reverse enginnering of database complete. \n your database is at revision# {}".format(version_no))
