#!/usr/bin/env python3
import argparse
from datetime import datetime

from labstats import db


def get_top_users(num, start, end):
    cnx = db.get_connection()
    cursor = cnx.cursor()

    query = """
        SELECT `user`, SUM(TIME_TO_SEC(TIMEDIFF(`end`, `start`))) AS `duration` FROM `session`
            WHERE  (
                `end` IS NOT NULL AND
                (`start` BETWEEN %s AND %s OR `end` BETWEEN %s AND %s))
            GROUP BY `user`
            ORDER BY `duration` DESC
            LIMIT {}""".format(int(num))

    cursor.execute(query, (start, end, start, end))

    return [user for user in cursor]

if __name__ == '__main__':
    num = 10
    now = True
    all_time = False
    start = datetime(datetime.now().year,
                     1 if datetime.now().month < 7 else 7, 1)
    end = datetime.now()

    parser = argparse.ArgumentParser(
        description='Generate list of top lab users')
    parser.add_argument('--start', type=str, dest='start',
                        help='Start of interval to generate stats for')
    parser.add_argument('--end', type=str, dest='end',
                        help='End of interval to generate stats for')
    parser.add_argument('--all-time', action='store_true',
                        dest='all_time', help='Get all-time stats')
    args = parser.parse_args()

    if args.all_time is True:
        start = datetime(2014, 2, 15, 9)  # 9am feb 15, 2014
        all_time = True
    else:
        if args.start is not None:
            start = datetime.strptime(args.start, '%Y-%m-%d')
        if args.end is not None:
            end = datetime.strptime(args.end, '%Y-%m-%d')
            now = False

    if all_time:
        str_range = 'since records began on {}'.format(start)
    else:
        str_range = ('between {} and {}' if not now else 'since {}').format(
            start, end)
    print('Top {} users of the lab {}:'.format(num, str_range))

    for i, (user, seconds) in enumerate(get_top_users(num, start, end)):
        hours, seconds = divmod(seconds, 3600)
        minutes = seconds // 60
        print('\t{}. \t{:<9} {:>4}h {}m'.format(
            i + 1, user, int(hours), int(minutes)))
