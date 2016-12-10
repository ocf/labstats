#!/usr/bin/env python3
# TODO: rewrite this
import time

from ocflib.printing.printers import get_toner
from ocflib.printing.printers import PRINTERS

import labstats.db


if __name__ == '__main__':
    dest_dir = '/opt/stats/var/printing/oracle/'
    suffix = '.csv'

    for target in PRINTERS:
        now = str(time.time())

        try:
            toner = get_toner(target)
        except OSError as ex:
            print('Error reading data from {}, continuing to next...'.format(target))
            print('\t{}'.format(ex))
            continue

        with open(dest_dir + target + suffix, 'a+') as file:
            out_str = ','.join(map(str, (now,) + toner)) + '\n'
            file.write(out_str)
            print('Updated {target} with new value: {out_str}'.format(
                target=target,
                out_str=out_str,
            ))

        value, max_ = toner
        c = labstats.db.get_connection()
        cursor = c.cursor()
        cursor.execute(
            (
                'INSERT INTO `printer_toner` (`date`, `printer`, `value`, `max`)'
                '   VALUES (CURRENT_TIMESTAMP(), %s, %s, %s)'
            ),
            (target, value, max_),
        )
        c.commit()
