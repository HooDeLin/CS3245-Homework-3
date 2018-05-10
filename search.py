#!/usr/bin/python
import sys
import getopt
import pickle
from math import log10
import string
from sets import Set
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
import heapq

punc = Set(string.punctuation)
def search(query, index, posting_file, stemmer):
    (query_tokens, query_normalized_vector) = process_query_to_vector(query, index, stemmer)
    doc_vector_list = get_document_vector_list(query_tokens, index, posting_file)
    return score(query_normalized_vector, doc_vector_list)

def process_query_to_vector(query, index, stemmer):
    """
    process_query_to_vector tokenizes the query and calculate the tf-idf of the query
    """
    query_tokens = {}
    stemmed_query = map(lambda x: stemmer.stem("".join(ch for ch in x if ch not in punc)).lower(),word_tokenize(query))
    # stemmed_query = map(lambda x: stemmer.stem(x).lower(),nltk.word_tokenize(query))
    for t in stemmed_query:
        if t not in query_tokens:
            query_tokens[t] = 1
        else:
            query_tokens[t] += 1
    tfidf = {}
    for t in query_tokens:
        if t in index:
            tf = 1 + log10(query_tokens[t])
            idf = index[t][0][1]
            tfidf[t] = tf * idf
    # From lecture 8: We can optimise this since this doesn't concern with documents
    # length_normalized_denominator = math.sqrt(reduce(lambda x, y: x + y**2, tfidf.values(), 0))
    # for t in tfidf:
    #     tfidf[t] = tfidf[t] / length_normalized_denominator
    return (query_tokens.keys(),tfidf)

def get_document_vector_list(query_tokens, index, posting_file):
    """
    get_document_vector_list() returns documents and its token tfs based on the available query tokens
    """
    tf_list = {}
    for t in query_tokens:
        if t in index:
            posting = Posting(posting_file, index[t][1], index[t][0][0])
            doc_tuple = posting.next()
            while doc_tuple != None:
                if str(doc_tuple[0]) not in tf_list:
                    tf_list[str(doc_tuple[0])] = {}
                tf_list[str(doc_tuple[0])][t] = doc_tuple[1]
                doc_tuple = posting.next()
    return tf_list

def score(query_vector, doc_vector_list):
    """
    score() returns the top 10 documents that has the highest ranking
    """
    pq = []
    for doc_id in doc_vector_list:
        doc_vector_score = 0
        for t in doc_vector_list[doc_id]:
            doc_vector_score += doc_vector_list[doc_id][t] * query_vector[t]
        # Sort by decreasing order of the score, but sort ascending of doc_id if the score is the same
        heapq.heappush(pq, (doc_vector_score, -1 * int(doc_id)))
    return map(lambda x: str(-1 * x[1]),heapq.nlargest(10, pq))

class Posting:
    def __init__(self, posting_file, pointer, number_of_postings):
        self.__number_of_postings = number_of_postings
        self.__file = open(posting_file, "r")
        self.__file.seek(pointer)
        self.__index = 0
    
    def next(self):
        """
        next() returns the next tuple of the docs, namely (doc_id, doc_normalized_tf)
        """
        if self.__index >= self.__number_of_postings:
            return None
        spaces_encountered = 0
        value = ""
        # The first one is a space
        self.__file.seek(1,1)
        while spaces_encountered < 2:
            current = self.__file.read(1)
            if current == " ":
                spaces_encountered += 1
            value += current
        # This is to make sure every time it will start with a space
        self.__file.seek(-1,1)
        value_token = value.split(" ")
        self.__index += 1
        return (int(value_token[0]), float(value_token[1]))

def usage():
    print "usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results"

dictionary_file = postings_file = file_of_queries = output_file_of_results = None
	
try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-d':
        dictionary_file  = a
    elif o == '-p':
        postings_file = a
    elif o == '-q':
        file_of_queries = a
    elif o == '-o':
        file_of_output = a
    else:
        assert False, "unhandled option"

if dictionary_file == None or postings_file == None or file_of_queries == None or file_of_output == None :
    usage()
    sys.exit(2)

index = pickle.load(open(dictionary_file, "rb"))
query_fp = open(file_of_queries, "r")
output_fp = open(file_of_output, "w")
stemmer = PorterStemmer()
for line in query_fp:
    result = search(line.strip(), index, postings_file, stemmer)
    output_fp.write(" ".join(result) + "\n")
query_fp.close()
output_fp.close()