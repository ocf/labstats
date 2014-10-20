#!/usr/bin/env python3
from labstats import settings, db
from datetime import datetime, timedelta, date
import sys

cols = ('Computer', 'Busy', 'Idle', '%Usage')
col_format = '{:<14}{:>5}{:>7}{:>9}'

def get_utilization(host, start, end):
	"""Return a UtilizationProfile for the given host between datetime
	objects start and end."""

	cnx = db.get_connection()
	cursor = cnx.cursor()

	query = """
		SELECT `start`, `end` FROM `session`
			WHERE `host` = %s AND (
			    `start` BETWEEN %s AND %s OR
				`end` BETWEEN %s AND %s OR
				%s BETWEEN `start` AND `end` OR
				%s BETWEEN `start` AND `end`)
			ORDER BY `start` ASC"""

	cursor.execute(query, (host, start, end, start, end, start, end))

	return UtilizationProfile(start, end, [session for session in cursor])

def generate_image(name, profile, now=None):
	"""Generates an image representing usage of the machine at minute
	resolution."""

	stats = [0, 0]
	minutes = int((profile.end - profile.start).total_seconds() // 60)
	
	for minute in range(minutes):
		instant = profile.start + timedelta(minutes=minute, seconds=30)
		in_use = profile.in_use(instant, now)
		stats[1 if in_use else 0] += 1
	
	print(col_format.format(name, stats[1], stats[0], \
			str(round(stats[1] / sum(stats) * 100, 2)) + "%"))


	#print(col_format.format(name))
	#print("Minutes in use: {}, not in use: {}".format(stats[1], stats[0]))
	#print("% utilization: {:.4}%".format((stats[1] / sum(stats)) * 100))


class UtilizationProfile:
	"""Somewhat naive way to store utilization as a binary (either in use or
	not) over time."""

	def __init__(self, start, end, sessions):
		self.start = start
		self.end = end
		self.sessions = sessions

	def in_use(self, datetime, now=None):
		if now:
			return any(s[0] <= datetime and datetime <= now and \
				(not s[1] or datetime <= s[1]) for s in self.sessions)
		return any(s[0] <= datetime and s[1] and \
			datetime <= s[1] for s in self.sessions)

if __name__ == "__main__":
	yesterday = date.today() - timedelta(1)
	day = date.today()# if datetime.now().hour > 18 else yesterday

	start = datetime(day.year, day.month, day.day, 9) # 9am
	end = datetime(day.year, day.month, day.day, 18) # 6pm

	print("Utilization of lab between {} and {}:".format(start, end))
	print("Busy and idle times are in minutes")
	print()
	print(col_format.format(*cols))
	print("-" * len(col_format.format(*cols)))
	for fullhost, host in settings.LAB_HOSTNAMES.items():
		profile = get_utilization(fullhost, start, end)
		generate_image(host, profile, datetime.now())
