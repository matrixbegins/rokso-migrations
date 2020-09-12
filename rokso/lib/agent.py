import sys, click, json, os, uuid
from .configManager import ConfigManager
from .dbManager import DBManager
from .migrationManager import MigrationManager
from tabulate import tabulate


json_dict = {}
initial_dirs = ["migration"]

def custom_exit(CODE, message="", ex=""):

    print("\n❌ Oooo... snap     \_(-_-)_/  \n"  )
    if ex!="":
        print(ex)
    if message!="":
        print( message, "\n")

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
    except FileExistsError as e:
        custom_exit(0, "", e)
    except Exception as e:
        custom_exit(1, "Unable to initialize rokso.", e)

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
    cwd = get_cwd()
    try:
        db = DBManager(ConfigManager().get_config(cwd).get("database"))
        cols , data = db.get_database_state()
    except FileNotFoundError as ex:
        custom_exit(1, "It seems the project setup is not complete.\nPlease run `rokso init` first.", ex)

    # get all successful migrations
    completed_migs = list(filter(lambda el: el[3] == "complete", data))

    # get any previous failed migrations
    failed_migs = list(filter(lambda el: el[3] == "error", data))

    print("Last few successful migrations: ")
    print(tabulate(completed_migs[-10:], headers=cols))

    if len(failed_migs) > 0:
        print("\n[❗] However we have detected few failed migrations in the past. \n Please fix them first.\n")
        print(tabulate(failed_migs, headers=cols))
        custom_exit(0)

    mg = MigrationManager(cwd + os.path.sep + 'migration')
    pending_migrations = mg.get_pending_migrations(data)

    if len(pending_migrations) > 0:
        toshow = []
        for pending in pending_migrations:
            toshow.append((pending, 'NA', 'pending'))

        print("\nPending migrations for application: ")
        print(tabulate(toshow, headers=('filename', 'version', 'status')))
        print("\n")
    else:
        print("\nNo new migration to process.\n")


def create_db_migration(tablename, filename):
    mg = MigrationManager(get_cwd() + os.path.sep + 'migration')

    mg.create_migration_file(tablename, filename)


def apply_migration(migration_file_name):
    """
        Checks if any previous migration is in
        @TODO:: check lockings for ALTER statements
        @TODO:: check for all/none or dependencies multi-table entries
    """
    version_no = str(uuid.uuid4())[:8]
    cwd = get_cwd()
    try:
        db = DBManager(ConfigManager().get_config(cwd).get("database"))
        col, data = db.get_database_state()
    except FileNotFoundError as ex:
        custom_exit(1, "It seems the project setup is not complete.\nPlease run `rokso init` first.", ex)

    # get any previous failed migrations
    failed_migs = list(filter(lambda el: el[3] == "error", data))

    failed_files = [f[1] for f in failed_migs]

    mg = MigrationManager(cwd + os.path.sep + 'migration')
    if migration_file_name:
        # if migration file is not in among the previously failed migrations then do not proceed.
        if len(failed_migs) > 0 and migration_file_name != failed_files[0]:
            print("""\n[❗] We have detected some failed migrations which still need to be fixed.
The given migration file name is not same or belongs to the list of below failed migration.
Please fix below files and follow the following order to apply migration. """)
            print(tabulate(failed_migs, headers=col))
            custom_exit(1)

        # process single migration
        sql = mg.import_single_migration(migration_file_name)

        try:
            print("🌀Applying migration file: ", migration_file_name)
            db.apply_migration(sql.get('apply'), migration_file_name, version_no)
        except Exception as ex:
            pass
        finally:
            print("✅ Your database is at revision# {}".format(version_no) )
            print("\n")

    else:
        # checking for failed migration. If present then attempt to migrate them first and do not proceed with new migrations.
        if len(failed_migs) > 0:
            print("""\n[❗] We have detected some failed migrations. Attempting to run following first.\n Once these are successful run `rokso migrate` again to apply new migrations.""")
            print(tabulate(failed_migs, headers=col))
            pending_migrations = failed_files
        else:
            pending_migrations = mg.get_pending_migrations(data)

        if len(pending_migrations) > 0:
            for p_mig in pending_migrations:

                sql = mg.import_single_migration(p_mig)
                try:
                    print("🌀Applying migration file: ", p_mig)
                    db.apply_migration(sql.get('apply'), p_mig, version_no)
                except Exception as ex:
                    print("✅ Your database is at revision# {}".format(version_no) )
                    custom_exit(1, "Your migration '{}' has failed. Please fix it and retry.".format(p_mig), ex)

            print("✅ Your database is at revision# {}".format(version_no) )
            print("\n")
        else:
            print("Nothing to migrate ....\n")


def rollback_db_migration(version):
    # check the revision number in database if nothing is found then report error
    # get all the files for the given revision number and all new revision after that.
    # render details on screen about all the eligible files for rollback
    # on confirmation process rollback one by one.
    cwd = get_cwd()
    try:
        db = DBManager(ConfigManager().get_config(cwd).get("database"))
        mg = MigrationManager(cwd + os.path.sep + 'migration')
    except FileNotFoundError as ex:
        custom_exit(1, "It seems the project setup is not complete.\nPlease run `rokso init` first.", ex)

    if version:
        cols, result = db.get_migrations_more_than_revision(version)
    else:
        cols, result = db.get_latest_db_revision()
        # getting all the files on the latest revision number
        cols, result = db.get_migrations_at_revision(result[0][2] )

    if len(result) < 1:
        custom_exit(1, "No Files to rollback. Probably {} is the latest version.".format(version))

    print("Following files will be rolledback: ")
    print(tabulate(result, headers=cols))
    confirm = input("\nPlease confirm to proceed(y/yes):")
    if confirm.lower() in ['y', 'yes']:
        try:
            for roll in result:
                sql = mg.import_single_migration(roll[1])
                print("\n🔄 Rolling back file:: ", roll[1])
                db.rollback_migration(sql.get('rollback'), roll[0])
        except Exception as ex:
            custom_exit(1, "An error occurred while performing rollback.", ex)

        print("✅ Rollback complete.\n")

    else:
        print("No operation performed.\n")


def reverse_engineer_db():
    """
        1. finds all the tables in database
        2. extract the table definition for each table from DB
        3. create the migration files under "migrations" dir located in project root.
        4. make an entry in version table for that migration
        5. @TODO:: get an optional argument of list of table for which the data should also be dumped.
        6. @TODO:: create logic for stored procedures, functions and triggers.
    """
    cwd = get_cwd()
    mg = MigrationManager(cwd + os.path.sep + 'migration')

    try:
        db = DBManager(ConfigManager().get_config(cwd).get("database"))
        cols , data = db.get_database_state()
    except FileNotFoundError as ex:
        custom_exit(1, "It seems the project setup is not complete.\nPlease run `rokso init` first.", ex)

    if len(data) > 0:
        custom_exit(1, "It seems you already have some rokso migrations in your database. Reverse engineering is possible just after the project setup.")
    else:
        print("Starting reverse engineering")
        version_no = str(uuid.uuid4())[:8]
        headers, data = db.select_query("show tables;")
        print("I found {} tables in the database... ".format(len(data)))
        print(tabulate(data, headers=headers))
        print("\n")

        for table in data:
            print('creating migration for table: ', table[0])
            if table[0] != db.revision_table:
                header, definition = db.get_table_definition(table[0])
                print(definition[0][0])
                # print(definition[0][1])
                migration_file_name = mg.create_migration_file_with_sql(table[0], definition[0][1])
                # now insert into the migration_version table
                db.insert_new_migration(migration_file_name, version_no, "complete" )

        print("✅ Reverse engineering of database complete. \n your database is at revision# {}\n".format(version_no))

def last_success():

    db = DBManager(ConfigManager().get_config(get_cwd()).get("database"))
    try:
        cols , data = db.get_latest_db_revision()
        if len(data) > 0:
            print(data[0][2])
        else:
            print("No last revion detected")
            exit(0)
    except Exception as e:
        #print(e.__class__.__name__)
        if int(str(e).split('(')[0]) == 1146:
            custom_exit(0, "Table does not exist, kindly initate rokso", e)
        else:
            custom_exit(1, "something went wrong", e)

