"""
Minimal web server for video transcript search interface.
"""
from flask import Flask, render_template, request, jsonify
from searcher import TranscriptSearcher
import os
import yt_dlp
from datetime import datetime

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

@app.route('/api/video/<video_id>', methods=['GET'])
def get_video_info(video_id):
    """
    Get video metadata from YouTube.
    
    Args:
        video_id: YouTube video ID
    
    Returns:
        JSON with title and upload_date
    """
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=False)
            
            # Parse upload date (format: YYYYMMDD)
            upload_date_str = info.get('upload_date', '')
            if upload_date_str:
                upload_date = datetime.strptime(upload_date_str, '%Y%m%d')
                formatted_date = upload_date.strftime('%B %d, %Y')
            else:
                formatted_date = 'Unknown'
            
            return jsonify({
                'video_id': video_id,
                'title': info.get('title', 'Unknown Title'),
                'upload_date': formatted_date,
                'upload_date_raw': upload_date_str
            })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'video_id': video_id,
            'title': f'Video {video_id}',
            'upload_date': 'Unknown'
        }), 500

if __name__ == '__main__':
    print("=" * 50)
    print("Video Index - Web Interface")
    print("=" * 50)
    print("\nStarting server at http://localhost:5000")
    print("Press Ctrl+C to stop\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
