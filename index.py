#!/usr/bin/python
import nltk
import sys
import getopt
import math
import pickle
from os import listdir
from os.path import isfile, join
from nltk.stem.porter import PorterStemmer
from sets import Set
import string
import sys

def build_index_and_posting(input_directory):
    punc = Set(string.punctuation)
    stemmer = PorterStemmer()
    files = [f for f in listdir(input_directory) if isfile(join(input_directory, f))]
    total_files = len(files)
    df = {}
    file_length = {}
    posting = {}
    for f in files:    
        fp = open(join(input_directory, f), "r")
        tf = {}
        for line in fp:
            for sent_tokens in nltk.sent_tokenize(line):
                for word in nltk.word_tokenize(sent_tokens):
                    stemmed_word = stemmer.stem("".join(ch for ch in word if ch not in punc)).lower()
                    # stemmed_word = stemmer.stem(word).lower()
                    if stemmed_word not in tf:
                        tf[stemmed_word] = 1
                    else:
                        tf[stemmed_word] += 1
        # log10 it
        for t in tf:
            tf[t] = 1 + math.log10(tf[t])
        # Prepare to normalize it
        length_normalized_denominator = math.sqrt(reduce(lambda x, y: x + y**2, tf.values(), 0))
        for t in tf:
            normalized_tf = tf[t] / length_normalized_denominator
            if t not in df:
                df[t] = 1
                posting[t] = {}
            elif f not in posting[t]:
                df[t] += 1
            posting[t][f] = normalized_tf
    idf = {}
    for t in df:
        idf[t] = (df[t], math.log10(float(total_files) / float(df[t])))
    return (idf, posting)

def save_into_disk(idf, posting, output_file_dictionary, output_file_postings):
    accumulate_fp = 0
    fp = open(output_file_postings, "w")
    for post in posting:
        post_string = get_posting_string(posting[post])
        fp.write(post_string)
        idf[post] = (idf[post], accumulate_fp)
        accumulate_fp += len(post_string)
    fp.close()
    pickle.dump(idf, open(output_file_dictionary,"wb"))

def get_posting_string(posting_list):
    # The posting string format is: " doc1_id doc1_tf_normalized doc2_id ......"
    # It does not have to be sorted, but it is good for debugging
    posting_array = sorted(map(lambda key : (int(key), posting_list[key]), posting_list.keys()))
    posting_string = ""
    for tup in posting_array:
        posting_string += " " + str(tup[0]) + " " + str(tup[1])
    return posting_string

def usage():
    print "usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file"

input_directory = output_file_dictionary = output_file_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
    
for o, a in opts:
    if o == '-i': # input directory
        input_directory = a
    elif o == '-d': # dictionary file
        output_file_dictionary = a
    elif o == '-p': # postings file
        output_file_postings = a
    else:
        assert False, "unhandled option"
        
if input_directory == None or output_file_postings == None or output_file_dictionary == None:
    usage()
    sys.exit(2)

(idf, posting) = build_index_and_posting(input_directory)
save_into_disk(idf, posting, output_file_dictionary, output_file_postings)
