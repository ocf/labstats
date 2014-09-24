#!/usr/bin/env python

import time, subprocess, os

check_toner = "python /opt/stats/labstats/printing/check_toner/check_toner.py"
dest_dir = "/opt/stats/printing/oracle/"
targets = ["deforestation", "logjam"]
suffix = ".csv"
popen = {"shell": True, "stdout": subprocess.PIPE}
realpath = lambda _: os.path.realpath(os.path.expanduser(_))

for target in targets:
  now = str(time.time())
  toner = subprocess.Popen(" ".join([check_toner, target]), **popen).communicate()[0].strip().split("/")
  if len(toner) is not 2:
    # print "Bad output", target
    continue
  try:
    map(int, toner)
  except ValueError:
    continue
  with open(realpath(dest_dir + target + suffix), 'a+') as file:
    try:
      last = list(file)[-1].strip().split(",")[1]
    except: # File doesn't exist yet
      last = False
    if last != toner[0]:
      toner.insert(0, now)
      out_str = ",".join(toner) + "\n"
      file.write(out_str)
      print "Updated", target, out_str
    else:
      # print "No update for", target
      pass
