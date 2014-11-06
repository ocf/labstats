#!/usr/bin/env python3
import argparse
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

from labstats import settings, db
from labstats.stats import utilization
from datetime import datetime, timedelta, date

graph_dpi=80
#Binomial-shaped weights for moving average
average_weights = tuple(zip(range(-2, 3), \
			(n/16 for n in (1, 4, 6, 4, 1)) ))

def generate_image(profiles, hosts, start, end, dest):
	"""Generates an image representing usage of the lab at minute resolution
	from a set of profiles, each representing a single machine."""

	stats = [0, 0]
	minutes = int((end - start).total_seconds() // 60)
	now = datetime.now()
	if now >= end or now <= start:
		now = None
	minute_now = None if not now else int((now - start).total_seconds() // 60)
	sums = []
	
	for minute in range(minutes):
		instant15 = start + timedelta(minutes=minute, seconds=15)
		instant45 = start + timedelta(minutes=minute, seconds=45)
		in_use = sum(1 if profile.in_use(instant15, now) \
			or profile.in_use(instant45, now) else 0 for profile in profiles)
		sums.append(in_use)
	
	#Do a weighted moving average to smooth out the data
	processed = [0] * len(sums)
	for i in range(len(sums)):
		for delta_i, weight in average_weights:
			m = i if (i+delta_i < 0 or i+delta_i >= len(sums)) else i+delta_i
			#Don't use data that hasn't occurred yet
			if minute_now and i <= minute_now and m >= minute_now:
				processed[i] += weight * sums[i]
			elif minute_now and i > minute_now:
				processed[i] = 0
			else:
				processed[i] += weight * sums[m]
	h = lambda h: h if h <= 12 else h - 12
	p = lambda h: "am" if h <= 11 else "pm"
	hours = ["{}{}".format(h(hour), p(hour)) for hour in range(start.hour, start.hour + minutes // 60)]

	x = list(range(minutes))
	plt.figure(figsize=(10,6))
	plt.grid(True)
	plt.plot(x, processed, color="k", linewidth=1.5)
	#Draw a vertical line, if applicable, showing current time
	if minute_now:
		plt.axvline(minute_now, linewidth=1.5)
	plt.xlim(0, minutes)
	plt.xticks(np.arange(0, minutes, 60), hours)
	plt.xlabel("Time")
	plt.ylim(0, len(hosts))
	plt.ylabel("Computers in Use")

	plt.title("Average Lab Utilization {}".format(start.strftime("%a %b %d, %Y")))

	plt.savefig(dest, dpi=graph_dpi, bbox_inches='tight')

if __name__ == "__main__":
	default_day = date.today() if datetime.now().hour >= 9 else date.today() - timedelta(1)

	parser = argparse.ArgumentParser(description="Generate utilization graphs")
	parser.add_argument("--date", type=str, dest="lookup_date", \
		default=default_day.isoformat(), \
		help="Date to generate graphs for")
	parser.add_argument("--destination", type=str, dest="dest", \
		default=os.path.join(os.getcwd(), "labstats.png"),
		help="Destination file name and path for output graph")
	args = parser.parse_args()

	day = datetime.strptime(args.lookup_date, "%Y-%m-%d")

	start = datetime(day.year, day.month, day.day, 9) # 9am
	end = datetime(day.year, day.month, day.day, 18) # 6pm

	hosts = [h for h in settings.LAB_HOSTNAMES if h not in ("eruption.ocf.berkeley.edu", "blizzard.ocf.berkeley.edu")]
	profiles = [utilization.get_utilization(host, start, end) for host in hosts]
	generate_image(profiles, hosts, start, end, args.dest)
