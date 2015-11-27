#!/usr/bin/env python3
# Print login record for a user
import sys

import labstats.db
import labstats.update

HOST_SUFFIX = '.ocf.berkeley.edu'

cnx = labstats.db.get_connection()
cursor = cnx.cursor()

if len(sys.argv) != 2:
    print('usage: {} user'.format(sys.argv[0]))
    sys.exit(1)

query = 'SELECT `host`, `start`, `end` FROM `session` WHERE `user` = %s ORDER BY `start` DESC'
res = cursor.execute(query, (sys.argv[1],))

for record in cursor:
    host, start, end = record
    if host.endswith(HOST_SUFFIX):
        host = host[:len(host) - len(HOST_SUFFIX)]
    print('{} from {} to {}'.format(host, start, end))
