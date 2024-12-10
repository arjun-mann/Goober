from tokenizer import tokenize
from nltk.stem import SnowballStemmer
from operator import itemgetter
import json
from math import log
import time
from collections import defaultdict


if __name__ == "__main__":
    docs = 55391
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
        #print(f"Error: {e}. Trying alternative paths...")

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
            #print(f"Failed to load files from alternative paths: {e}")
            raise  # Re-raise the exception after logging
    

    query = input()
    start_time = time.perf_counter()
    tokens = tokenize(query, stemmer)
    
    for token in tokens:
        try:
            token_freq.append([token,len(tags[token])])
        except:
            continue
    
    token_freq.sort(key = lambda x: x[1])
    for i in range(0,len(token_freq)):
        max_tag = 1
        if (i == 0):
            for j in range(55391):
                try:
                    posting = tags[token_freq[i][0]][j]
                    if j == 0: 
                        max_tag = posting[2]
                    q[posting[0]] = (log(posting[2]) + log(docs/token_freq[i][1])) *posting[2]/max_tag
                except:
                    continue
        else:
            max_tag = tags[token_freq[i][0]][0][2]
            for p in tags[token_freq[i][0]]:
                if p[0] in q:
                    q[p[0]] += (log(p[2]) + log(docs/token_freq[i][1]) )* p[2]/max_tag
    
    #print(q)
    
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
                    postings s= data[token]
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
        #print(f'{mapping[str(r)][2]}\n\n')
    end_time = time.perf_counter()
    print(f"Time to tokenize query: {end_time - start_time:.6f} seconds")



