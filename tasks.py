from fabric import Connection
c = Connection('sandglass', user='swasher')
c.run('echo test from invoke')
