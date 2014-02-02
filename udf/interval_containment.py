#! /usr/bin/env python

from helper.easierlife import *

for row in get_inputs():

	#log(row["relations_formationtemporal_global.t0.formation"])
	#log(row["relations_formationtemporal_global.t0.interval"])
	#log(row["relations_formationtemporal_global.t1.interval"])
	#log("~~~~~~~")

	formation = row["relations_formationtemporal_global.t0.formation"]
	interval1 = row["relations_formationtemporal_global.t0.interval"]
	interval2 = row["relations_formationtemporal_global.t1.interval"]

	(name1, large1, small1) = interval1.split('|')
	(name2, large2, small2) = interval2.split('|')

	large1 = float(large1)
	large2 = float(large2)
	small1 = float(small1)
	small2 = float(small2)

	if small2 <= small1 and large2 >= large1:
		print json.dumps({"formation":formation, "child":interval1, "parent":interval2})
