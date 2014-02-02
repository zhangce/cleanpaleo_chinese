#! /usr/bin/env pypy

import codecs

from helper.easierlife import *

from multiprocessing import *

INPUT_FOLDER = BASE_FOLDER + "/chinese_input"

titles = {}
usefuldocs = {}
try:
	for l in open(BASE_FOLDER + '/titles_jan20'):
		(id, title) = l.rstrip('\r').rstrip('\n').split('\t')
		if 'overlappingpdfs' in id:
			id = 'overlappingpdfs.' + id.split('/')[-1]
		else:
			id = id.split('/')[-1]
		titles[id] = title

	for l in open(BASE_FOLDER + '/titles_jan18'):
		(id, title) = l.rstrip('\r').rstrip('\n').split('\t')
		titles[id] = title

	for l in open(BASE_FOLDER + '/mapped_pdfs.txt'):
		(refid, id) = l.rstrip().split('\t')
		usefuldocs[id.replace('georefpdfs.', '')] = 1
except:
	donothing = True

def normalize_docids(DOCID):
	TDOCID = DOCID.replace('.task', '')
	TDOCID = TDOCID.replace('NLPRS_jan20_overlap_21.', '')
	TDOCID = TDOCID.replace('NLPRS_jan20_overlap_20.', '')
	return TDOCID

for docid in os.listdir(INPUT_FOLDER):
	if docid.startswith('.'): continue
	
	#TDOCID = normalize_docids(docid)
	#if TDOCID not in usefuldocs:
	#	continue

	title = ""

	try: title = titles[TDOCID]
	except: donothing = True

	print json.dumps({"docid" : docid, "folder" : INPUT_FOLDER+"/"+docid, "title": title})






