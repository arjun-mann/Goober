import os
import json
from bs4 import BeautifulSoup
from tokenizer import tokenize
from collections import defaultdict
import re

def build_index(data_dir, stemmer):
    """
    Builds an inverted index from a set of JSON files containing web page data.
    
    Parameters:
    - data_dir (str): Path to the directory containing JSON files to be indexed.
    - stemmer (SnowballStemmer): Stemmer used to reduce words to their base form.
    
    Returns:
    - folder with index (dict)s with 10,000 sites' postings at a time : Dictionary where each key is a token and the value is a ListOfPostings.
    - url_mapping (dict): Maps document IDs to URL information.
    """
    index = defaultdict(list)  # Stores tokens with associated postings
    tag_index = defaultdict(list) #Stores only tokens with important tagged postings
    url_mapping = {}  # Maps document ID to its URL and file metadata
    doc_id = 1  # Incremental document ID
    batch_size = 10000
    # Walk through the directory to process each JSON file
    for root, _, files in os.walk(data_dir):
        print("Currently building index with directory:", root)
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, "r", errors="ignore") as file:
                try:
                    data = json.load(file)  # Load JSON data from the file
                    url = data["url"]  # Extract URL
                    content = data["content"]  # Extract HTML content

                    # Parse HTML content and extract visible text
                    if not content.strip():
                        print("Empty document content detected, skipping.")
                        continue
                    
                    content = re.sub(r'[\x00-\x1F\x7F]', '', content)
                    try:
                        soup = BeautifulSoup(content, 'html.parser')
                    except Exception as e:
                        print("Error parsing HTML with BeautifulSoup:", e)
                        continue
                    l = ["title", "header", "h1", "h2", "b", "strong", True]
                    token_dict = {}
                    try:
                        file_title = soup.find(True).get_text(strip=True) # title/header of url to use when returning search results. goest to url_mapping
                    except:
                        file_title = ""
                    for tag in l:
                        for element in soup.find_all(tag):
                            text = element.get_text(strip=True)
                            if text:
                                tokens = tokenize(text,stemmer)
                                for token in tokens:
                                    if token in token_dict:
                                        token_dict[token][0] +=1 #frequency
                                        if(isinstance(tag, str)):
                                            if (tag == "title" or "header"):
                                                token_dict[token][1] +=20 #scoring important tags, 
                                                #title/header being most important, h2 2nd, and bold/strong 3rd
                                            elif (tag == "h1" or "h2"):
                                                token_dict[token][1] += 10
                                            else:
                                                token_dict[token][1] += 1
                                    else:
                                        if(isinstance(tag, str)):
                                            if (tag == "title" or "header"):
                                                token_dict[token] = [1,20] #scoring important tags, 
                                                #title/header being most important, h2 2nd, and bold/strong 3rd
                                            elif (tag == "h1" or "h2"):
                                                token_dict[token] = [1,10]
                                            else:
                                                token_dict[token] = [1,1]
                                           
                                        else:
                                            token_dict[token] = [1,0]
                            element.decompose() 
                        
                    for key in token_dict: # terms with nonzero tag scores will go to both tagged index AND normal index.
                        if (token_dict[key][1]) != 0:
                            tag_index[key].append([doc_id, token_dict[key][0],token_dict[key][1]])
                        
                        index[key].append([doc_id, token_dict[key][0]])
                    if doc_id % 1000 == 0: # progress checking
                        print(f"\nProcessed {doc_id} pages!\n")
                    if doc_id % batch_size == 0:
                        write_partial_index(index, doc_id)
                        index.clear()

                    # Store document metadata in the URL mapping
                    url_mapping[doc_id] = (url, file_name, file_title[0:100])
                    doc_id += 1  # Increment document ID for the next file
                except json.JSONDecodeError:
                    # Skip files that aren't properly formatted JSON
                    continue
    #return index, url_mapping

    # Write any remaining index and URL mappings
    write_tag_index(tag_index)
    write_partial_index(index, doc_id)  # Write any remaining index data
    write_url_mapping(url_mapping)


def postprocess_index():
     index_dir = './partial_indexes'
     for i in range (7):
         with open(f'./final_indicies/index_{i}.json', "w") as f:
            data = {}
            json.dump(data,f)
     
     for root, _, files in os.walk(index_dir):
        print("Currently postprocessing index with directory:", root)
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if file_name == "index_part_0.json":
                ### index_part_0 is the tag only json
                with open(file_path, "r", errors="ignore") as file:
                    try:
                        data = json.load(file)
                        sorted_data = {}
                        for keys in data:
                            #sort based on tag score
                            data[keys].sort(key=lambda x: (x[2],x[1]),reverse = True)
                            sorted_data[keys] = data[keys]

                        with open('./final_indicies/index_0.json', "w") as f:
                            json.dump(data,f)
                    except json.JSONDecodeError:
                        continue
            else:
                with open(file_path, "r", errors="ignore") as file:
                    #only opening one file at a time, limited memory
                    try:
                        alpha = [{} for _ in range(6)]
                        data = json.load(file)  # Load dict "data" from json
                        for key in data:
                            #alphabetic buckets
                            if key.isnumeric():
                                data[key].sort(key=lambda x: x[1], reverse=True)
                                alpha[5][key] = data[key]
                            elif (key < "e"):
                                data[key].sort(key=lambda x: x[1], reverse=True)
                                alpha[0][key] = data[key]
                            elif (key < "i"):
                                data[key].sort(key=lambda x: x[1], reverse=True)
                                alpha[1][key] = data[key]
                            elif (key < "n"):
                                data[key].sort(key=lambda x: x[1], reverse=True)
                                alpha[2][key] = data[key]
                            elif (key < "s"):
                                data[key].sort(key=lambda x: x[1], reverse=True)
                                alpha[3][key] = data[key]
                            else:
                                data[key].sort(key=lambda x: x[1], reverse=True)
                                alpha[4][key] = data[key]

                        for i in range (1,7):
                            with open(f'./final_indicies/index_{i}.json', "r+") as f:
                                initial = json.load(f)
                                new = merge_dicts(alpha[i-1], initial) 
                                f.seek(0)
                                json.dump(new,f)
                                f.truncate()
                        print (f'done with {file_name}')
                    except json.JSONDecodeError:
                        continue

def merge_dicts(y,x) -> dict: #merges two dicts, combining postings lists in the case of like keys.
    de = defaultdict(list, x)
    for i, j in y.items():
        if(de[i]):
            de[i].extend(j)
        else:
            de[i] = j
        de[i].sort(key=lambda x: x[1], reverse=True)
        
    return de
def write_tag_index(index):
    print(f"Writing tag only index\n")
    partial_index_filename = f"partial_indexes/index_part_0.json"
    with open(partial_index_filename, "w") as outfile:
        json.dump(index, outfile)

def write_partial_index(index, doc_id):
    # Writes the partial index to disk
    print(f"Writing partial_index {doc_id - 10000} - {doc_id}")
    partial_index_filename = f"partial_indexes/index_part_{doc_id}.json"
    with open(partial_index_filename, "w") as outfile:
        json.dump(index, outfile)

def write_url_mapping(url_mapping):
    with open("url_mapping.json", "w", encoding='utf-8') as file:
            json.dump(url_mapping, file)
