from tokenizer import tokenize
#from collections import defaultdict
from nltk.stem import SnowballStemmer
from operator import itemgetter
import json

if __name__ == "__main__":
    docs = 55391
    index_path = "./final_indicies"  # Path to save the index file
    url_mapping_file = "url_mapping.json"  # Path to save the URL mappings
    stemmer = SnowballStemmer("english")
    q = {}
    tags = {}
    mapping = {}
    with open (url_mapping_file, "r") as f:
        data = json.load(f)
        mapping = data
    with open(f'{index_path}/index_0.json', "r") as t:
        data = json.load(t)
        tags = data
    token_freq = []

    query = input('Please enter your query: \n')
    tokens = tokenize(query, stemmer)
    for token in tokens:
        token_freq.append([token,len(data[token])])
    token_freq.sort(key = lambda x: x[1])
    for i in range(0,len(token_freq)):
        if (i == 0):
            for j in range(50):
                try:
                    posting = tags[token_freq[i][0]][j]
                    q[posting[0]] = posting[2]
                except:
                    continue
        else:
            for p in tags[token_freq[i][0]]:
                if p[0] in q:
                    q[p[0]] += p[2]


    res = dict(sorted(q.items(), key=itemgetter(1), reverse=True)[:10]).keys()
    for r in res:
        print(mapping[str(r)][0])
        print(f'{mapping[str(r)][2]}\n\n')
        
def get_search_results(query):
    docs = 55391
    index_path = "./final_indicies"  # Path to save the index file
    url_mapping_file = "url_mapping.json"  # Path to save the URL mappings
    stemmer = SnowballStemmer("english")
    q = {}
    tags = {}
    mapping = {}
    with open (url_mapping_file, "r") as f:
        data = json.load(f)
        mapping = data
    with open(f'{index_path}/index_0.json', "r") as t:
        data = json.load(t)
        tags = data
    token_freq = []
    tokens = tokenize(query, stemmer)
    for token in tokens:
        token_freq.append([token,len(data[token])])
    token_freq.sort(key = lambda x: x[1])
    for i in range(0,len(token_freq)):
        if (i == 0):
            for j in range(50):
                try:
                    posting = tags[token_freq[i][0]][j]
                    q[posting[0]] = posting[2]
                except:
                    continue
        else:
            for p in tags[token_freq[i][0]]:
                if p[0] in q:
                    q[p[0]] += p[2]


    res = dict(sorted(q.items(), key=itemgetter(1), reverse=True)[:10]).keys()
    res_just_urls = []
    for r in res:
        print(mapping[str(r)][0])
        print(f'{mapping[str(r)][2]}\n\n')
        res_just_urls.append(mapping[str(r)][0])
    return res_just_urls





    '''
    with open(index_file, 'r', encoding = 'utf-8') as i:
        data = json.load(i)
        for word in tokens:
            postings = data[word]
            idf = log(docs/len(postings))
            for p in postings:
                tf_idf_scores[p[0]] += float(p[1]*idf) #Need to change?

    res = dict(sorted(tf_idf_scores.items(), key=itemgetter(1), reverse=True)[:10]).keys()


    print (f"Top 10 results for {query}: \n ")
    with open (url_mapping_file, 'r', encoding = 'utf-8') as f:
        data2 = json.load(f)
        i = 1
        for keys in res:
            print (f"{i}: {(data2[str(keys)])[0]}\n")
            i+=1
    '''

