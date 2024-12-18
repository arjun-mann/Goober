from index_builder import build_index, postprocess_index
from preprocess import preprocess_urls #run this function before building_index if working with default/new web data
from analytics import generate_analytics_report
from nltk.stem import SnowballStemmer

if __name__ == "__main__":
      # Define paths for data and output files
      data_dir = "./DEV"  # Directory containing files to index

      # Initialize a stemmer for token processing
      stemmer = SnowballStemmer("english")

      # Preprocess URLs in the data directory (Only run if working with new URL data)
      #print("Preprocessing URLs...")
      #preprocess_urls(data_dir)

      # Build the index and URL mapping from the provided data directory
      print("Building index...")
      build_index(data_dir, stemmer)

      print("Post processing index...")
      postprocess_index() # postprocess turns partial indexes folder into final indicies folder
                          # final index 0 contains index with only tagged terms
                          # the rest (1-6) are just alphabetical buckets with ONLY frequency, no 
                          # when querying we'll only search indicies 1-6 as a last resort.


      # Generate a report with basic analytics on the index
      print("Generating analytics report...")
      generate_analytics_report("./partial_indexes", "url_mapping.json")
