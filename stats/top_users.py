#!/usr/bin/env python3
from labstats import settings, db
from datetime import datetime, timedelta

def get_top_users(num, start, end):
	cnx = db.get_connection()
	cursor = cnx.cursor()

	query = """
		SELECT `user`, SUM(TIMEDIFF(`end`, `start`)) AS `duration` FROM `session`
			WHERE  (
				`end` IS NOT NULL AND
				(`start` BETWEEN %s AND %s OR `end` BETWEEN %s AND %s))
			GROUP BY `user`
			ORDER BY `duration` DESC
			LIMIT {}""".format(int(num))

	cursor.execute(query, (start, end, start, end))

	return [user for user in cursor]

if __name__ == "__main__":
	num = 10
	start = datetime(2014, 2, 15, 9) # 9am feb 15, 2014

	now = True
	end = datetime.now()

	str_range = "between {} and {}" if not now else "since {}".format(start, end)
	print("Top {} users of the lab {}:".format(num, str_range))

	for i, (user, seconds) in enumerate(get_top_users(num, start, end)):
		hours, seconds = divmod(seconds, 3600)
		minutes = seconds // 60
		print("\t{}. {}: {}h {}m".format(i + 1, user, int(hours), int(minutes)))
