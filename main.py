import os
from index_builder import build_index, save_index_to_file
from analytics import generate_analytics_report
from nltk.stem import SnowballStemmer

if __name__ == "__main__":
    data_dir = "./data/DEV"
    index_file = "./indices/dev_index.txt"
    url_mapping_file = "url_mapping.txt"

    # Load the stemmer
    stemmer = SnowballStemmer("english")

    # Build index and save
    print("Building index...")
    index, url_mapping = build_index(data_dir, stemmer)
    save_index_to_file(index, index_file)
    
    # Save URL mappings
    with open(url_mapping_file, "w") as file:
        for doc_id, (url, file_name, term_count) in url_mapping.items():
            file.write(f"{doc_id} : {url} {file_name} {term_count}\n")

    # Generate analytics report
    generate_analytics_report(index_file, url_mapping)
