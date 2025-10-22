"""
Video transcription module using OpenAI Whisper.
"""
import whisper
import json
from pathlib import Path
from typing import List, Dict
from tqdm import tqdm


class VideoTranscriber:
    def __init__(self, model_name: str = "base", videos_dir: str = "videos", transcripts_dir: str = "transcripts"):
        """
        Initialize the video transcriber.
        
        Args:
            model_name: Whisper model to use (tiny, base, small, medium, large)
            videos_dir: Directory containing video files
            transcripts_dir: Directory where transcripts will be saved
        """
        print(f"[INFO] Loading Whisper model: {model_name}")
        self.model = whisper.load_model(model_name)
        self.videos_dir = Path(videos_dir)
        self.transcripts_dir = Path(transcripts_dir)
        self.transcripts_dir.mkdir(exist_ok=True)
        print(f"[INFO] Whisper model loaded successfully")
    
    def transcribe_video(self, video_path: Path) -> Dict:
        """
        Transcribe a single video file.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            Dictionary containing transcript data with timestamps
        """
        video_id = video_path.stem
        transcript_path = self.transcripts_dir / f"{video_id}.json"
        
        # Skip if already transcribed
        if transcript_path.exists():
            print(f"[SKIP] Transcript for {video_id} already exists")
            with open(transcript_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        print(f"[TRANSCRIBE] Processing {video_id}...")
        
        try:
            # Transcribe with word-level timestamps
            result = self.model.transcribe(
                str(video_path),
                word_timestamps=True,
                verbose=False
            )
            
            # Extract segments with timestamps
            segments = []
            for segment in result['segments']:
                segments.append({
                    'start': segment['start'],
                    'end': segment['end'],
                    'text': segment['text'].strip()
                })
            
            transcript_data = {
                'video_id': video_id,
                'video_path': str(video_path),
                'language': result.get('language', 'unknown'),
                'segments': segments,
                'full_text': result['text']
            }
            
            # Save transcript
            with open(transcript_path, 'w', encoding='utf-8') as f:
                json.dump(transcript_data, f, indent=2, ensure_ascii=False)
            
            print(f"[SUCCESS] Transcript saved: {transcript_path}")
            return transcript_data
            
        except Exception as e:
            print(f"[ERROR] Failed to transcribe {video_id}: {str(e)}")
            return None
    
    def transcribe_all(self) -> List[str]:
        """
        Transcribe all audio files in the videos directory.
        
        Returns:
            List of successfully transcribed video IDs
        """
        video_files = list(self.videos_dir.glob("*.m4a"))
        video_files.extend(self.videos_dir.glob("*.mp3"))
        video_files.extend(self.videos_dir.glob("*.mp4"))
        video_files.extend(self.videos_dir.glob("*.webm"))
        video_files.extend(self.videos_dir.glob("*.mkv"))
        
        if not video_files:
            print(f"[ERROR] No audio/video files found in {self.videos_dir}")
            return []
        
        print(f"\n[INFO] Found {len(video_files)} audio files to transcribe")
        
        transcribed = []
        for video_path in tqdm(video_files, desc="Transcribing videos"):
            result = self.transcribe_video(video_path)
            if result:
                transcribed.append(video_path.stem)
        
        print(f"\n[SUCCESS] Transcribed {len(transcribed)}/{len(video_files)} videos")
        return transcribed


def main():
    """Main function for standalone execution."""
    import sys
    
    model_name = "base"
    if len(sys.argv) > 1:
        model_name = sys.argv[1]
    
    print(f"[INFO] Using Whisper model: {model_name}")
    print("[INFO] Available models: tiny, base, small, medium, large")
    print("[INFO] Larger models are more accurate but slower")
    
    transcriber = VideoTranscriber(model_name=model_name)
    transcribed = transcriber.transcribe_all()
    
    print(f"\n[COMPLETE] Transcripts saved to: {transcriber.transcripts_dir.absolute()}")
    print(f"[COMPLETE] Total videos transcribed: {len(transcribed)}")


if __name__ == "__main__":
    main()
