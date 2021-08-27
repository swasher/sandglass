"""
pyinfra inventory.py backup_sql.py -vvv
"""

from pyinfra.operations import apt, server, files
from pyinfra.api import deploy
from decouple import config

DBUSER = config('DATABASE_USER')
DBNAME = config('DATABASE_NAME')
DBPASS = config('DATABASE_PASSWORD')

server.shell(
    name='Run an ad-hoc command',
    chdir='backupdb',
    # get_pty=True,
    stdin=DBPASS,
    commands=[
        f'pg_dump -h localhost -p 5432 -U {DBUSER} -F c -b -v -f "sandglass.backup" {DBNAME}'
    ],
)
