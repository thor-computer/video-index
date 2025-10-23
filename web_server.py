"""
Minimal web server for video transcript search interface.
"""
from flask import Flask, render_template, request, jsonify
from searcher import TranscriptSearcher
import os

app = Flask(__name__)
searcher = TranscriptSearcher()

@app.route('/')
def index():
    """Serve the main search interface."""
    return render_template('index.html')

@app.route('/api/search', methods=['GET'])
def search():
    """
    Search endpoint that returns matching transcript segments.
    
    Query parameters:
        q: Search query string
        max_results: Maximum number of results (optional)
    """
    query = request.args.get('q', '').strip()
    max_results = request.args.get('max_results', type=int)
    
    if not query:
        return jsonify({'error': 'No search query provided'}), 400
    
    matches = searcher.search_all(query, max_results=max_results)
    
    return jsonify({
        'query': query,
        'total_results': len(matches),
        'results': matches
    })

if __name__ == '__main__':
    print("=" * 50)
    print("Video Index - Web Interface")
    print("=" * 50)
    print("\nStarting server at http://localhost:5000")
    print("Press Ctrl+C to stop\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
