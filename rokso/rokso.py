import click


@click.group()
def cli():
    pass

@click.command('init', short_help='🚀 init your migration project. configures db connection parameters')
@click.option('--dbhost', prompt='Enter database hostname: ',
    required=True, envvar='MIG_DB_HOST',
    help="Database host where rokso will connect to.")
@click.option('--dbname', prompt='Enter database name: ',
    required=True, envvar='MIG_DB_NAME',
    help="Database name where rokso will apply migrations.")
@click.option('--dbusername', prompt='Enter database username: ',
    required=True, envvar='MIG_DB_USER', help="Database username for connecting database.")
@click.option('--dbpassword', prompt='Enter database password:',
    required=True, hide_input=True, envvar='MIG_DB_PASSWORD',
    help="Database password for connecting database.")
@click.option('--configpath', prompt='Enter config directory:',
    required=True, envvar='MIG_DB_CONFIG_PATH', help="rokso will store environment config here. rokso can create this directory if not exists.")
@click.option('--migrationspath', prompt='Enter path where your migration scripts will live: ',
    required=True, envvar='MIG_DB_MIGRATIONS_PATH', help="Your migration files will be created and maintained in this directory. rokso can create this directory if not exists.")
def init(dbhost, dbname, dbusername, dbpassword, configpath, migrationspath):
    """This commands configures basic environment variables that are needed to cary out database migrations.
    Make sure the given user has ALTER, ALTER ROUTINE, CREATE, CREATE ROUTINE, DELETE, DROP, EXECUTE,
    INDEX, INSERT, SELECT, SHOW DATABASES, UPDATE privileges.
    """
    click.echo('checking existing config')
    click.echo('Creating new config...')

@click.command('status', short_help='✅ checks the current state of database and pending migrations')
def status():
    """ checks the current state of database and pending migrations. It's good to run this before running migrate command. """
    click.echo('checking database status')

@click.command('remap', short_help='🔄 Reverse engineer your DB migrations from existing database.')
def remap():
    """ Reverse engineer your DB migrations from existing database.
     Make sure init command is complete and you have a valid config file and migrations directory setup. """
    click.echo('Starting remapping of existing database for versioning')

@click.command('create', short_help='➕ create a database migration.')
@click.option('--tablename', help="The table/entity name for which you want to create the migration.")
@click.option('--filename', help="Name of the migration file.")
def create(tablename, filename):
    """ Creates a migration template file for specified table/entity name. """
    click.echo('creating a migration for .....')

@click.command('migrate', short_help='⤴️  Apply all outstanding migrations to database.')
@click.option('--migration', help="Specific migration that needs to be carried out.")
def migrate(migration):
    """ Apply all outstanding migrations to database.
    By specifing --migration option you can apply just one single migration. """
    click.echo('Applying following migrations to database....' + migration)

@click.command('rollback', short_help='⤵️  Rollback last applied migration')
@click.option('--version', help="Rollbacks database state to specified version. ")
def rollback(version):
    """ Rollback last applied out migration
        By specifing --version option you can rollback to an previous DB state. """
    click.echo('Rolling back migration to revision # 123')


@click.command()
def unstage():
    click.echo('Too soon to open curtains! check back later')

cli.add_command(init)
cli.add_command(status)
cli.add_command(remap)
cli.add_command(create)
cli.add_command(migrate)
cli.add_command(rollback)

# 🛑    ⛔  🚫  ❌


if __name__ == '__main__':
    cli()