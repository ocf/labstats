#!/usr/bin/env python3
import argparse
import matplotlib.pyplot as plt
import numpy as np
import sys

from labstats import settings, db
from labstats.stats import utilization
from datetime import datetime, timedelta, date

def generate_image(profiles, hosts, start, end):
	"""Generates an image representing usage of the lab at minute resolution
	from a set of profiles, each representing a single machine."""

	stats = [0, 0]
	minutes = int((end - start).total_seconds() // 60)
	sums = []
	
	for minute in range(minutes):
		instant = start + timedelta(minutes=minute, seconds=30)
		in_use = sum(1 if profile.in_use(instant) else 0 for profile in profiles)

		sums.append(in_use)
	
	h = lambda h: h if h <= 12 else h - 12
	p = lambda h: "am" if h <= 11 else "pm"
	hours = ["{}{}".format(h(hour), p(hour)) for hour in range(start.hour, start.hour + minutes // 60)]

	plt.bar(range(minutes), sums, color="b")
	plt.xlim(0, minutes)
	plt.xticks(np.arange(0, minutes, 60), hours)
	plt.xlabel("Time")
	plt.ylabel("Computers in Use")
	plt.ylim(0, len(hosts))

	plt.title("Lab Utilization {}".format(start.strftime("%a %b %d, %Y")))

	plt.savefig(dest)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Generate utilization graphs")
	parser.add_argument("--date", type=str, default=datetime.now().isoformat(),
			help="Date to generate graphs for")

	yesterday = date.today() - timedelta(1)
	day = date.today() if datetime.now().hour >= 18 else yesterday

	start = datetime(day.year, day.month, day.day, 9) # 9am
	end = datetime(day.year, day.month, day.day, 18) # 6pm

	hosts = [h for h in settings.LAB_HOSTNAMES if h not in ("eruption.ocf.berkeley.edu", "blizzard.ocf.berkeley.edu")]
	profiles = [utilization.get_utilization(host, start, end) for host in hosts]
	generate_image(profiles, hosts, start, end, args.dest)
