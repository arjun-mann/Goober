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
    Modifies JSON files to store normalized URLs and deletes duplicate files.
    """
    seen_urls = {}  # Maps normalized URL to (original_file_path, original_url)
    files_to_delete = set()
    modified_files = set()  # Track which files need URL updates
    
    # First pass: identify duplicates and files needing URL normalization
    for root, _, files in os.walk(data_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                with open(file_path, "r", errors="ignore") as file:
                    data = json.load(file)
                    original_url = data["url"]
                    normalized_url = normalize_url(original_url)
                    
                    # Check if URL needs normalization
                    if original_url != normalized_url:
                        modified_files.add((file_path, normalized_url))
                    
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
    
    # Second pass: update URLs in files that need normalization
    for file_path, normalized_url in modified_files:
        if file_path not in files_to_delete:  # Don't modify files we're going to delete
            try:
                with open(file_path, "r", errors="ignore") as file:
                    data = json.load(file)
                    data["url"] = normalized_url
                
                with open(file_path, "w") as file:
                    json.dump(data, file)
                print(f"Updated URL in file: {file_path}")
            except Exception as e:
                print(f"Error updating file {file_path}: {str(e)}")
    
    # Third pass: delete duplicate files
    for file_path in files_to_delete:
        try:
            os.remove(file_path)
            print(f"Deleted duplicate file: {file_path}")
        except Exception as e:
            print(f"Error deleting file {file_path}: {str(e)}")
    
    print(f"Pre-processing complete:")
    print(f"- Found {len(seen_urls)} unique URLs")
    print(f"- Updated {len(modified_files)} files with normalized URLs")
    print(f"- Removed {len(files_to_delete)} duplicate files")
    return len(seen_urls), len(files_to_delete)
