#!/usr/bin/env python3
# initializes the database
import labstats.db as db

cnx = db.get_connection()
cursor = cnx.cursor()

print("Creating session table...")

query = """
CREATE TABLE `session` (
        `id` int NOT NULL AUTO_INCREMENT,
        `host` varchar(255) NOT NULL,
        `user` varchar(8) NOT NULL,
        `start` datetime NOT NULL,
        `end` datetime DEFAULT NULL,
        `last_update` datetime,
        PRIMARY KEY (`id`)
) ENGINE=InnoDB;

CREATE VIEW `session_duration` AS
    SELECT *, timediff(`end`, `start`) AS `duration` FROM `session`;

CREATE VIEW `session_duration_public` AS
    SELECT `id`, `host`, `start`, `end`, `duration` FROM `session_duration`;

GRANT SELECT ON `ocfstats`.`session_duration_public` TO 'anonymous'@'%';
"""

cursor.execute(query)
