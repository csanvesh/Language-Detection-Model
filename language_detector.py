#!/usr/bin/env python

from optparse import OptionParser
import collections
import os, logging
import string
import re
import math
def create_model(path):
	model = []
	count=0
	f = open(path, "r")
	#print("anvesh")
	unigram= collections.defaultdict(int)
	bigram=collections.defaultdict(lambda : collections.defaultdict(int))
	model.append(unigram)
	model.append(bigram)
	for l in f.readlines():
		#if(count >= 50):
		#	break;
		l=l.lower()
		l=l.replace('\n','')
		l=re.sub('[^a-z|\s]','',l)
		
		for token in l.split(" "):
			token= '$' + token + '$'
			count=count+1
			for i in range(len(token)):
				unigram[token[i]]+=1
				#last_index=len()
				if i< (len(token)-1):
					model[1][token[i]][token[i+1]] += 1
	for key,value in bigram.iteritems():
		for key2,value2 in value.items():
			bigram[key][key2]=math.log10(float((value2 + 1.0)/(unigram[key] + 27.0)))
        ########################################
        ## YOUR CODE GOES HERE
        ########################################     
			
        
        pass
	return model
def calc_prob(file,model):
	fp= open(file,"r")
	probability=0.0
	counter=0
	for line in fp.readlines():
		#if(counter >= 225):
		#	break
		line=line.lower()
		line=line.replace('\n','')
		line=re.sub('[^a-z|\s]','',line)
		for token in line.split(" "):
			token= '$' + token + '$'
			counter = counter + 1
			for i in range(len(token)):
				if i< (len(token)-1):
					if(model[1][token[i]][token[i+1]]==0):
						#print(model[1][token[i]][token[i+1]])
						#model[1][token[i]][token[i+1]]= math.log10(float(1.0/(model[0][token[i]]+27.0))))
						model[1][token[i]][token[i+1]]= math.log10(float(1.0/(model[0][token[i]]+27.0)))
						#model[1][token[i]][token[i+1]]=2
					probability=probability+ model[1][token[i]][token[i+1]]
					#else:
						#model.bigram[token[i]][token[i+1]]= float(model.bigram[token[i]][token[i+1]] / model.unigram[token[i]])
		
	return probability
def predict(file, model_en, model_es):
	prediction = None
	prob_en = calc_prob(file,model_en)
	prob_sp= calc_prob(file,model_es)
	if prob_en > prob_sp:
		prediction = "English"
		#print(file,prob_en,prob_sp)
		#print(prob_en-prob_sp)
	else:
		prediction = "Spanish"
		#print(file,prob_en,prob_sp)
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
