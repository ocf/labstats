#!/usr/bin/env python3
# TODO: rewrite this
import time

from ocflib.printing.printers import get_lifetime_pages
from ocflib.printing.printers import PRINTERS

import labstats.db


if __name__ == '__main__':
    dest_dir = '/opt/stats/var/printing/history/'
    suffix = '.csv'

    for target in PRINTERS:
        now = str(time.time())

        try:
            lifetime_pages = get_lifetime_pages(target)
        except OSError as ex:
            print('Error reading data from {}, continuing to next...'.format(target))
            print('\t{}'.format(ex))
            continue

        with open(dest_dir + target + suffix, 'a+') as file:
            out_str = ','.join(map(str, (now, lifetime_pages))) + '\n'
            file.write(out_str)
            print('Updated {target} with new value: {out_str}'.format(
                target=target,
                out_str=out_str,
            ))

        c = labstats.db.get_connection()
        cursor = c.cursor()
        cursor.execute(
            (
                'INSERT INTO `printer_pages` (`date`, `printer`, `value`)'
                '   VALUES (CURRENT_TIMESTAMP(), %s, %s)'
            ),
            (target, lifetime_pages),
        )
        c.commit()
