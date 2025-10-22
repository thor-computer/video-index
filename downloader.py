"""
Video downloader module for downloading all videos from a YouTube channel/profile.
"""
import subprocess
import sys
import json
from pathlib import Path
from typing import List, Dict
from tqdm import tqdm


class ChannelDownloader:
    def __init__(self, output_dir: str = "videos"):
        """
        Initialize the channel downloader.
        
        Args:
            output_dir: Directory where videos will be saved
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def get_channel_videos(self, channel_url: str) -> List[Dict]:
        """
        Get list of all videos from a YouTube channel.
        
        Args:
            channel_url: URL of the YouTube channel/profile
            
        Returns:
            List of video metadata dictionaries
        """
        print(f"[INFO] Fetching video list from channel: {channel_url}")
        
        try:
            # Use yt-dlp to get video metadata without downloading
            cmd = [
                sys.executable, "-m", "yt_dlp",
                "--flat-playlist",
                "--dump-json",
                channel_url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Parse JSON output (one JSON object per line)
            videos = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    try:
                        video_data = json.loads(line)
                        videos.append({
                            'id': video_data.get('id'),
                            'title': video_data.get('title'),
                            'url': f"https://www.youtube.com/watch?v={video_data.get('id')}",
                            'duration': video_data.get('duration')
                        })
                    except json.JSONDecodeError:
                        continue
            
            print(f"[INFO] Found {len(videos)} videos in channel")
            return videos
            
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to fetch channel videos: {e.stderr}")
            return []
        except Exception as e:
            print(f"[ERROR] Unexpected error: {str(e)}")
            return []
    
    def download_video(self, video_url: str, video_id: str) -> bool:
        """
        Download audio from a single video.
        
        Args:
            video_url: URL of the video
            video_id: Video ID for filename
            
        Returns:
            True if successful, False otherwise
        """
        output_path = self.output_dir / f"{video_id}.m4a"
        
        # Skip if already downloaded
        if output_path.exists():
            print(f"[SKIP] Audio {video_id} already exists")
            return True
        
        try:
            cmd = [
                sys.executable, "-m", "yt_dlp",
                "-f", "bestaudio[ext=m4a]/bestaudio",
                "-x",  # Extract audio
                "--audio-format", "m4a",
                "-o", str(output_path),
                video_url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and output_path.exists():
                return True
            else:
                print(f"[ERROR] Failed to download audio {video_id}: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Exception downloading audio {video_id}: {str(e)}")
            return False
    
    def download_all(self, channel_url: str, max_videos: int = None) -> List[str]:
        """
        Download all videos from a channel.
        
        Args:
            channel_url: URL of the YouTube channel/profile
            max_videos: Maximum number of videos to download (most recent first). None for all videos.
            
        Returns:
            List of successfully downloaded video IDs
        """
        videos = self.get_channel_videos(channel_url)
        
        if not videos:
            print("[ERROR] No videos found or failed to fetch channel")
            return []
        
        # Limit to max_videos if specified
        if max_videos is not None and max_videos > 0:
            videos = videos[:max_videos]
            print(f"[INFO] Limiting to {max_videos} most recent videos")
        
        downloaded = []
        print(f"\n[INFO] Starting audio download of {len(videos)} videos...")
        
        for video in tqdm(videos, desc="Downloading audio"):
            video_id = video['id']
            video_url = video['url']
            title = video['title']
            
            print(f"\n[DOWNLOAD] {title} ({video_id})")
            
            if self.download_video(video_url, video_id):
                downloaded.append(video_id)
        
        print(f"\n[SUCCESS] Downloaded {len(downloaded)}/{len(videos)} audio files")
        return downloaded


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
            print(f"[INFO] Will download maximum of {max_videos} videos")
        except ValueError:
            print(f"[WARNING] Invalid max_videos value '{sys.argv[2]}', downloading all videos")
    
    downloader = ChannelDownloader()
    downloaded = downloader.download_all(channel_url, max_videos)
    
    print(f"\n[COMPLETE] Audio files saved to: {downloader.output_dir.absolute()}")
    print(f"[COMPLETE] Total audio files downloaded: {len(downloaded)}")


if __name__ == "__main__":
    main()
