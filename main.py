import os
from index_builder import build_index, save_index_to_file
from analytics import generate_analytics_report
from nltk.stem import SnowballStemmer

if __name__ == "__main__":
    # Define paths for data and output files
    data_dir = "./data/DEV"  # Directory containing files to index
    index_file = "./indices/dev_index.txt"  # Path to save the index file
    url_mapping_file = "url_mapping.txt"  # Path to save the URL mappings

    # Initialize a stemmer for token processing
    stemmer = SnowballStemmer("english")

    # Build the index and URL mapping from the provided data directory
    print("Building index...")
    index, url_mapping = build_index(data_dir, stemmer)
    save_index_to_file(index, index_file)  # Save the index to a file
    
    # Save URL mappings to a separate file
    with open(url_mapping_file, "w") as file:
        for doc_id, (url, file_name, term_count) in url_mapping.items():
            file.write(f"{doc_id} : {url} {file_name} {term_count}\n")

    # Generate a report with basic analytics on the index
    generate_analytics_report(index_file, url_mapping)
