#!/usr/bin/env python3
# TODO: rewrite this
import time

from ocflib.printing.printers import get_lifetime_pages
from ocflib.printing.printers import PRINTERS

dest_dir = '/opt/stats/var/printing/history/'
suffix = '.csv'

for target in PRINTERS:
    now = str(time.time())

    try:
        toner = [get_lifetime_pages(target)]
    except OSError as ex:
        print('Error reading data from {}, continuing to next...'.format(target))
        print('\t{}'.format(ex))
        continue

    with open(dest_dir + target + suffix, 'a+') as file:
        toner.insert(0, now)
        out_str = ','.join(map(str, toner)) + '\n'
        file.write(out_str)
        print('Updated {target} with new value: {out_str}'.format(
            target=target,
            out_str=out_str,
        ))
