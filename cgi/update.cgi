#!/usr/bin/env python3
import cgi, sys, os, datetime
sys.path.append("/opt/stats/labstats")
import labstats.update

# get host from CN of the SSL client cert
host = os.environ["SSL_CLIENT_S_DN_CN"]

# get state and current user from request data (GET/POST)
form = cgi.FieldStorage()
state = form["state"].value
user = form["user"].value if "user" in form else None

# update the database
labstats.update.update_host(host, user)

# output some debug info
print("Content-Type: text/plain")
print("")
print("Host: {}".format(host))
print("State: {}".format(state))
print("User: {}".format(user))
