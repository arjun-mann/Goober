import os

def generate_analytics_report(index_file, url_mapping):
    num_documents = len(url_mapping)
    unique_tokens = sum(1 for _ in open(index_file))
    index_size = os.path.getsize(index_file) / 1024 

    with open("analytics_report.txt", "w") as report:
        report.write(f"Number of Indexed Documents: {num_documents}\n")
        report.write(f"Number of Unique Tokens: {unique_tokens}\n")
        report.write(f"Total Index Size: {index_size:.2f} KB\n")
    
    print("Analytics report generated.")
