from nltk.tokenize import RegexpTokenizer

def tokenize(text, stemmer):
    """
    Tokenizes and stems text using a specified stemmer.
    
    Parameters:
    - text (str): The text content to tokenize.
    - stemmer (SnowballStemmer): Stemmer to reduce words to their base form.
    
    Returns:
    - stemmed_tokens (list): List of stemmed tokens extracted from the text.
    """
    tokenizer = RegexpTokenizer(r"\b\w+\b")  # Only match words with alphanumeric characters
    tokens = tokenizer.tokenize(text)  # Tokenize text into individual words
    # Apply stemming and convert tokens to lowercase
    stemmed_tokens = [stemmer.stem(token.lower()) for token in tokens]
    return stemmed_tokens