#! /usr/bin/env python

import fileinput
import json
import math

#from helper.ocr import *

from cls.Box import *
from cls.Word import *
from cls.Sentence import *
from cls.Entity import *

import zlib

import sys

import os

import cPickle as pickle

import itertools

import os

import zlib, base64

BASE_FOLDER, throwaway = os.path.split(os.path.realpath(__file__))
BASE_FOLDER = BASE_FOLDER + "/../../"

IS_SMALL_CORPUS = True
SMALL_CORPUS_FOLDER = BASE_FOLDER + "/input"


def assemble_docs(row):
	doc = deserialize(row["documents.t0.document"])
	ent_types = row[".entities_types"]
	ents = row[".entities"]

	for ct in range(0, len(ent_types)):
		ent_type = ent_types[ct]
		ent = deserialize(ents[ct])

		for sentid in ent:
			for entity in ent[sentid]:
				e = Entity(entity.type, entity.entity, 
					doc.sents[entity.sentid].words[entity.words[0].insent_id:entity.words[-1].insent_id+1])
				e.spectype = entity.spectype
				e.author_year = entity.author_year
				e.genus_reso = entity.genus_reso

				if ent_type == 'BODY':
					doc.push_entity(e)
				else:
					doc.titleentities.append(e)


	for sentid in doc.entities:
		toremove = []
		for e1 in doc.entities[sentid]:
			for e2 in doc.entities[sentid]:
				if e1 == e2: continue
				if e1.type == e2.type: continue
				if e1.words == e2.words:
					if e1.type != 'LOCATION' and e1.type != 'INTERVAL' and e1.type != 'ROCK':
						toremove.append(e1)
				if e1.phrase in e2.phrase:
					if e1.type == 'LOCATION' and e2.type == 'ROCK':
						toremove.append(e1)
					if e2.phrase not in e1.phrase and e1.type in ['genus', 'subgenus', 'subgenus!'] and e2.type.startswith('subgen'):
						toremove.append(e1)
					if e1.type == 'LOCATION' and e2.type == 'INTERVAL':
						toremove.append(e2)
	
		newlist = []
		for e in doc.entities[sentid]:
			if e in toremove: continue
			newlist.append(e)
		doc.entities[sentid] = newlist

	doc.assign_ids()
	return doc


def is_fossil_entity(ent):
	if 'class' in ent.type or 'clade' in ent.type or 'subgenus' in ent.type or 'order' in ent.type or 'family' in ent.type or 'genus' in ent.type or 'species' in ent.type:
		return True
	else:
		return False

def myjoin(d, array, mapfunc):
	rs = []
	for a in array:
		if mapfunc(a) not in ['?']: rs.append(mapfunc(a))
	return d.join(rs)

def my_par_join(d, array):
    rss = []
    for a in array:
        if a.altword != None and a.altword != a.word and a.altword != None:
            rss.append([a.word, a.altword])
        else:
            rss.append([a.word])

    for i in itertools.product(*rss):
        rs = []
        for a in i:
            if a not in ['?', '']:
                rs.append(a)
        yield d.join(rs)

def log(str):
	sys.stderr.write(str.__repr__() + "\n")

def asciiCompress(data, level=9):
    """ compress data to printable ascii-code """

    code = zlib.compress(data,level)
    csum = zlib.crc32(code)
    code = base64.encodestring(code)
    return code.replace('\n', ' ')

def asciiDecompress(code):
    """ decompress result of asciiCompress """

    code = base64.decodestring(code.replace(' ', '\n'))
    csum = zlib.crc32(code)
    data = zlib.decompress(code)
    return data

def serialize(obj):
	#return zlib.compress(pickle.dumps(obj))
	return asciiCompress(pickle.dumps(obj))

def deserialize(obj):
	#return pickle.loads(str(unicode(obj)))
	return pickle.loads(asciiDecompress(obj.encode("utf-8")))

def get_inputs():
	for line in fileinput.input():
		line = line.rstrip()
		try:
			yield json.loads(line)
		except:
			log("ERROR  :  " + line)

def dump_input(OUTFILE):
	fo = open(OUTFILE, 'w')
	for line in fileinput.input():
		fo.write(line)
	fo.close()
