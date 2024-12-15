import os
import json
def generate_analytics_report(index_path, url_mapping):
    """
    Generates an analytics report on the indexing process.
    
    Parameters:
    - index_file (str): Path to the main index file containing tokens and postings.
    - url_mapping (dict): A dictionary that maps document IDs to URL information.

    """
    with open(url_mapping, 'r') as f:
        data = json.load(f)
        num_documents = len(data)
    unique_tokens = 0
    index_size = 0
    for root, _, files in os.walk(index_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            if(file_name == "index_0.json"):
                index_size += os.path.getsize(file_path) / 1024
                continue
            with open(file_path, "r", errors="ignore") as file:
                data1 = json.load(file)
            unique_tokens += len(data1)
            index_size += os.path.getsize(file_path) / 1024  # Size of the index file in KB

    # Write the analytics report to a text file
    with open("analytics_report.txt", "w", encoding='utf-8') as report:
        report.write(f"Number of Indexed Documents: {num_documents}\n")
        report.write(f"Number of Unique Tokens: {unique_tokens}\n")
        report.write(f"Total Index Size: {index_size:.2f} KB\n")
    
    print("New Analytics report generated.")
