#!/usr/bin/env python3
from labstats import settings, db
from datetime import datetime, timedelta
import sys

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

def generate_image(name, profile):
	"""Generates an image representing usage of the machine at minute
	resolution."""

	stats = [0, 0]
	minutes = int((profile.end - profile.start).total_seconds() // 60)
	
	for minute in range(minutes):
		instant = profile.start + timedelta(minutes=minute, seconds=30)
		in_use = profile.in_use(instant)

		stats[1 if in_use else 0] += 1
	
	print("{}:".format(name))
	print("Minutes in use: {}, not in use: {}".format(stats[1], stats[0]))
	print("% utilization: {:.4}%".format((stats[1] / sum(stats)) * 100))

class UtilizationProfile:
	"""Somewhat naive way to store utilization as a binary (either in use or
	not) over time."""

	def __init__(self, start, end, sessions):
		self.start = start
		self.end = end
		self.sessions = sessions

	def in_use(self, datetime):
		return any(s[0] <= datetime <= s[1] for s in self.sessions)

if __name__ == "__main__":
	start = datetime(2014, 2, 19, 9) # 9am feb 19, 2014
	end = datetime(2014, 2, 19, 18) # 6pm
	print("Utilization of lab between {} and {}:".format(start, end))

	for fullhost, host in settings.LAB_HOSTNAMES.items():
		print()
		profile = get_utilization(fullhost, start, end)
		generate_image(host, profile)

#import code
#code.interact(local=locals())
