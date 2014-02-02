#! /usr/bin/env pypy

import codecs

from helper.easierlife import *
from ext.doc.Document import *


for row in get_inputs():

	doc = assemble_docs(row)

	for sentid in doc.entities:
		for entity in doc.entities[sentid]:
			print json.dumps({'docid':doc.docid, 'type':entity.type, 'eid':entity.eid, 
				'entity':entity.entity, 'author_year':entity.author_year, 'content': ''})
			
	for entity in doc.titleentities:
		print json.dumps({'docid':doc.docid, 'type':entity.type, 'eid':entity.eid, 
				'entity':entity.entity, 'author_year':entity.author_year, 'content': ''})

