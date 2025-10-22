# Video Index

A Python-based tool for downloading YouTube channel videos, transcribing them with OpenAI Whisper, and searching through the transcripts with timestamped results.

## Features

- **Download entire YouTube channels**: Uses yt-dlp to download all videos from a YouTube channel or profile
- **Incremental processing**: Processes one video at a time (download → transcribe → next)
- **Smart skipping**: Automatically skips already downloaded videos and existing transcripts
- **Re-run friendly**: Perfect for updating when new videos are posted - only processes new content
- **Local transcription**: Uses OpenAI Whisper to transcribe videos locally (no API costs)
- **Searchable transcripts**: Search across all transcripts and get timestamped YouTube URLs
- **Simple interface**: Easy-to-use batch files for Windows

## Requirements

- Python 3.8 or higher
- Windows (for .bat files, but Python scripts work cross-platform)
- FFmpeg (required by Whisper, install separately)

## Installation

1. Clone or download this repository
2. Install FFmpeg if not already installed:
   - Download from https://ffmpeg.org/download.html
   - Add to your system PATH

## Usage

### Step 1: Download and Transcribe Videos

Run `run.bat` and provide a YouTube channel URL when prompted:

```batch
run.bat
```

**For testing with a limited number of videos**, you can specify the maximum number of most recent videos to download:

```batch
run.bat 5
```

This will download only the 5 most recent videos from the channel.

You can also specify the limit interactively when prompted during execution.

The script will:
1. Create a virtual environment
2. Install all dependencies
3. Process each video one at a time:
   - Download the video (skip if already exists)
   - Transcribe the video (skip if transcript already exists)
   - Move to next video

**Incremental Processing Benefits**:
- If a video is already downloaded, it won't be downloaded again
- If a transcript already exists, it won't be transcribed again
- Perfect for re-running on the same channel to catch new videos
- Saves time and bandwidth on subsequent runs

**Note**: This process can take a long time depending on:
- Number of videos in the channel
- Length of videos
- Your computer's processing power

Videos are saved to `videos/` and transcripts to `transcripts/`.

### Step 2: Search Transcripts

Run `search.bat` and enter your search query:

```batch
search.bat
```

The search will:
- Find all matching text across all transcripts
- Display the matching segments with timestamps
- Provide timestamped YouTube URLs that jump directly to the match

Example output:
```
[RESULTS] Found 3 matches:

Video: dQw4w9WgXcQ

[1] Timestamp: 01:23
    Text: This is the matching text from the video
    URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=83s
```

## Whisper Models

The default model is `base`, which provides a good balance of speed and accuracy. You can change this in `run.bat`:

- **tiny**: Fastest, least accurate (~1GB RAM)
- **base**: Good balance (default, ~1GB RAM)
- **small**: Better accuracy (~2GB RAM)
- **medium**: High accuracy (~5GB RAM)
- **large**: Best accuracy (~10GB RAM)

Edit line 48 in `run.bat` to change the model:
```batch
python transcriber.py small
```

## Project Structure

```
video-index/
├── run.bat              # Main script to download and transcribe
├── search.bat           # Search script
├── process_videos.py    # Main orchestrator (incremental processing)
├── downloader.py        # YouTube channel downloader
├── transcriber.py       # Whisper transcription module
├── searcher.py          # Transcript search module
├── requirements.txt     # Python dependencies
├── videos/              # Downloaded videos (created automatically)
├── transcripts/         # JSON transcripts (created automatically)
└── venv/                # Virtual environment (created automatically)
```

## Advanced Usage

You can also run the Python scripts directly:

### Process videos (recommended - incremental):
```bash
# Process all videos from a channel
python process_videos.py "https://www.youtube.com/@channelname"

# Process only 5 most recent videos
python process_videos.py "https://www.youtube.com/@channelname" 5

# Process with a different Whisper model
python process_videos.py "https://www.youtube.com/@channelname" 5 small
```

### Download videos only:
```bash
# Download all videos
python downloader.py "https://www.youtube.com/@channelname"

# Download only 5 most recent videos
python downloader.py "https://www.youtube.com/@channelname" 5
```

### Transcribe videos only:
```bash
python transcriber.py base
```

### Search transcripts:
```bash
python searcher.py "search query"
```

## Troubleshooting

### "FFmpeg not found"
- Install FFmpeg and add it to your system PATH
- Restart your terminal/command prompt after installation

### "No videos found"
- Ensure the YouTube URL is correct
- Try using the channel's main page URL
- Some channels may have restrictions

### Transcription is slow
- Use a smaller Whisper model (tiny or base)
- Transcription is CPU/GPU intensive and takes time
- Consider using GPU acceleration if you have CUDA-compatible GPU

### Out of memory
- Use a smaller Whisper model
- Close other applications
- Process fewer videos at a time

## License

This project is provided as-is for personal use. Please respect YouTube's Terms of Service and copyright laws when downloading videos.

## Dependencies

- **yt-dlp**: YouTube video downloader
- **openai-whisper**: Speech recognition model
- **torch**: PyTorch (required by Whisper)
- **tqdm**: Progress bars
