"""
pyinfra inventory.py restore_last_backup.py -vvv
"""

from pyinfra.operations import apt, server, files, ssh
from pyinfra.api import FactBase
from pyinfra import host
from pyinfra.facts.server import Command
from decouple import config

DBUSER = config('DATABASE_USER')
DBNAME = config('DATABASE_NAME')
DBPASS = config('DATABASE_PASSWORD')


# class RawCommandOutput(FactBase):
#     '''
#     Returns the raw output of a command.
#     '''
#
#     def command(self, command):
#         return command
#
#     def process(self, output):
#         return '\n'.join(output)  # re-join and return the output lines


dbfile = host.get_fact(Command, 'cd backupdb && ls -rt | tail -1')
#     chdir='backupdb',
#     command='ls -rt | tail -1'
# )


server.shell(
    name='Found latest backup:',
    commands=f'echo {dbfile}',
)

# print(command_output)

files.get(
    'backupdb/' + dbfile,
    dbfile,
)

server.shell(
    name='Restore db',
    commands='touch 111222'
)

from pyinfra.api.connectors import local
local.run_shell_command(
    name='test local',
    commands='touch 111222'
)