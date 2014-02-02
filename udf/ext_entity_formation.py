#! /usr/bin/env pypy

import re
from helper.easierlife import *
from ext.Util import *
from ext.doc.Entity import *

dict_intervals = {}
stop_words = {}
rocktypes = {"formation":1, "group":1, "member":1, "shale":1, "slate":1, "marble":1, "formations":1, 
		"groups":1, "members":1, "shales":1, "facies":1, "slates":1, "marbles":1, "limestone":1, 'tuff':1, 
		'beds':1, 'bed':1, "face":1, "sandstones":1, "sandstone":1, "siltstone":1, "dolomite":1, 
		"conglomerate":1, "chert":1, "coal":1, "breccia":1, "silt":1, "sand":1, "claystone":1, "clay":1, 
		"arkose":1, "evaporite":1,
		"anhydrite":1, "gypsum":1, "mudstone":1, "marl":1, "argillite":1, "supergroup":1, "greensand":1, 
		"grit":1, "flysch":1, "chalk":1, "oolite":1, "ash":1, "volcanics":1, "molasse":1, "schist":1, 
		"phosphorite":1, "quartzite":1}


goodpos = {"NR VV" : 1, "NR NN" : 1, "NR CD NN" : 1, "NR NN VV NN" : 1, 
		"NN VV NN" : 1, "CD M VV VV" : 1, "NN" : 1, "NN NN" : 1, "NN NN NN NN" : 1, 
		"NN NN NN" : 1}

BADFORMATIONNAME = {"lower":1,"upper":1,"middle":1}

for l in open(BASE_FOLDER + '/dicts/intervals.tsv', 'r'):
	(begin, end, name) = l.rstrip().split('\t')
	dict_intervals[name.lower()] = name + '|' + begin + '|' + end
	va = name.lower().replace('late ', 'upper ').replace('early ', 'lower')
	if va != name.lower():
		dict_intervals[va] = name + '|' + begin + '|' + end
        
for l in open(BASE_FOLDER + '/dicts/english.stop', 'r'):
	stop_words[l.strip().lower()] = 1

MAXPHRASELEN = 5


for row in get_inputs():
	doc = deserialize(row["documents.document"])

	good_names = {}
	for sent in doc.sents:
		history = {}
		for start in range(0, len(sent.words)):
			for end in reversed(range(start + 1, min(len(sent.words), start + 1 + MAXPHRASELEN))):
				if start in history or end in history: continue



				phrase = myjoin(" ", sent.words[start:end], lambda (w) : w.word)
				ner = myjoin(" ", sent.words[start:end], lambda (w) : w.ner)
				pos = myjoin(" ", sent.words[start:end], lambda (w) : w.pos)
				lemma = myjoin(" ", sent.words[start:end], lambda (w) : w.lemma)
				isvalid = True

				if not sent.words[end-1].word == '组' and not sent.words[end-1].word.endswith('组'):
					continue

				if phrase == '组':
					continue

				if pos not in goodpos:
					continue

				#if sent.words[end - 1].lemma.lower() not in rocktypes:
				#	isvalid = False

				if isvalid == False:
					continue

				rocktype = sent.words[end - 1].lemma.lower()

				#if (re.search('^([A-Z][a-zA-Z][a-zA-Z]+\s*|de\s*)*$', phrase) and start>0) or re.search('^([A-Z][a-zA-Z][a-zA-Z][a-zA-Z]+\s*|de\s*)*$', phrase) or re.search('^[A-Z][a-z] ([A-Z][a-zA-Z][a-zA-Z][a-zA-Z]+\s*)*$', phrase):
				if 1 == 1:
					word ='' 
					if ' ' in phrase:
						word = phrase.lower()[:phrase.index(' ')]
					else:
						word = phrase.lower()
					if len(word.strip())<=4 and word.lower() in stop_words:continue

					for lastword in [rocktype,]:
						if phrase.lower().endswith(' ' + lastword) and phrase.lower() != lastword:
							contains = False
							for interval in dict_intervals:
								if interval.lower() in phrase.lower():
									contains = True
							for badname in BADFORMATIONNAME:
								if badname + " " in phrase.lower():
									contains = True
  
							if contains == False:
								good_names[phrase.lower()] = phrase.lower()
								#good_names[phrase[0:phrase.rindex(' ')].lower()] = phrase.lower()
								name = phrase.lower()
															#print phrase[0:phrase.rindex(' ')]
								if phrase.lower().endswith('bed') or phrase.lower().endswith('beds') or phrase.lower().endswith('tuff') or (phrase.lower() + " " + lastword).lower().endswith('limestone'):
									name = name + ' ' + 'formation'
								if not (lemma.lower().endswith(' facies') or lemma.lower().endswith(' face')): 
									entity = Entity("ROCK", lemma.lower(), sent.words[start:end])
									doc.push_entity(entity)

									for i in range(start, end): history[i] = 1

	"""
	for sent in doc.sents:
		history = {}
		for start in range(0, len(sent.words)):
			for end in reversed(range(start + 1, min(len(sent.words), start + 1 + MAXPHRASELEN))):
				if start in history or end in history: continue
				phrase = myjoin(" ", sent.words[start:end], lambda (w) : w.word)
				ner = myjoin(" ", sent.words[start:end], lambda (w) : w.ner)
				lemma = myjoin(" ", sent.words[start:end], lambda (w) : w.lemma)

				lemma = lemma.replace('Sandstones', 'Sandstone')
				isvalid = True

				if sent.words[end - 1].lemma.lower() not in rocktypes:
					isvalid = False

				if isvalid == False:continue

				rocktype = sent.words[end - 1].lemma.lower()

				if re.search('^([A-Z][a-zA-Z][a-zA-Z][a-zA-Z]+\s*|de\s*)*$', phrase):
					exted = False
					for lastword in [rocktype, ]:
						if phrase.lower().endswith(" " + lastword) and phrase.lower() != lastword:
							contains = False
							for interval in dict_intervals:
								if interval.lower() in phrase.lower():
									contains = True
							for badname in BADFORMATIONNAME:
								if badname + " " in phrase.lower():
									contains = True

							if contains == False:
								exted = True
	"""

	for sent in doc.sents:
		for start in range(0, len(sent.words)):
			for end in reversed(range(start + 1, min(len(sent.words), start + 1 + MAXPHRASELEN))):
				phrase = myjoin(" ", sent.words[start:end], lambda (w) : w.word)
				lemma = myjoin(" ", sent.words[start:end], lambda (w) : w.lemma)
				lemma = lemma.replace('Sandstones', 'Sandstone')

				if phrase.lower() in good_names:

					c= True
					if sent.sentid in doc.entities:	
						for ent in doc.entities[sent.sentid]:
							if ent.phrase.strip().lower()==phrase.strip().lower() or phrase.strip().lower() in ent.phrase.strip().lower():
								c = False
					if c:
						
						entity = Entity("ROCK", good_names[phrase.lower()], sent.words[start:end], good_names[phrase.lower()])
						doc.push_entity(entity)


	print json.dumps({'docid':doc.docid, 'entities':serialize(doc.entities), 'type': 'BODY'})
	print json.dumps({'docid':doc.docid, 'entities':serialize(doc.titleentities), 'type': 'TITLE'})


