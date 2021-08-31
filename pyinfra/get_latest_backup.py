"""
pyinfra inventory.py get_latest_backup.py -vvv
"""

from pyinfra import host
from pyinfra.operations import server, files
from pyinfra.facts.server import Command


dbfile = host.get_fact(
    Command,
    'cd backupdb && ls -rt | tail -1'
)


server.shell(
    name='Found latest backup:',
    commands=f'echo {dbfile}',
)


files.get(
    'backupdb/' + dbfile,
    'backupdb/' + dbfile,
)