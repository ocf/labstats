#!/usr/bin/env python3
import argparse
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

from labstats import settings, db
from labstats.stats import utilization
from datetime import datetime, timedelta, date

graph_dpi=75

def generate_image(profiles, hosts, start, end, dest):
	"""Generates an image representing usage of the lab at minute resolution
	from a set of profiles, each representing a single machine."""

	stats = [0, 0]
	minutes = int((end - start).total_seconds() // 60)
	sums = []
	
	for minute in range(minutes):
		instant = start + timedelta(minutes=minute, seconds=30)
		in_use = sum(1 if profile.in_use(instant) else 0 for profile in profiles)

		sums.append(in_use)
	
	#Do a simple weighted moving average to smooth out the data
	processed = [0] * len(sums)
	for i in range(len(sums)):
		for j in range(-2, 3):
			processed[i] += 0 if (i+j < 0 or i+j >= len(sums)) else (3-abs(j))*sums[i+j]
		processed[i] /= 9
	sums = processed
	h = lambda h: h if h <= 12 else h - 12
	p = lambda h: "am" if h <= 11 else "pm"
	hours = ["{}{}".format(h(hour), p(hour)) for hour in range(start.hour, start.hour + minutes // 60)]

	x = list(range(minutes))
	plt.figure(figsize=(10,6))
	plt.grid(True)
	plt.plot(x, sums, color="k", linewidth=1.5)
	plt.xlim(0, minutes)
	plt.xticks(np.arange(0, minutes, 60), hours)
	plt.xlabel("Time")
	plt.ylim(0, len(hosts))
	plt.ylabel("Computers in Use")

	plt.title("Average Lab Utilization {}".format(start.strftime("%a %b %d, %Y")))

	plt.savefig(dest, dpi=graph_dpi, bbox_inches='tight')

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Generate utilization graphs")
	parser.add_argument("--date", type=str, dest="lookup_date", default=date.today().isoformat(),
			help="Date to generate graphs for")
	parser.add_argument("--destination", type=str, dest="dest", default=os.path.join(os.getcwd(), "labstats.png"),
			help="Destination file name and path for output graph")
	args = parser.parse_args()

	day = datetime.strptime(args.lookup_date, "%Y-%m-%d")

	start = datetime(day.year, day.month, day.day, 9) # 9am
	end = datetime(day.year, day.month, day.day, 18) # 6pm

	hosts = [h for h in settings.LAB_HOSTNAMES if h not in ("eruption.ocf.berkeley.edu", "blizzard.ocf.berkeley.edu")]
	profiles = [utilization.get_utilization(host, start, end) for host in hosts]
	generate_image(profiles, hosts, start, end, args.dest)
