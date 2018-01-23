#!/usr/bin/env python

from optparse import OptionParser
import collections
import os, logging
import string
import re
import math
def create_model(path):
	model = []
	f = open(path, "r")
	#print("anvesh")
	unigram= collections.defaultdict(int)
	bigram=collections.defaultdict(lambda : collections.defaultdict(int))
	trigram=collections.defaultdict(lambda : collections.defaultdict(lambda : collections.defaultdict(int)))
	model.append(unigram)
	model.append(bigram)
	model.append(trigram)
	for l in f.readlines():
		l=l.lower()
		l=l.replace('\n','')
		l=re.sub('[^a-z|\s]','',l)
		
		for token in l.split(" "):
			token= '$' + token + '$'
			for i in range(len(token)):
				unigram[token[i]]+=1
				#last_index=len()
				
				if(i< (len(token)-1)):
					model[1][token[i]][token[i+1]] +=1
				if(i< (len(token)-2)):
					model[2][token[i]][token[i+1]][token[i+2]] += 1
        ########################################
        ## YOUR CODE GOES HERE
        ########################################     
	for key1,value1 in trigram.iteritems():
		for key2,value2 in value1.iteritems():
			for key3,value3 in value2.iteritems():
				tri_count=model[2][key1][key2][key3]
				bi_count=model[1][key1][key2]
				model[2][key1][key2][key3]= math.log10(float((tri_count+1.0)/(bi_count + (27*27))))
        
        pass
	return model
def calc_prob(file,model):
	fp= open(file,"r")
	probability=0.0
	for line in fp.readlines():
		line=line.lower()
		line=line.replace('\n','')
		line=re.sub('[^a-z|\s]','',line)
		for token in line.split(" "):
			token= '$' + token + '$'
			for i in range(len(token)):
				if i< (len(token)-2):
					if(model[2][token[i]][token[i+1]][token[i+2]]==0):
						#print(model[1][token[i]][token[i+1]])
						#model[1][token[i]][token[i+1]]= math.log10(float(1.0/(model[0][token[i]]+27.0))))
						model[2][token[i]][token[i+1]][token[i+2]]= (float(1.0/(model[1][token[i]][token[i+1]]+(27*27))))
						#model[1][token[i]][token[i+1]]=2
					probability=probability+ model[2][token[i]][token[i+1]][token[i+2]]
					#else:
						#model.bigram[token[i]][token[i+1]]= float(model.bigram[token[i]][token[i+1]] / model.unigram[token[i]])
		
	return probability
def predict(file, model_en, model_es):
	prediction = None
	prob_en = calc_prob(file,model_en)
	prob_sp= calc_prob(file,model_es)
	if prob_en > prob_sp:
		prediction = "English"
	else:
		prediction = "Spanish"
	return prediction

def main(en_tr, es_tr, folder_te):
    ## STEP 1: create a model for English with file en_tr
    model_en = create_model(en_tr)

    ## STEP 2: create a model for Spanish with file es_tr
    model_es = create_model(es_tr)

    ## STEP 3: loop through all the files in folder_te and print prediction
    folder = os.path.join(folder_te, "en")
    print "Prediction for English documents in test:"
    for f in os.listdir(folder):
        f_path =  os.path.join(folder, f)
        print "%s\t%s" % (f, predict(f_path, model_en, model_es))
    
    folder = os.path.join(folder_te, "es")
    print "\nPrediction for Spanish documents in test:"
    for f in os.listdir(folder):
        f_path =  os.path.join(folder, f)
        print "%s\t%s" % (f, predict(f_path, model_en, model_es))

if __name__ == "__main__":
    usage = "usage: %prog [options] EN_TR ES_TR FOLDER_TE"
    parser = OptionParser(usage=usage)

    parser.add_option("-d", "--debug", action="store_true",
                      help="turn on debug mode")

    (options, args) = parser.parse_args()
    if len(args) != 3:
		parser.error("Please provide required arguments")

    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.CRITICAL)

    main(args[0], args[1], args[2])
