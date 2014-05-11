#!/usr/bin/env python3
from labstats import settings, db
from labstats.stats import who
import grp
import operator
import pwd

if __name__ == "__main__":
	staff = grp.getgrnam("approve").gr_mem
	users = [(user, pwd.getpwnam(user).pw_gecos) for  user, _, _ in who.get_current_users() if user in staff]

	for user in sorted(users, key=operator.itemgetter(1)):
		print(user[1])
