import os
import json
from bs4 import BeautifulSoup
from tokenizer import tokenize
from posting import Posting, ListOfPostings
from collections import defaultdict

def build_index(data_dir, stemmer):
    index = defaultdict(ListOfPostings)
    url_mapping = {}
    doc_id = 1

    for root, _, files in os.walk(data_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, "r", errors="ignore") as file:
                try:
                    data = json.load(file)
                    url = data["url"]
                    content = data["content"]
                    
                    soup = BeautifulSoup(content, "html.parser")
                    text = soup.get_text()
                    tokens = tokenize(text, stemmer)

                    token_counts = defaultdict(int)
                    for token in tokens:
                        token_counts[token] += 1
                    
                    for token, frequency in token_counts.items():
                        index[token].add_posting(Posting(doc_id, frequency))

                    url_mapping[doc_id] = (url, file_name, len(tokens))
                    doc_id += 1
                except json.JSONDecodeError:
                    continue
    return index, url_mapping

def save_index_to_file(index, file_path):
    with open(file_path, "w") as file:
        for term, postings in sorted(index.items()):
            file.write(f"{term} : {postings}\n")
