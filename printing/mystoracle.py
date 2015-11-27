#!/usr/bin/env python3
import os.path
from datetime import date
from datetime import datetime
from datetime import timedelta

DATA_DIR = '/opt/stats/var/printing/history'
PRINTERS = ('logjam', 'deforestation')


def load_data(printer):
    csv_path = os.path.join(DATA_DIR, printer + '.csv')

    with open(csv_path) as csv:
        def read_line(line):
            parts = line.strip().split(',')
            timestamp, pages = float(parts[0]), int(parts[1])
            return datetime.fromtimestamp(timestamp), pages

        return list(map(read_line, csv))


def pages_in_range(data, start, end):
    pages_start = None

    for time, pages in data:
        if start <= time < end and pages_start is None:
            pages_start = pages
        elif time > end:
            break

    if not pages_start:
        return 0

    return pages - pages_start

if __name__ == '__main__':
    data = {printer: load_data(printer) for printer in PRINTERS}

    one_day = timedelta(days=1)
    time = datetime.combine(date.today(), datetime.min.time()) + one_day

    cols = ('date', 'total') + PRINTERS
    col_format = '{:>13}{:>13}' + '{:>16}' * (len(cols) - 2)
    print(col_format.format(*cols))

    for _ in range(30):
        def num_pages(printer):
            return pages_in_range(data[printer], time - one_day, time)

        pages = tuple(map(num_pages, PRINTERS))
        cols = ((time - one_day).strftime('%a %b %d'), sum(pages)) + pages
        print(col_format.format(*cols))

        time -= one_day
