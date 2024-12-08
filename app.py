from flask import Flask, request, jsonify, send_from_directory
from query import get_search_results

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query', '')
    print(f"Received query: {query}")
    #Pass function to program here that accepts query and returns top K urls
    #ex:
    try:
        urls = get_search_results(query)
    except:
        urls = []
    # Mock a list of 20 URLs based on the query
    # urls = [f"https://example.com/{query}-{i}" for i in range(1, 11)]
    
    return jsonify(urls)

if __name__ == '__main__':
    app.run(debug=True)
