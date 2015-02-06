#!/usr/bin/env python

import time, subprocess, os

check_toner = "python /opt/stats/labstats/printing/check_toner/check_pages.py"
dest_dir = "/opt/stats/var/printing/history/"
targets = ["deforestation", "logjam"]
suffix = ".csv"
popen = {"shell": True, "stdout": subprocess.PIPE}
realpath = lambda _: os.path.realpath(os.path.expanduser(_))

for target in targets:
  now = str(time.time())
  pages = subprocess.Popen(" ".join([check_toner, target]), **popen).communicate()[0].strip()
  # if len(pages) is not 1:
    # print "Bad output", target
    #continue
  pages = [pages]

  try:
    map(int, pages)
  except ValueError:
    continue
  with open(realpath(dest_dir + target + suffix), 'a+') as file:
    try:
      last = list(file)[-1].strip().split(",")[1]
    except: # File doesn't exist yet
      last = False
    if last != pages[0]:
      pages.insert(0, now)
      out_str = ",".join(pages) + "\n"
      file.write(out_str)
      print "Updated", target, out_str
    else:
      # print "No update for", target
      pass
