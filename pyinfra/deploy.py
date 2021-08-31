"""
pyinfra inventory.py deploy.py  -vvv
"""

from pyinfra.operations import apt, server, files
from pyinfra.api import deploy
from decouple import config

SUDO_PASS = config('SUDO_PASS')

server.shell(
    name='Git fetch and reset',
    chdir='sandglass',
    commands=[
        'git fetch --all',
        'git reset --hard origin/master',
    ],
)

server.shell(
    name='Run django related commands',
    chdir='sandglass',
    # get_pty=True,
    stdin='yes',
    commands=[
        '/home/swasher/.local/bin/pipenv install',
        '/home/swasher/.local/bin/pipenv run python manage.py collectstatic',
        '/home/swasher/.local/bin/pipenv run python manage.py migrate',
    ],
)

server.shell(
    name='Restart gunicorn',
    # get_pty=True,
    # sudo=True,
    # use_sudo_password=True,
    stdin=SUDO_PASS,
    commands=[
        'sudo systemctl restart gunicorn',
        # 'sudo systemctl restart nginx'
    ],
)

# files.file(
#     name='Create pyinfra log file',
#     path='/home/swasher/111.txt',
#     user='swasher',
#     group='swasher',
#     mode='644',
#     sudo=True,
# )


# @deploy('Install test')
# def test1(state=None, host=None):
#     files.file(
#         name='Create pyinfra log file',
#         path='/home/swasher/111.txt',
#         user='swasher',
#         group='swasher',
#         mode='644',
#         sudo=True,
#     )
