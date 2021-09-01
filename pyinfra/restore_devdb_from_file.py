"""
pyinfra @docker/sandglass_db_1 restore_devdb_from_file.py -vvv
"""

from pyinfra.operations import apt, server, files, ssh
from pyinfra.api import FactBase
from pyinfra import host, local
from decouple import config
from pyinfra.facts.server import Command


DBNAME = config('DATABASE_NAME')
DBUSER = config('DATABASE_USER')
DBPASS = config('DATABASE_PASSWORD')
CONTAINER = config('CONTAINER')
DEV_DBNAME = config('DEV_DBNAME')
DEV_DBUSER = config('DEV_DBUSER')
DUMPFILE = '/root/sql.dump'

# server.shell(
#     name='TEST',
#     get_pty=False,
#     # sudo=True,
#     # use_sudo_password=True,
#     # stdin=SUDO_PASS,
#     commands=[
#         'echo Hello from docker!',
#         # 'sudo systemctl restart nginx'
#     ],
# )
#
# a = local.shell(
#     commands='cd backupdb && ls -rt | tail -1'
# )
#

# local.shell(
#     commands=[
#         'docker compose down',
#         'docker volume rm sandglass_postgres_data',
#         'docker compose up -d',
#         'sleep 3',
#         'cd .. && python manage.py makemigrations timer',
#         'python manage.py migrate',
#         # 'python manage.py loaddata manager',
#         'python manage.py createsuperuser - -username = swasher - -email = mr.swasher @ gmail.com;'
#     ]
# )

# server.shell(
#     name='TEST2',
#     commands=f'echo {a}'
# )

server.shell(
    name='Get dump',
    commands=[
        f"pg_dump -h sandglass -U {DBUSER} -Fc -v {DBNAME} -f {DUMPFILE}",
    ]
)
server.shell(
    name='Drop database',
    commands=[
        f"su - postgres -c 'dropdb -f {DEV_DBNAME}'",
    ]
)
server.shell(
    name='Create database',
    commands=[
        f"su - postgres -c 'createdb -T template0 {DEV_DBNAME}'",
    ]
)
server.shell(
    name='Load dump into db',
    commands=[
        f"su - postgres -c 'pg_restore -d {DEV_DBNAME} {DUMPFILE}'",
    ]
)
server.shell(
    name='Restart postgres',
    commands=[
        "su - postgres -c '/etc/init.d/postgresql restart'",
    ]
)



server.shell(
    # pg_restore -U username -d dbname -1 filename.dump
    # pg_restore  -U postgres -d old_db -v "/usr/local/backup/10.70.0.61.backup"
    # -h localhost -p 5432
    # shell_executable='bash',
    # use_su_login=True,
    # su_user='postgres',
    # su_shell='bash',

    commands=[
        # f"su - postgres -c '/usr/lib/postgresql/13/bin/pg_ctl -w restart'",
        # f"su - postgres -c 'dropdb {DEV_DBNAME}'",
        # f'pg_restore -U {DEV_DBUSER} -v -d {DEV_DBNAME} < /dir_backup_outside_container/file_name.tar',
    ]
)


