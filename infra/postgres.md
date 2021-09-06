https://www.bigbinary.com/blog/configure-postgresql-to-allow-remote-connection

# postgresql.conf
change line

    listen_addresses = 'localhost'

to 

    listen_addresses = '*'

# pg_hba.conf
add two line at end

    host    all             all              0.0.0.0/0                       md5
    host    all             all              ::/0                            md5
