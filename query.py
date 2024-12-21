from tokenizer import tokenize
from nltk.stem import SnowballStemmer
from operator import itemgetter
import json
from math import log
import time
from collections import defaultdict


if __name__ == "__main__":
    docs = 43717
    stemmer = SnowballStemmer("english")
    q = {}
    tags = {}
    mapping = {}
    token_freq = []
    tf_idf_scores = defaultdict(float)

    try:
        # First attempt: original paths
        index_path = "final_indicies"
        url_mapping_file = "url_mapping.json"

        with open(url_mapping_file, "r") as f:
            data = json.load(f)
            mapping = data

        with open(f"{index_path}/index_0.json", "r") as t:
            data = json.load(t)
            tags = data
    except FileNotFoundError as e:

        # Fallback: alternative paths
        index_path = "../final_indicies"
        url_mapping_file = "../url_mapping.json"

        try:
            with open(url_mapping_file, "r") as f:
                data = json.load(f)
                mapping = data

            with open(f"{index_path}/index_0.json", "r") as t:
                data = json.load(t)
                tags = data

        except FileNotFoundError as e:
            # If fallback paths also fail
            raise
    

    query = input() #Users query
    start_time = time.perf_counter()
    tokens = tokenize(query, stemmer) #Tokenizes users query
    
    for token in tokens:
        try:
            token_freq.append([token, len(tags[token])])
        except:
            continue
    
    token_freq.sort(key = lambda x: x[1], reverse = True)
    for i in range(0, len(token_freq)): #Looping through queried tokens
        if (i == 0):
            for j in range(0, token_freq[i][1]): #Looping through documents with the current tagged token
                try:
                    #print("What is this tag?: ", tags[token_freq[i][0]][j])
                    posting = tags[token_freq[i][0]][j]
                    
                    # Calculate components separately for clarity
                    tf = 1 + log(posting[1]) if posting[1] > 0 else 0  # term frequency component
                    idf = log(docs/token_freq[i][1])  # inverse document frequency
                    tag_weight = posting[2]  # tag count weight
                    
                    # Combine all components
                    q[posting[0]] = (tf + idf) + tag_weight
                
                    #print(f"Document {posting[0]}:")
                    #print(f"  tf: {posting[1]}, 1 + log(tf): {tf}, idf: {idf}, tag_weight: {tag_weight}")
                    #print(f"  Final score: {q[posting[0]]}")
                except:
                    continue
        else:
            # For subsequent terms in multi-word queries, add their scores to existing documents
            for p in tags[token_freq[i][0]]:
                if p[0] in q:
                    tf = 1 + log(p[1]) if p[1] > 0 else 0
                    idf = log(docs/token_freq[i][1])
                    tag_weight = p[2]
                    
                    # Add the score for this term to the document's existing score
                    q[p[0]] += (tf + idf) + tag_weight
    
    if (len(token_freq) == 0):

        for token in tokens:
            pos = 0
            if token.isnumeric():
                pos = 6
            elif (token < "e"):
                pos = 1
            elif (token < "i"):
                pos = 2
            elif (token < "n"):
                pos = 3
            elif (token < "s"):
                pos = 4
            else:
                pos = 5
            with open (f'final_indicies/index_{pos}.json', "r") as f:
                data = json.load(f)
                try:
                    postings = data[token]
                except:
                    continue
                idf = log(docs/len(postings))
                for p in postings:
                    tf_idf_scores[p[0]] += float(p[1]*idf)
        if (len(tf_idf_scores) == 0):
            print("No Results Found")
        q = tf_idf_scores
        

    res = dict(sorted(q.items(), key=itemgetter(1), reverse=True)[:10]).keys()


    for r in res:
        print(mapping[str(r)][0])
    end_time = time.perf_counter()
    print(f"Time to tokenize query: {end_time - start_time:.6f} seconds")