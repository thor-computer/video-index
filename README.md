# Video Index

Download YouTube channel videos, transcribe them with OpenAI Whisper, and search through the transcripts with timestamped results.

## Features

- **Download entire YouTube channels**: Uses yt-dlp to download all videos from a channel
- **Local transcription**: Uses OpenAI Whisper to transcribe videos locally (no API costs)
- **Searchable transcripts**: Search across all transcripts and get timestamped YouTube URLs
- **Smart skipping**: Automatically skips already processed videos
- **Space-saving**: Replaces video files with empty placeholders after transcription

## Prerequisites

- **Python 3.8+**
- **FFmpeg** - Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to your system PATH

## Usage

### Download and Transcribe

Process all videos from a channel:

```bat
run.bat "https://www.youtube.com/@channelname"
```

Process only the 5 most recent videos:

```bat
run.bat "https://www.youtube.com/@channelname" 5
```

The script will:
1. Set up a virtual environment and install dependencies
2. Download videos to `videos/`
3. Transcribe each video and save to `transcripts/`
4. Replace video files with empty placeholders to save disk space

Re-running the script on the same channel will only process new videos.

### Search Transcripts

Search across all transcripts:

```bat
search.bat "your search query"
```

Results include timestamps and direct YouTube URLs:

```
[RESULTS] Found 3 matches:

Video: dQw4w9WgXcQ

[1] Timestamp: 01:23
    Text: This is the matching text from the video
    URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=83s
```

## Whisper Models

The default model is `base`. You can change this by editing `run.bat`:

- **tiny**: Fastest, least accurate (~1GB RAM)
- **base**: Good balance (default, ~1GB RAM)
- **small**: Better accuracy (~2GB RAM)
- **medium**: High accuracy (~5GB RAM)
- **large**: Best accuracy (~10GB RAM)

## Troubleshooting

**"FFmpeg not found"**

Install FFmpeg and add it to your system PATH, then restart your terminal.

**"No videos found"**

Ensure the YouTube URL is correct. Try using the channel's main page URL.

**Transcription is slow**

Use a smaller Whisper model (tiny or base). Transcription is CPU/GPU intensive and takes time.

**Out of memory**

Use a smaller Whisper model or process fewer videos at a time.

## How It Works

The program uses yt-dlp to download videos from YouTube channels, then transcribes them locally using OpenAI's Whisper model. After transcription, video files are replaced with empty placeholders to save disk space while keeping the transcripts for searching.

## License

This project is provided as-is for personal use. Please respect YouTube's Terms of Service and copyright laws when downloading videos.
