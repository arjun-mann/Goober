# Goober
a Web search engine from the ground up that is capable of handling tens of thousands of Web pages, under harsh operational constraints and having a query response time under 300ms 

## Index Analytics
Number of Indexed Documents: 43716
Number of Unique Tokens: 2054645
Total Index Size: 172686.30 KB



# How It Works
1. User Input: The user types a query in the search bar on the frontend.
2. API Call: The frontend sends the query to the /api/query endpoint (query.py).
3. Query Processing:
4. The backend reads the dataset (final_indicies).
5. Tokenizes and stems the query (tokenizer.py).
6. Scores and ranks documents.
7. Response: The backend returns the top 10 results, which are displayed on the frontend.

# Method 1: [goober-tau.vercel.app](https://goober-tau.vercel.app)
Query on our deployed search engine!

# Method 2: Local Installation
```bash
git clone https://github.com/arjun-mann/Goober.git
cd goober-frontend
npm install
npm run dev
```
Open your local host and query away!

# Method 3: Terminal Access
```bash
# Make sure you are in the root directory
git clone https://github.com/arjun-mann/Goober.git
pip install nltk
python query.py
```
