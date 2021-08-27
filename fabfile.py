from fabric import Connection, task

c = Connection('sandglass', user='swasher')


@task
def proba(c):
    c.run('echo test from invoke')
#
#     fab_c = Connection('localhost')
#     fab_c.local('echo test from invoke via fabric')
