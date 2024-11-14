class Posting:
    def __init__(self, doc_id, frequency):
        self.doc_id = doc_id
        self.frequency = frequency

    def __repr__(self):
        return f"({self.doc_id},{self.frequency})"

class ListOfPostings:
    def __init__(self):
        self.postings = []

    def add_posting(self, posting):
        self.postings.append(posting)

    def __repr__(self):
        return " ".join(str(posting) for posting in self.postings)
