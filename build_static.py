"""
Build script to create a static site bundle for GitHub Pages.
Combines all transcripts into a single JSON file with video metadata.
"""
import json
from pathlib import Path
import yt_dlp
from datetime import datetime
from tqdm import tqdm

def fetch_video_metadata(video_id):
    """
    Fetch video metadata from YouTube.
    
    Args:
        video_id: YouTube video ID
        
    Returns:
        Dictionary with title, upload_date, and author
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
            
            return {
                'title': info.get('title', 'Unknown Title'),
                'upload_date': formatted_date,
                'upload_date_raw': upload_date_str,
                'author': info.get('uploader', 'Unknown'),
                'channel_id': info.get('channel_id', ''),
                'duration': info.get('duration', 0)
            }
    except Exception as e:
        print(f"[WARNING] Failed to fetch metadata for {video_id}: {e}")
        return {
            'title': f'Video {video_id}',
            'upload_date': 'Unknown',
            'upload_date_raw': '',
            'author': 'Unknown',
            'channel_id': '',
            'duration': 0
        }

def build_static_site():
    """Bundle all transcripts into a single JSON file for static hosting."""
    transcripts_dir = Path("transcripts")
    output_dir = Path(".")  # Output to root directory
    
    # Create output directory (already exists as root)
    output_dir.mkdir(exist_ok=True)
    
    # Load all transcripts
    all_transcripts = []
    transcript_files = list(transcripts_dir.glob("*.json"))
    
    print(f"[INFO] Found {len(transcript_files)} transcript files")
    print()
    
    # Load transcripts with progress bar
    print("[STEP 1/2] Loading transcripts...")
    for transcript_path in tqdm(transcript_files, desc="Loading", unit="file"):
        try:
            with open(transcript_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_transcripts.append(data)
        except Exception as e:
            print(f"\n[ERROR] Failed to load {transcript_path.name}: {e}")
    
    print(f"[OK] Loaded {len(all_transcripts)} transcripts")
    print()
    
    # Fetch metadata for each video
    print("[STEP 2/2] Fetching video metadata from YouTube...")
    for transcript in tqdm(all_transcripts, desc="Fetching metadata", unit="video"):
        video_id = transcript.get('video_id', 'unknown')
        metadata = fetch_video_metadata(video_id)
        transcript['metadata'] = metadata
    
    print(f"[OK] Fetched metadata for {len(all_transcripts)} videos")
    print()
    
    # Write bundled transcripts with metadata
    output_file = output_dir / "transcripts.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_transcripts, f, ensure_ascii=False, indent=2)
    
    print(f"[SUCCESS] Created {output_file}")
    print(f"[INFO] Total transcripts: {len(all_transcripts)}")
    
    # Calculate total size
    size_mb = output_file.stat().st_size / (1024 * 1024)
    print(f"[INFO] Bundle size: {size_mb:.2f} MB")
    
    if size_mb > 10:
        print("[WARNING] Bundle is quite large. Consider splitting or compressing.")
    
    return len(all_transcripts)

if __name__ == "__main__":
    print("=" * 50)
    print("Building Static Site")
    print("=" * 50)
    print()
    
    count = build_static_site()
    
    print()
    print("=" * 50)
    print(f"Build complete! {count} transcripts bundled.")
    print("=" * 50)
