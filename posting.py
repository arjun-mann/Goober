class Posting:
    """
    Represents an individual posting entry in the inverted index.
    
    Attributes:
    - doc_id (int): Document ID where the term appears.
    - frequency (int): Frequency of the term in the document.
    """
    def __init__(self, doc_id, frequency):
        self.doc_id = doc_id
        self.frequency = frequency

    def __repr__(self):
        # Format as (doc_id, frequency) for easy readability
        return f"({self.doc_id},{self.frequency})"

class ListOfPostings:
    """
    Represents a list of postings for a specific term in the inverted index.
    
    Attributes:
    - postings (list): List of Posting objects associated with a term.
    """
    def __init__(self):
        self.postings = []

    def add_posting(self, posting):
        """
        Adds a new posting to the postings list.
        
        Parameters:
        - posting (Posting): Posting object to add.
        """
        self.postings.append(posting)

    def __repr__(self):
        # Join each posting as a space-separated string
        return " ".join(str(posting) for posting in self.postings)
