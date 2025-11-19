import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import yt_dlp
import os
import threading
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


def show_ffmpeg_warning():
    """Show installation instructions for ffmpeg."""
    warning_msg = """FFmpeg is not installed or not found in PATH!

FFmpeg is required for merging video and audio streams for HD quality.

Installation Instructions:

Windows:
  • Download from: https://www.gyan.dev/ffmpeg/builds/
  • Extract and add to PATH, OR
  • Use: winget install ffmpeg

Mac:
  • brew install ffmpeg

Linux:
  • sudo apt install ffmpeg  (Debian/Ubuntu)
  • sudo yum install ffmpeg  (RedHat/CentOS)

After installation, restart this application.

Continue anyway? (Some videos may still download, but quality may be limited)"""
    
    response = messagebox.askokcancel(
        "FFmpeg Not Found",
        warning_msg,
        icon=messagebox.WARNING
    )
    return response


class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader (HD)")
        self.root.geometry("700x550")
        self.root.resizable(False, False)
        
        # Set default output path
        self.output_path = os.path.join(os.getcwd(), 'downloads')
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.setup_ui()
        self.check_ffmpeg_on_start()
        
    def check_ffmpeg_on_start(self):
        """Check for ffmpeg when the application starts."""
        if not check_ffmpeg():
            if not show_ffmpeg_warning():
                self.root.destroy()
                return
            self.log_message("⚠️  WARNING: FFmpeg not detected. Some features may be limited.")
        else:
            self.log_message("✅ FFmpeg detected - ready for HD downloads!")
        self.log_message("="*60)
        
    def setup_ui(self):
        """Set up the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="🎥 YouTube Video Downloader", 
            font=("Arial", 18, "bold"),
            fg="#CC0000"
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # URL Input Section
        url_label = ttk.Label(main_frame, text="Video URL:", font=("Arial", 11))
        url_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        self.url_entry = ttk.Entry(main_frame, width=70, font=("Arial", 10))
        self.url_entry.grid(row=2, column=0, columnspan=3, pady=(0, 15), ipady=5)
        self.url_entry.focus()
        
        # Output Directory Section
        output_label = ttk.Label(main_frame, text="Save to:", font=("Arial", 11))
        output_label.grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        
        self.output_entry = ttk.Entry(main_frame, width=55, font=("Arial", 10))
        self.output_entry.insert(0, self.output_path)
        self.output_entry.grid(row=4, column=0, columnspan=2, pady=(0, 15), ipady=5)
        
        browse_btn = ttk.Button(
            main_frame, 
            text="Browse...", 
            command=self.browse_folder,
            width=12
        )
        browse_btn.grid(row=4, column=2, padx=(5, 0), pady=(0, 15))
        
        # Quality Selection
        quality_label = ttk.Label(main_frame, text="Quality:", font=("Arial", 11))
        quality_label.grid(row=5, column=0, sticky=tk.W, pady=(0, 5))
        
        self.quality_var = tk.StringVar(value="1080p (Full HD)")
        quality_options = [
            "2160p (4K)",
            "1440p (2K)", 
            "1080p (Full HD)",
            "720p (HD)",
            "480p",
            "Best Available"
        ]
        quality_dropdown = ttk.Combobox(
            main_frame, 
            textvariable=self.quality_var,
            values=quality_options,
            state="readonly",
            width=25,
            font=("Arial", 10)
        )
        quality_dropdown.grid(row=6, column=0, sticky=tk.W, pady=(0, 15))
        
        # Download Button
        self.download_btn = tk.Button(
            main_frame,
            text="⬇️  Download Video",
            command=self.start_download,
            font=("Arial", 12, "bold"),
            bg="#CC0000",
            fg="white",
            activebackground="#990000",
            activeforeground="white",
            cursor="hand2",
            pady=10
        )
        self.download_btn.grid(row=7, column=0, columnspan=3, pady=(0, 20), sticky=(tk.W, tk.E))
        
        # Progress Bar
        self.progress = ttk.Progressbar(
            main_frame, 
            mode='indeterminate', 
            length=660
        )
        self.progress.grid(row=8, column=0, columnspan=3, pady=(0, 10))
        
        # Status/Log Area
        status_label = ttk.Label(main_frame, text="Status:", font=("Arial", 11))
        status_label.grid(row=9, column=0, sticky=tk.W, pady=(0, 5))
        
        self.status_text = scrolledtext.ScrolledText(
            main_frame,
            width=80,
            height=12,
            font=("Consolas", 9),
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg="#f0f0f0"
        )
        self.status_text.grid(row=10, column=0, columnspan=3)
        
        # Initial status message will be set by check_ffmpeg_on_start
        
    def browse_folder(self):
        """Open folder browser dialog."""
        folder = filedialog.askdirectory(initialdir=self.output_path)
        if folder:
            self.output_path = folder
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, folder)
            
    def log_message(self, message):
        """Add message to status text area."""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
        self.root.update_idletasks()
        
    def clear_log(self):
        """Clear the status text area."""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.delete(1.0, tk.END)
        self.status_text.config(state=tk.DISABLED)
        
    def start_download(self):
        """Start the download process in a separate thread."""
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showwarning("No URL", "Please enter a YouTube video URL.")
            return
            
        # Disable button and start progress
        self.download_btn.config(state=tk.DISABLED, text="Downloading...")
        self.progress.start(10)
        self.clear_log()
        
        # Run download in separate thread to keep GUI responsive
        download_thread = threading.Thread(
            target=self.download_video, 
            args=(url,),
            daemon=True
        )
        download_thread.start()
        
    def get_format_string(self):
        """Get the format string based on selected quality."""
        quality = self.quality_var.get()
        
        # Map quality selection to height
        quality_map = {
            "2160p (4K)": 2160,
            "1440p (2K)": 1440,
            "1080p (Full HD)": 1080,
            "720p (HD)": 720,
            "480p": 480,
            "Best Available": 9999  # Use very high number for best available
        }
        
        height = quality_map.get(quality, 1080)
        
        if height == 9999:
            # Best available quality
            return 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best'
        else:
            # Specific quality
            return f'bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<={height}]+bestaudio/best[height<={height}]/best'
    
    def download_video(self, url):
        """Download the video using yt-dlp."""
        output_path = self.output_entry.get().strip()
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        # Get selected quality
        selected_quality = self.quality_var.get()
            
        # Configure yt-dlp options for faster HD downloads
        ydl_opts = {
            # Quality based on user selection
            'format': self.get_format_string(),
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
            
            'quiet': True,
            'no_warnings': True,
            'progress_hooks': [self.progress_hook],
        }
        
        try:
            self.log_message(f"🔗 URL: {url}")
            self.log_message(f"📁 Saving to: {output_path}")
            self.log_message(f"🎬 Quality: {selected_quality}\n")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get video info first
                self.log_message("📋 Fetching video information...")
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', 'Unknown')
                duration = info.get('duration', 0)
                uploader = info.get('uploader', 'Unknown')
                
                self.log_message(f"📹 Title: {video_title}")
                self.log_message(f"👤 Channel: {uploader}")
                self.log_message(f"⏱️  Duration: {duration // 60}:{duration % 60:02d}")
                self.log_message(f"\n⬇️  Starting download ({selected_quality})...\n")
                
                # Download the video
                ydl.download([url])
                
            self.log_message("\n" + "="*60)
            self.log_message("✅ Download completed successfully!")
            self.log_message(f"📂 Video saved to: {output_path}")
            self.log_message("="*60)
            
            # Show success message
            self.root.after(0, lambda: messagebox.showinfo(
                "Success", 
                f"Video downloaded successfully!\n\nSaved to:\n{output_path}"
            ))
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            self.log_message("\n" + error_msg)
            self.root.after(0, lambda: messagebox.showerror(
                "Download Error", 
                f"An error occurred:\n\n{str(e)}"
            ))
            
        finally:
            # Re-enable button and stop progress
            self.root.after(0, self.reset_ui)
            
    def progress_hook(self, d):
        """Hook to display download progress."""
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            
            # Only log every few updates to avoid flooding
            if hasattr(self, '_last_percent'):
                if self._last_percent == percent:
                    return
            self._last_percent = percent
            
            msg = f"⬇️  Progress: {percent} | Speed: {speed} | ETA: {eta}"
            self.root.after(0, lambda: self.log_message(msg))
            
        elif d['status'] == 'finished':
            self.root.after(0, lambda: self.log_message("\n🔄 Processing video (merging/converting)..."))
            
    def reset_ui(self):
        """Reset UI elements after download."""
        self.download_btn.config(state=tk.NORMAL, text="⬇️  Download HD Video")
        self.progress.stop()


def main():
    """Main function to run the GUI application."""
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

