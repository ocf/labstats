# handles database querying
import mysql.connector
import labstats.settings as settings

def get_connection():
	return mysql.connector.connect(
			user=settings.MYSQL_USER,
			password=settings.MYSQL_PASSWORD,
			host=settings.MYSQL_HOST,
			database=settings.MYSQL_DB,
			autocommit=False,
	)
