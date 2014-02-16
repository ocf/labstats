#!/usr/bin/env python3
# initializes the database
import db

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
	) ENGINE=InnoDB"""

cursor.execute(query)
