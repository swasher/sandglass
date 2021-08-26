"""
pyinfra inventory.py deploy.py  -vvv
"""

from pyinfra.operations import apt, server, files
from pyinfra.api import deploy

server.shell(
    name='Run an ad-hoc command',
    chdir='sandglass',
    get_pty=True,
    stdin='yes',
    commands=[
        'git fetch --all',
        'git reset --hard origin/master',
        '/home/swasher/.local/bin/pipenv install',
        '/home/swasher/.local/bin/pipenv run python manage.py collectstatic',
        '/home/swasher/.local/bin/pipenv run python manage.py migrate',

        # 'sudo systemctl restart gunicorn',
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
