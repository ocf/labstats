# handles database querying
import mysql.connector
import labstats.settings as settings

def get_connection():
	cnx = mysql.connector.connect(
			user=settings.MYSQL_USER,
			password=settings.MYSQL_PASSWORD,
			host=settings.MYSQL_HOST,
			database=settings.MYSQL_DB)
	
	return cnx
