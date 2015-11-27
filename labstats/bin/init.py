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

CREATE TABLE `staff` (
        `user` varchar(8) NOT NULL,
        PRIMARY KEY (`user`)
) ENGINE=InnoDB;

CREATE VIEW `session_duration` AS
    SELECT *, timediff(`end`, `start`) AS `duration` FROM `session`;

CREATE VIEW `session_duration_public` AS
    SELECT `id`, `host`, `start`, `end`, `duration` FROM `session_duration`;

CREATE VIEW `users_in_lab` AS
    SELECT `user`, `host`, `start` FROM `session` WHERE `end` IS NULL;

CREATE VIEW `users_in_lab_count_public` AS
    SELECT count(*) as `count` FROM `users_in_lab`;

CREATE VIEW `staff_in_lab_public` AS
    SELECT `user`, `host`, `start` FROM `users_in_lab` WHERE `user` IN (
        SELECT `user` FROM `staff`
    );

GRANT SELECT ON `ocfstats`.`session_duration_public` TO 'anonymous'@'%';
GRANT SELECT ON `ocfstats`.`users_in_lab_count_public` TO 'anonymous'@'%';
GRANT SELECT ON `ocfstats`.`staff_in_lab_public` TO 'anonymous'@'%';
"""

cursor.execute(query)
