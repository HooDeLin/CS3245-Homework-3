This is the README file for A0126576X's submission

== Python Version ==

I'm (We're) using Python Version 2.7 for
this assignment.

== General Notes about this assignment ==

Give an overview of your program, describe the important algorithms/steps 
in your program, and discuss your experiments in general.  A few paragraphs 
are usually sufficient.

Indexing:
To index, we follow a similar strategy as homework 2. We read each file, and we tokenize the contents.
We piggyback on the fact that the number of documents will not change, hence we can calculate normalized tf
as well as idf in the index phase. This is to reduce the time needed on the searching phase.
We will then store the index and the posting
The format of the posting will be as follows:
 doc_id1 tf1_normalized doc_id2 tf2_normalized ...

The format of the index will be as follows:
{
    "term": ((number of docs, idf), pointer to posting)
    ......
}

Note: We need to record the number of docs so that we can know when to stop when iterating the posting list during
searching.

Searching:
To search, we follow a similar strategy as homework 2. We read the query file, and we tokenize the query.
After that, we calculate the tdidf of the query. We omit query normalization since it is not important when comparing ranking (as discussed in lecture 8)
From the query tokens, we extract the documents that might have any relevance to the query.
We calculate the diff from the documents to the query and store it into the heap and show the top 10.

== Files included with this submission ==

List the files in your submission here and provide a short 1 line
description of each file.  Make sure your submission's files are named
and formatted correctly.

index.py: This file indexes the documents and produces a dictionary file and a posting file
search.py: This file reads through the queries and writes the results to a file
dictionary.txt: This file contains the dictionary
posting.txt: This file contains the postings
README.txt: This file.

== Statement of individual work ==

Please initial one of the following statements.

[X] I, A0126576X, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I, A0000000X, did not follow the class rules regarding homework
assignment, because of the following reason:

N/A

I suggest that I should be graded as follows:

N/A

== References ==
