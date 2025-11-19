# YouTube Video Downloader

A simple Python script to download YouTube videos in HD quality using yt-dlp.

## Features

- **Multiple Quality Options**: 4K, 2K, 1080p, 720p, 480p, or Best Available
- **Fast Downloads**: Parallel fragment downloads (8x concurrent) with 10MB chunks
- **Smart Codec Selection**: Automatically chooses best codecs for quality
- **HD Quality**: Up to 4K (2160p) support
- **Auto-merge**: Automatically merges best video and audio streams
- **MP4 Format**: Saves videos in universal MP4 format
- **Progress Tracking**: Real-time progress bar with speed and ETA
- **Video Info**: Shows title, channel, and duration before downloading
- **Retry Logic**: Automatic retries on network issues

## Requirements

- Python 3.7 or higher
- yt-dlp
- FFmpeg (required for HD quality)

## Installation

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Install FFmpeg (Required)

FFmpeg is **required** for merging video and audio streams to get HD quality videos.

#### Windows

Option 1 (Easiest - Automated):
```bash
install_ffmpeg.bat
```
Run the provided batch script that will automatically install FFmpeg using winget.

Option 2 (Manual - winget):
```bash
winget install ffmpeg
```

Option 3 (Manual - Download):
1. Download from [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)
2. Extract the archive
3. Add the `bin` folder to your system PATH

#### Mac

```bash
brew install ffmpeg
```

#### Linux

Debian/Ubuntu:
```bash
sudo apt update
sudo apt install ffmpeg
```

RedHat/CentOS:
```bash
sudo yum install ffmpeg
```

### Step 3: Verify Installation

Both scripts will automatically check for FFmpeg when you run them and display a warning if it's not found.

## Usage

### GUI Version (Recommended)

Run the graphical interface:

```bash
python youtube_downloader_gui.py
```

This opens a user-friendly window where you can:
- **Paste YouTube URLs** - Simply copy and paste any YouTube video URL
- **Select Quality** - Choose from 4K, 2K, 1080p, 720p, 480p, or Best Available
- **Choose Save Location** - Pick where to save your videos
- **Real-time Progress** - Watch download progress with speed and ETA
- **Video Information** - See title, channel, and duration before downloading

The GUI now includes:
- **Quality selector dropdown** for choosing video resolution
- **Optimized downloads** with 8x parallel fragment downloading
- **Smart FFmpeg detection** that automatically finds your installation

### Command Line Version

#### Method 1: Interactive mode

Run the script and enter the URL when prompted:

```bash
python youtube_downloader.py
```

#### Method 2: Command line argument

Provide the URL directly:

```bash
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

#### Method 3: Custom output directory

Specify a custom output folder:

```bash
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" "my_videos"
```

## Output

- Videos are saved to the `downloads` folder by default
- Filename format: `[Video Title].mp4`

## Notes

- The script downloads the best available quality up to 1080p (HD)
- Make sure you have enough disk space for the video
- Downloading videos may be subject to YouTube's terms of service
- Some videos may be restricted or unavailable for download

## Troubleshooting

### FFmpeg Not Found

If you see an FFmpeg warning:
1. Make sure FFmpeg is installed (see installation instructions above)
2. Verify FFmpeg is in your PATH by running: `ffmpeg -version`
3. Restart your terminal/command prompt after installation
4. On Windows, you may need to restart your computer

### Other Issues

- **Codec errors**: Make sure FFmpeg is properly installed
- **Download failures**: Try updating yt-dlp: `pip install --upgrade yt-dlp`
- **Connection errors**: Check your internet connection and ensure the video is publicly accessible
- **Permission errors**: Run the script with appropriate permissions or change the output directory

## License

This project is for educational purposes only. Please respect copyright laws and YouTube's terms of service.

