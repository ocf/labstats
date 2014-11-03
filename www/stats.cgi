#!/usr/bin/env python3
import cgi, sys, os, datetime
sys.path.append("/opt/stats/labstats")
import labstats.update, labstats.db

print("Content-Type: text/html")
print("")

cnx = labstats.db.get_connection()
cursor = cnx.cursor()

query = "SELECT * FROM `session` ORDER BY `start` DESC"
res = cursor.execute(query)

print("<!-- lol this html... -->")
print("<table border=\"1\">")
print("<tr><th>id</th><th>host</th><th>user</th><th>start</th><th>end</th><th>last updated</th></tr>")

fdate = lambda date: date.strftime("%c") if date else "-"
wrappers = ((str,) * 3) + ((fdate,) * 3)

for record in cursor:
	print("<tr>")
	for i in range(0, 6):
		print("<td>" + wrappers[i](record[i]) + "</td>")
	print("</tr>")

print("</table>")
