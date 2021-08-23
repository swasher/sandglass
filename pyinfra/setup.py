"""
pyinfra inventory.py setup.py  -vv
"""

from pyinfra.operations import apt, server, files
from pyinfra.api import deploy

server.shell(
    name='Setup dependencies',
    chdir='sandglass',
    commands=[
        'pip install --user pipenv'
    ],
)