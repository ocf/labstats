#!/usr/bin/env python3
import argparse
import collections
import matplotlib.pyplot as plt
import numpy as np
import sys

from labstats import settings, db
from labstats.stats import utilization
from datetime import datetime, timedelta, date

def generate_image(usage, user, dest):
	h = lambda h: 12 if h == 0 else (h if h <= 12 else h - 12)
	p = lambda h: "am" if h <= 11 else "pm"
	hours = ["{}{}".format(h(hour), p(hour)) for hour in range(24)]
	sums = [sum(usage[h]) for h in range(24)]

	fig = plt.figure()
	fig.set_size_inches(12, 4)

	plt.bar(range(24), sums, color="b")
	plt.xlim(0, 24)
	plt.xticks(range(24), hours, fontsize=8)
	plt.xlabel("Hour")
	plt.ylabel("# Times Present")
	plt.ylim(0, max(sums) * 1.15)

	plt.title("OCF Lab Timecard for {} (Fall 2014)".format(user))
	plt.savefig(dest, bbox_inches="tight")

def get_usage_count(user):
	hours = collections.defaultdict(lambda: [0 for _ in range(7)])

	cnx = db.get_connection()
	cursor = cnx.cursor()

	time = datetime(2015, 1, 1, 9) # 9am jan 1, 2015
	now = datetime.now()
	step = timedelta(minutes=60)

	def in_lab(time):
		start, end = time, time + step
		query = """
			SELECT COUNT(*) FROM `session`
				WHERE `user` = %s AND (
					`start` BETWEEN %s AND %s OR
					`end` BETWEEN %s AND %s OR
					%s BETWEEN `start` AND `end` OR
					%s BETWEEN `start` AND `end`)"""

		cursor.execute(query, (user, start, end, start, end, start, end))
		return cursor.fetchone()[0] > 0

	while time < now:
		if in_lab(time):
			hours[time.hour][time.weekday()] += 1
		time += step

	return hours

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Generate timecard graphs")
	parser.add_argument("user", type=str, help="User to generate graph for")
	parser.add_argument("dest", type=str, help="File to save graph in")
	args = parser.parse_args()

	usage = get_usage_count(args.user)
	generate_image(usage, args.user, args.dest)
