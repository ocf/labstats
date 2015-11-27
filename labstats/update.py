# handles storing updates in the database
from ocflib.account.utils import list_staff

import labstats.db as db
import labstats.settings as settings


def update_host(host, user):
    if not user:
        close_session(host)
    else:
        new_session(host, user)


def session_exists(host, user):
    """Returns whether an open session already exists for a given host and user
    pair."""

    cnx = db.get_connection()
    cursor = cnx.cursor()

    query = """
        SELECT count(*) FROM `session`
            WHERE `host` = %s AND `user` = %s AND `end` IS NULL"""

    cursor.execute(query, (host, user))

    return cursor.fetchone()[0] > 0


def update_session(host, user):
    cnx = db.get_connection()
    cursor = cnx.cursor()

    query = """
        UPDATE `session` SET `last_update` = NOW()
            WHERE `host` = %s AND `user` = %s AND `end` IS NULL"""

    cursor.execute(query, (host, user))
    cnx.commit()


def new_session(host, user):
    if session_exists(host, user):
        update_session(host, user)
        return

    close_session(host)  # close old sessions
    cnx = db.get_connection()
    cursor = cnx.cursor()

    query = """
        INSERT INTO `session` (`host`, `user`, `start`, `last_update`)
            VALUES (%s, %s, NOW(), NOW())"""

    cursor.execute(query, (host, user))
    cnx.commit()


def close_session(host):
    cnx = db.get_connection()
    cursor = cnx.cursor()

    query = """
        UPDATE `session` SET `end` = NOW(), `last_update` = NOW()
            WHERE `host` = %s AND `end` IS NULL"""

    cursor.execute(query, (host,))
    cnx.commit()


def close_old_sessions():
    """Closes sessions which we haven't received an update for in a while.
    Usually this means the host is off, so we want to end the session."""

    cnx = db.get_connection()
    cursor = cnx.cursor()

    query = """
        UPDATE `session` SET `end` = NOW(), `last_update` = NOW()
            WHERE `end` IS NULL AND
                `last_update` < ADDDATE(NOW(), INTERVAL -{} MINUTE)""".format(int(settings.HOST_TIMEOUT))

    cursor.execute(query)
    cnx.commit()


def update_staff():
    staff = list_staff()

    cnx = db.get_connection()
    cursor = cnx.cursor()
    cursor.execute('DELETE FROM `staff`')
    for user in staff:
        cursor.execute('INSERT INTO `staff` (`user`) VALUES (%s)', (user,))

    cnx.commit()
