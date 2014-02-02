#! /usr/bin/env python

from helper.easierlife import *

from ext.op.superviser_occurrences import *


for row in get_inputs():


	o = {}
	for key in row:
		kk = key.split('.')[1]
		if kk != 'id':
			o[kk] = row[key]

        o['is_correct'] = None

	print json.dumps(o)


