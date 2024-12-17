import os
import json
from urllib.parse import urlparse, urlunparse

def normalize_url(url_str):
    """Normalize URL by removing fragments and queries"""
    parsed = urlparse(url_str)
    normalized = parsed._replace(fragment="", query="")
    return urlunparse(normalized)

def preprocess_urls(data_dir):
    """
    Pre-processes the data directory by removing duplicate URLs after defragmenting and dequerying.
    Deletes files that contain URLs which are duplicates after normalization.
    """
    seen_urls = {}  # Maps normalized URL to (original_file_path, original_url)
    files_to_delete = set()
    
    # First pass: identify duplicates
    for root, _, files in os.walk(data_dir):
        print("Currently preprocessing data with directory:", root)
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                with open(file_path, "r", errors="ignore") as file:
                    data = json.load(file)
                    original_url = data["url"]
                    normalized_url = normalize_url(original_url)
                    
                    if normalized_url in seen_urls:
                        # This is a duplicate after normalization
                        files_to_delete.add(file_path)
                    else:
                        seen_urls[normalized_url] = (file_path, original_url)
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON file: {file_path}")
                continue
            except Exception as e:
                print(f"Error processing file {file_path}: {str(e)}")
                continue
    
    # Second pass: delete duplicate files
    for file_path in files_to_delete:
        try:
            os.remove(file_path)
            print(f"Deleted duplicate file: {file_path}")
        except Exception as e:
            print(f"Error deleting file {file_path}: {str(e)}")
    
    print(f"Pre-processing complete. Removed {len(files_to_delete)} duplicate files.")
    return len(seen_urls), len(files_to_delete)