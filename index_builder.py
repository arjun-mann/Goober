import os
import json
from bs4 import BeautifulSoup
from tokenizer import tokenize
from posting import Posting, ListOfPostings
from collections import defaultdict

def build_index(data_dir, stemmer):
    """
    Builds an inverted index from a set of JSON files containing web page data.
    
    Parameters:
    - data_dir (str): Path to the directory containing JSON files to be indexed.
    - stemmer (SnowballStemmer): Stemmer used to reduce words to their base form.
    
    Returns:
    - index (dict): Dictionary where each key is a token and the value is a ListOfPostings.
    - url_mapping (dict): Maps document IDs to URL information.
    """
    index = defaultdict(ListOfPostings)  # Stores tokens with associated postings
    url_mapping = {}  # Maps document ID to its URL and file metadata
    doc_id = 1  # Incremental document ID

    # Walk through the directory to process each JSON file
    for root, _, files in os.walk(data_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, "r", errors="ignore") as file:
                try:
                    data = json.load(file)  # Load JSON data from the file
                    url = data["url"]  # Extract URL
                    content = data["content"]  # Extract HTML content
                    
                    # Parse HTML content and extract visible text
                    soup = BeautifulSoup(content, "html.parser")
                    text = soup.get_text()
                    
                    # Tokenize and stem words in the text
                    tokens = tokenize(text, stemmer)
                    token_counts = defaultdict(int)

                    # Count the frequency of each token in the document
                    for token in tokens:
                        token_counts[token] += 1
                    
                    # Add each token to the index with a posting entry
                    for token, frequency in token_counts.items():
                        index[token].add_posting(Posting(doc_id, frequency))

                    # Store document metadata in the URL mapping
                    url_mapping[doc_id] = (url, file_name, len(tokens))
                    doc_id += 1  # Increment document ID for the next file
                except json.JSONDecodeError:
                    # Skip files that aren't properly formatted JSON
                    continue
    return index, url_mapping

def save_index_to_file(index, file_path):
    """
    Saves the inverted index to a file.
    
    Parameters:
    - index (dict): The inverted index with tokens as keys and postings lists as values.
    - file_path (str): Path to save the index file.
    
    Writes each token and its associated postings to a line in the file.
    """
    with open(file_path, "w") as file:
        for term, postings in sorted(index.items()):
            file.write(f"{term} : {postings}\n")  # Save each token and postings list

