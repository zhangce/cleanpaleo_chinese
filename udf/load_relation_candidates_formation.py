#! /usr/bin/env python

from helper.easierlife import *

from ext.op.superviser_occurrences import *

superviser = OccurrencesSuperviser()
superviser.loadDict()

#superviser.extract()

import os
for f in os.listdir(BASE_FOLDER + "/tmp_reran/"):
	if f.endswith('.rel'):
		for l in open(BASE_FOLDER + "/tmp_reran/" + f):
			if '"type": "FORMATION"' in l:
				print l.rstrip().replace('\r', '').replace('\n', '')
