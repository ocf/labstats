#!/usr/bin/env python3
from labstats import settings, db
from datetime import datetime, timedelta

def get_current_users():
	cnx = db.get_connection()
	cursor = cnx.cursor()

	query = """
		SELECT `user`, `host`, `start` FROM `session`
			WHERE `end` IS NULL
			ORDER BY `host`"""

	cursor.execute(query)

	return [user for user in cursor]

if __name__ == "__main__":
	print("Current users in the lab:")
	current_users = get_current_users()

	for user, host, start in current_users:
		seconds = (datetime.now() - start).total_seconds()
		hours, seconds = divmod(seconds, 3600)
		minutes = seconds // 60
		print("\t{}: {}, {}h {}m".format(settings.LAB_HOSTNAMES[host], user, int(hours), int(minutes)))

	print("Total: {}".format(len(current_users)))
