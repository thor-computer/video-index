"""
Transcript search module for finding text in video transcripts with timestamps.
"""
import json
from pathlib import Path
from typing import List, Dict
import re


class TranscriptSearcher:
    def __init__(self, transcripts_dir: str = "transcripts"):
        """
        Initialize the transcript searcher.
        
        Args:
            transcripts_dir: Directory containing transcript JSON files
        """
        self.transcripts_dir = Path(transcripts_dir)
        
        if not self.transcripts_dir.exists():
            print(f"[ERROR] Transcripts directory not found: {self.transcripts_dir}")
    
    def load_transcript(self, transcript_path: Path) -> Dict:
        """
        Load a transcript JSON file.
        
        Args:
            transcript_path: Path to transcript file
            
        Returns:
            Transcript data dictionary
        """
        try:
            with open(transcript_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to load {transcript_path}: {str(e)}")
            return None
    
    def format_timestamp(self, seconds: float) -> str:
        """
        Convert seconds to HH:MM:SS format.
        
        Args:
            seconds: Time in seconds
            
        Returns:
            Formatted timestamp string
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    
    def search_transcript(self, transcript_data: Dict, query: str, case_sensitive: bool = False) -> List[Dict]:
        """
        Search for a query string in a transcript.
        
        Args:
            transcript_data: Transcript data dictionary
            query: Search query string
            case_sensitive: Whether to perform case-sensitive search
            
        Returns:
            List of matching segments with timestamps
        """
        if not transcript_data:
            return []
        
        matches = []
        video_id = transcript_data.get('video_id', 'unknown')
        
        # Prepare search pattern
        if case_sensitive:
            pattern = re.compile(re.escape(query))
        else:
            pattern = re.compile(re.escape(query), re.IGNORECASE)
        
        # Search through segments
        for segment in transcript_data.get('segments', []):
            text = segment['text']
            
            if pattern.search(text):
                matches.append({
                    'video_id': video_id,
                    'start': segment['start'],
                    'end': segment['end'],
                    'timestamp': self.format_timestamp(segment['start']),
                    'text': text,
                    'youtube_url': f"https://www.youtube.com/watch?v={video_id}&t={int(segment['start'])}s"
                })
        
        return matches
    
    def search_all(self, query: str, case_sensitive: bool = False, max_results: int = None) -> List[Dict]:
        """
        Search for a query across all transcripts.
        
        Args:
            query: Search query string
            case_sensitive: Whether to perform case-sensitive search
            max_results: Maximum number of results to return (None for all)
            
        Returns:
            List of all matching segments across all videos
        """
        if not query:
            print("[ERROR] No search query provided")
            return []
        
        transcript_files = list(self.transcripts_dir.glob("*.json"))
        
        if not transcript_files:
            print(f"[ERROR] No transcript files found in {self.transcripts_dir}")
            return []
        
        print(f"[INFO] Searching {len(transcript_files)} transcripts for: '{query}'")
        
        all_matches = []
        
        for transcript_path in transcript_files:
            transcript_data = self.load_transcript(transcript_path)
            if transcript_data:
                matches = self.search_transcript(transcript_data, query, case_sensitive)
                all_matches.extend(matches)
        
        # Sort by video_id and timestamp
        all_matches.sort(key=lambda x: (x['video_id'], x['start']))
        
        # Limit results if specified
        if max_results and len(all_matches) > max_results:
            all_matches = all_matches[:max_results]
        
        return all_matches
    
    def display_results(self, matches: List[Dict]):
        """
        Display search results in a formatted way.
        
        Args:
            matches: List of matching segments
        """
        if not matches:
            print("\n[NO RESULTS] No matches found")
            return
        
        print(f"\n[RESULTS] Found {len(matches)} matches:\n")
        print("=" * 80)
        
        current_video = None
        for i, match in enumerate(matches, 1):
            video_id = match['video_id']
            
            # Print video header if it's a new video
            if video_id != current_video:
                if current_video is not None:
                    print("-" * 80)
                print(f"\nVideo: {video_id}")
                current_video = video_id
            
            print(f"\n[{i}] Timestamp: {match['timestamp']}")
            print(f"    Text: {match['text']}")
            print(f"    URL: {match['youtube_url']}")
        
        print("\n" + "=" * 80)


def main():
    """Main function for standalone execution."""
    import sys
    
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
    else:
        query = input("Enter search query: ").strip()
    
    if not query:
        print("[ERROR] No search query provided")
        return
    
    searcher = TranscriptSearcher()
    matches = searcher.search_all(query)
    searcher.display_results(matches)
    
    print(f"\n[COMPLETE] Search finished. Total matches: {len(matches)}")


if __name__ == "__main__":
    main()
