import yt_dlp
import os
import sys
import subprocess
import shutil


def check_ffmpeg():
    """
    Check if ffmpeg is installed and accessible.
    Returns True if available, False otherwise.
    Also adds FFmpeg to PATH if found in common winget locations.
    """
    # Check if ffmpeg is in PATH
    if shutil.which('ffmpeg') is not None:
        return True
    
    # Check common winget installation locations
    winget_base = os.path.join(os.environ.get('LOCALAPPDATA', ''), 
                               'Microsoft', 'WinGet', 'Packages')
    
    if os.path.exists(winget_base):
        for item in os.listdir(winget_base):
            if 'ffmpeg' in item.lower():
                # Look for ffmpeg.exe in subdirectories
                package_dir = os.path.join(winget_base, item)
                for root, dirs, files in os.walk(package_dir):
                    if 'ffmpeg.exe' in files:
                        ffmpeg_dir = root
                        # Add to PATH for this session
                        os.environ['PATH'] = ffmpeg_dir + os.pathsep + os.environ.get('PATH', '')
                        return True
    
    # Try to run ffmpeg command
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE, 
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def print_ffmpeg_warning():
    """Print installation instructions for ffmpeg."""
    print("\n" + "="*60)
    print("⚠️  WARNING: FFmpeg not found!")
    print("="*60)
    print("\nFFmpeg is required for merging video and audio streams.")
    print("The download may still work for some videos, but for best")
    print("quality (HD), please install FFmpeg:\n")
    print("Windows:")
    print("  1. Download from: https://www.gyan.dev/ffmpeg/builds/")
    print("  2. Extract and add to PATH, OR")
    print("  3. Use: winget install ffmpeg\n")
    print("Mac:")
    print("  brew install ffmpeg\n")
    print("Linux:")
    print("  sudo apt install ffmpeg  (Debian/Ubuntu)")
    print("  sudo yum install ffmpeg  (RedHat/CentOS)")
    print("="*60 + "\n")
    
    response = input("Continue anyway? (y/n): ").strip().lower()
    if response != 'y':
        print("Exiting. Please install FFmpeg and try again.")
        sys.exit(0)


def download_video(url, output_path='downloads'):
    """
    Download a YouTube video in HD quality.
    
    Args:
        url (str): YouTube video URL
        output_path (str): Directory to save the downloaded video
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # Configure yt-dlp options for faster HD downloads
    ydl_opts = {
        # HD Quality: Prefer 1080p with best codecs (VP9/AV1 for video, Opus for audio)
        'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best[height<=1080]/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        
        # Speed optimizations
        'concurrent_fragment_downloads': 8,  # Download fragments in parallel
        'http_chunk_size': 10485760,  # 10MB chunks for faster downloads
        'retries': 10,  # Retry on failure
        'fragment_retries': 10,  # Retry fragments
        'buffersize': 1024 * 1024 * 2,  # 2MB buffer
        
        # Quality settings
        'prefer_free_formats': False,  # Don't prefer free formats, prefer quality
        
        # Post-processing
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        
        'quiet': False,
        'no_warnings': False,
    }
    
    try:
        print(f"\n🎬 Starting download from: {url}")
        print(f"📁 Saving to: {os.path.abspath(output_path)}\n")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get video info first
            info = ydl.extract_info(url, download=False)
            video_title = info.get('title', 'Unknown')
            duration = info.get('duration', 0)
            
            print(f"📹 Video: {video_title}")
            print(f"⏱️  Duration: {duration // 60}:{duration % 60:02d}")
            print(f"\n⬇️  Downloading in HD quality...\n")
            
            # Download the video
            ydl.download([url])
            
        print(f"\n✅ Download completed successfully!")
        print(f"📂 Check the '{output_path}' folder for your video.\n")
        
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}\n")
        sys.exit(1)


def main():
    """Main function to handle user input and start download."""
    print("\n" + "="*50)
    print("🎥 YouTube Video Downloader (HD)")
    print("="*50 + "\n")
    
    # Check for ffmpeg
    if not check_ffmpeg():
        print_ffmpeg_warning()
    else:
        print("✅ FFmpeg detected - ready for HD downloads!\n")
    
    # Get URL from user
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Enter YouTube video URL: ").strip()
    
    if not url:
        print("❌ No URL provided. Exiting.")
        sys.exit(1)
    
    # Optional: custom output path
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    else:
        output_path = 'downloads'
    
    download_video(url, output_path)


if __name__ == "__main__":
    main()

