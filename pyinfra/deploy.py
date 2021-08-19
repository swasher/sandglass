from pyinfra.operations import apt, server

host = ['sandglass']

server.shell(
    name='Run an ad-hoc command',  # optional name for the operation
    commands=['echo "hello world"'],
)

@deploy('Fetch')
def git_fetch(state=None, host=None):
    apt.packages(
        name='Install MariaDB apt package',
        packages=['mariadb-server'],
        state=state,  # note passing of state & host here
        host=host,
    )