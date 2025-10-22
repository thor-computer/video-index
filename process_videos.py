"""
Main orchestrator that processes videos one at a time: download → transcribe → repeat.
Skips already downloaded videos and already transcribed videos.
"""
import sys
from pathlib import Path
from downloader import ChannelDownloader
from transcriber import VideoTranscriber


def process_channel(channel_url: str, max_videos: int = None, model_name: str = "base"):
    """
    Process videos from a channel one at a time.
    
    Args:
        channel_url: URL of the YouTube channel/profile
        max_videos: Maximum number of videos to process (None for all)
        model_name: Whisper model to use for transcription
    """
    print("=" * 80)
    print("VIDEO INDEX - INCREMENTAL PROCESSING")
    print("=" * 80)
    print(f"Channel: {channel_url}")
    print(f"Max videos: {max_videos if max_videos else 'All'}")
    print(f"Whisper model: {model_name}")
    print("=" * 80)
    print()
    
    # Initialize downloader and transcriber
    downloader = ChannelDownloader()
    transcriber = VideoTranscriber(model_name=model_name)
    
    # Get list of videos from channel
    print("[STEP 1] Fetching video list from channel...")
    videos = downloader.get_channel_videos(channel_url)
    
    if not videos:
        print("[ERROR] No videos found or failed to fetch channel")
        return
    
    # Limit to max_videos if specified
    if max_videos is not None and max_videos > 0:
        videos = videos[:max_videos]
        print(f"[INFO] Limiting to {max_videos} most recent videos")
    
    print(f"[INFO] Found {len(videos)} videos to process")
    print()
    
    # Process each video one at a time
    processed_count = 0
    skipped_count = 0
    failed_count = 0
    
    for i, video in enumerate(videos, 1):
        video_id = video['id']
        video_url = video['url']
        title = video['title']
        
        print("-" * 80)
        print(f"[{i}/{len(videos)}] Processing: {title}")
        print(f"Video ID: {video_id}")
        print("-" * 80)
        
        # Check if transcript already exists
        transcript_path = transcriber.transcripts_dir / f"{video_id}.json"
        if transcript_path.exists():
            print(f"[SKIP] Transcript already exists for {video_id}")
            skipped_count += 1
            print()
            continue
        
        # Check if video already downloaded
        video_path = downloader.output_dir / f"{video_id}.mp4"
        video_is_placeholder = False
        
        if video_path.exists():
            # Check if it's an empty placeholder
            if video_path.stat().st_size == 0:
                print(f"[INFO] Empty placeholder exists (already processed)")
                video_is_placeholder = True
            else:
                print(f"[INFO] Video already downloaded: {video_id}")
        else:
            # Download the video
            print(f"[DOWNLOAD] Downloading video...")
            success = downloader.download_video(video_url, video_id)
            
            if not success:
                print(f"[ERROR] Failed to download {video_id}, skipping...")
                failed_count += 1
                print()
                continue
            
            print(f"[SUCCESS] Downloaded: {video_id}")
        
        # Skip transcription if placeholder exists (already transcribed)
        if video_is_placeholder:
            print(f"[SKIP] Video already transcribed (placeholder indicates completion)")
            skipped_count += 1
            print()
            continue
        
        # Transcribe the video
        print(f"[TRANSCRIBE] Transcribing video...")
        result = transcriber.transcribe_video(video_path)
        
        if result:
            print(f"[SUCCESS] Transcribed: {video_id}")
            processed_count += 1
            
            # Replace video file with empty placeholder to save space
            try:
                # Get the file size before deletion
                file_size = video_path.stat().st_size
                file_size_mb = file_size / (1024 * 1024)
                
                # Delete the actual video file
                video_path.unlink()
                
                # Create an empty placeholder file
                video_path.touch()
                
                print(f"[CLEANUP] Replaced video with empty placeholder (freed {file_size_mb:.1f} MB)")
            except Exception as e:
                print(f"[WARNING] Could not replace video with placeholder: {str(e)}")
        else:
            print(f"[ERROR] Failed to transcribe {video_id}")
            failed_count += 1
        
        print()
    
    # Summary
    print("=" * 80)
    print("PROCESSING COMPLETE")
    print("=" * 80)
    print(f"Total videos in list: {len(videos)}")
    print(f"Newly processed: {processed_count}")
    print(f"Already processed (skipped): {skipped_count}")
    print(f"Failed: {failed_count}")
    print()
    print(f"Videos directory: {downloader.output_dir.absolute()}")
    print(f"Transcripts directory: {transcriber.transcripts_dir.absolute()}")
    print("=" * 80)


def main():
    """Main function for standalone execution."""
    if len(sys.argv) > 1:
        channel_url = sys.argv[1]
    else:
        channel_url = input("Enter YouTube channel/profile URL: ").strip()
    
    if not channel_url:
        print("[ERROR] No URL provided")
        return
    
    # Check for optional max_videos parameter
    max_videos = None
    if len(sys.argv) > 2:
        try:
            max_videos = int(sys.argv[2])
        except ValueError:
            print(f"[WARNING] Invalid max_videos value '{sys.argv[2]}', processing all videos")
    
    # Check for optional model parameter
    model_name = "base"
    if len(sys.argv) > 3:
        model_name = sys.argv[3]
    
    process_channel(channel_url, max_videos, model_name)


if __name__ == "__main__":
    main()
