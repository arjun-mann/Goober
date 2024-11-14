from nltk.tokenize import RegexpTokenizer

def tokenize(text, stemmer):
    tokenizer = RegexpTokenizer(r"\b\w+\b")
    tokens = tokenizer.tokenize(text)
    stemmed_tokens = [stemmer.stem(token.lower()) for token in tokens]
    return stemmed_tokens
