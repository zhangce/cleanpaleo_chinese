#! /usr/bin/env pypy

import codecs

from helper.easierlife import *
from ext.doc.Document import *

#fo = open('/tmp/output', 'w')

for row in get_inputs():
	docid = row["docids.docid"]
	title = row["docids.title"]
	folder= row["docids.folder"]

	doc = Document(docid)
	doc.parse_doc(folder)
	doc.title = title

	#fo.write(json.dumps({'docid':docid, 'document':serialize(doc)}) + '\n')
	print json.dumps({'docid':docid, 'document':serialize(doc)}) 
#fo.close()


"""
from multiprocessing import *

INPUT_FOLDER = BASE_FOLDER + "/NLPRS_jan20"

from ext.doc.Document import *

from ext.op.tab_tablefromtext import *

from ext.op.ner_location import *
from ext.op.ner_fossil import *
from ext.op.ner_interval import *
from ext.op.ner_formation import *

from ext.op.rel_samesent import *
from ext.op.rel_title import *
from ext.op.rel_tablecaption import *
from ext.op.rel_jointformation import *
from ext.op.rel_sectionheader import *
from ext.op.rel_listext import *

from ext.op.superviser_occurrences import *


locationext = LocationEntityExtractor()
locationext.loadDict(INPUT_FOLDER)

fossilext = FossilEntityExtractor()
fossilext.loadDict(INPUT_FOLDER)

intervalext = IntervalEntityExtractor()
intervalext.loadDict()

formationext = FormationEntityExtractor()
formationext.loadDict()

samesentrel = SameSentRelationExtractor()
samesentrel.loadDict()

tableexttext = TableExtractorFromText()
tableexttext.loadDict()

tablecaprel = TableCaptionRelationExtractor()
tablecaprel.loadDict()

title_rel = TitleRelationExtractor()

sectionrel = SectionHeaderRealtionExtraction()
sectionrel.loadDict()

listrel = ListRelationExtraction()
listrel.loadDict()

jointrel = JointFormationRelationExtractor()
jointrel.loadDict()

superviser = OccurrencesSuperviser()
superviser.loadDict()


titles = {}
for l in open('/lfs/madmax3/0/czhang/paleopaleo/titles_jan20'):
	(id, title) = l.rstrip('\r').split('\t')
	if 'overlappingpdfs' in id:
		id = 'overlappingpdfs.' + id.split('/')[-1]
	else:
		id = id.split('/')[-1]
	titles[id] = title

for l in open('/lfs/madmax3/0/czhang/paleopaleo/titles_jan18'):
	(id, title) = l.rstrip('\r').split('\t')
	titles[id] = title

usefuldocs = {}
for l in open('/lfs/madmax3/0/czhang/paleopaleo/mapped_pdfs.txt'):
	(refid, id) = l.rstrip().split('\t')
	usefuldocs[id.replace('georefpdfs.', '')] = 1

class Task:
	l = None
	docid = None

	def __init__(self):
		self.l = ""
		self.docid = ""

lock = Lock()

def initializer(*args):
	global lock
	lock = args[0]

def process(task):

	global titles
	DOCID = task.docid

	
	TDOCID = DOCID.replace('.task', '')
	TDOCID = TDOCID.replace('NLPRS_jan20_overlap_21.', '')
	TDOCID = TDOCID.replace('NLPRS_jan20_overlap_20.', '')
	

	if TDOCID not in usefuldocs:
		return

	title = ""

	try:
		title = titles[TDOCID]
		title = title.rstrip('\n')
		#log(title)
	except:
		#log("~~~~" + TDOCID)
		donothing = 1
	#return

	global INPUT_FOLDER
	DOCDIR = INPUT_FOLDER

	import os.path
	if os.path.isfile(BASE_FOLDER + "/tmp_reran/" + DOCID + ".ent"):
	    return

	log(DOCID + '~~~~~~~~')

	#return

	doc = Document(DOCID)
	doc.parse_doc(DOCDIR + "/" + DOCID)

	doc.title = title

	global locationext
	global fossilext
	global intervalext
	global formationext
	global samesentrel
	global tableexttext
	global tablecaprel
	global jointrel
	global sectionrel

	global superviser

	try:

		locationext.extract(doc)

		#print "1"

		fossilext.extract(doc)

		#print "2"

		intervalext.extract(doc)

		#print "3"

		formationext.extract(doc)

		#print "4"

		##### ----

		doc.cleanup_entities()

		#print "5"

		samesentrel.extract(doc)

		#print "6"

		tableexttext.extract(doc)

		#print "7"

		tablecaprel.extract(doc)

		#print "8"
	
		sectionrel.extract(doc)

		#print "9"

		listrel.extract(doc)

		#print "10"

		jointrel.extract(doc)

		#print "11"

		title_rel.extract(doc)

		#print "12"

		oriid = doc.docid
		
		doc.assign_ids()
	
		fo = codecs.open(BASE_FOLDER + "/tmp_reran/" + doc.docid + ".ent", 'w', 'utf-8')
		doc.get_entities_candidates(fo)
		fo.close()

		fo = codecs.open(BASE_FOLDER + "/tmp_reran/" + doc.docid + ".rel", 'w', 'utf-8')
		doc.get_relation_candidates(superviser, fo)
		fo.close()

	except:
		import traceback
		traceback.print_exc()
		traceback.print_stack()
		donothing = True

	#lock.acquire()
	#print json.dumps({"docid":DOCID, "document":serialize(doc)})
	#sys.stdout.flush()
	#lock.release()

	#return doc

log("START PROCESSING!")

def do():
	tasks = []
	#ct = 0
	for docid in os.listdir(INPUT_FOLDER):
		if docid.startswith('.'): continue

		#if 'NLPRS_jan20_overlap_20.jan18pdfs.149.pdf.task' not in docid: continue

		task = Task()
		task.docid = docid
		tasks.append(task)

		#if task.docid != "11173.2": continue
		#print task.docid
		#process(task)
		#print "done"

		#ct = ct + 1
		#if ct > 1:
		#	break

		#tasks.append(task)

	pool = Pool(40, initializer, (lock,))
	pool.map(process, tasks)

#import cProfile
#cProfile.run('do()')

do()

#for doc in pool.map(process, tasks):
#print json.dumps({"docid":doc.docid, "document":serialize(doc)})
"""








