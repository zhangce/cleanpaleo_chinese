#! /usr/bin/env pypy

import re
from helper.easierlife import *
from ext.Util import *
from ext.doc.Entity import *


chinese_names = []
for l in open(BASE_FOLDER + '/dicts/intervals_chinese.tsv', 'r'):
	chinese_names.append(l.strip())

dict_intervals = {}
ct = 0
for l in open(BASE_FOLDER + '/dicts/intervals.tsv', 'r'):
	(begin, end, name) = l.rstrip().split('\t')

	chinese_name = chinese_names[ct]
	ct = ct + 1

	if name.startswith('Cryptic'): continue

	dict_intervals[chinese_name] = name + '|' + begin + '|' + end

	"""
	va = name.lower().replace('late ', 'upper ').replace('early ', 'lower')
	if va != name.lower():
		dict_intervals[va] = name + '|' + begin + '|' + end	
	"""

MAXPHRASELEN = 3

for row in get_inputs():
	doc = deserialize(row["documents.document"])

	titlewords = re.sub('\s+', ' ', doc.title.replace(',', ' ').replace('(', ' ').replace(')', ' ')).lower().split(' ')

	log(titlewords)

	history = {}
	for start in range(0, len(titlewords)):
		for end in reversed(range(start + 1, min(len(titlewords)+1, start + 1 + MAXPHRASELEN))):
			phrase = " ".join(titlewords[start:end])

			if start in history: continue
			if phrase.lower() in dict_intervals:
				doc.titleentities.append(Entity("INTERVAL", dict_intervals[phrase.lower()], []))
				for i in range(start, end):
					history[i] = 1

	for sent in doc.sents:
		history = {}
		for start in range(0, len(sent.words)):
			for end in reversed(range(start + 1, min(len(sent.words), start + 1 + MAXPHRASELEN))):
									
				if start in history or end in history: continue
						
				phrase = myjoin(" ", sent.words[start:end], lambda (w) : w.word)
				ner = myjoin(" ", sent.words[start:end], lambda (w) : w.ner)
						
				if phrase.lower() in dict_intervals:
					entity = Entity("INTERVAL", dict_intervals[phrase.lower()], sent.words[start:end])
					doc.push_entity(entity)
					for i in range(start, end):
						history[i]=1

				if '-' in phrase:
					for part in phrase.split('-'):
						if part.lower() in dict_intervals:
							entity = Entity("INTERVAL", dict_intervals[part.lower()], sent.words[start:end])
							doc.push_entity(entity)
							for i in range(start, end):
								history[i]=1

	print json.dumps({'docid':doc.docid, 'entities':serialize(doc.entities), 'type': 'BODY'})
	print json.dumps({'docid':doc.docid, 'entities':serialize(doc.titleentities), 'type': 'TITLE'})






