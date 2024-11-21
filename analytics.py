import os
import json
def generate_analytics_report(index_file, url_mapping):
    """
    Generates an analytics report on the indexing process.
    
    Parameters:
    - index_file (str): Path to the main index file containing tokens and postings.
    - url_mapping (dict): A dictionary that maps document IDs to URL information.

    """
    with open(url_mapping, 'r') as f:
        data = json.load(f)
        num_documents = len(data)
    #num_documents = len(url_mapping)  # Count of indexed documents
    
    with open(index_file, 'r', encoding = 'utf-8') as i:
        data1 = json.load(i)
        unique_tokens = len(data1)
    #unique_tokens = sum(1 for _ in open(index_file))  # Count of unique tokens by lines in index file
    index_size = os.path.getsize(index_file) / 1024  # Size of the index file in KB

    # Write the analytics report to a text file
    with open("analytics_report.txt", "w", encoding='utf-8') as report:
        report.write(f"Number of Indexed Documents: {num_documents}\n")
        report.write(f"Number of Unique Tokens: {unique_tokens}\n")
        report.write(f"Total Index Size: {index_size:.2f} KB\n")
    
    print("Analytics report generated.")
