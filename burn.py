import subprocess
import os

def main():
    if not os.path.exists("output/burmese.srt"):
        print("⚠️ No burmese.srt, skipping burn")
        return
        
    style = (
        "FontName=Pyidaungsu,"
        "FontSize=25,"
        "PrimaryColour=&H00FFFFFF&,"
        "BackColour=&H00000000&,"
        "BorderStyle=3,"
        "Outline=0,"
        "Shadow=0,"
        "MarginV=120"
    )
    
    cmd = [
        "ffmpeg", "-i", "input/video.mp4",
        "-vf", f"subtitles=output/burmese.srt:force_style='{style}'",
        "-c:v", "libx264", "-crf", "23",
        "-c:a", "copy",
        "output/with_subs.mp4", "-y"
    ]
    
    print("🎬 Burning High-Quality Burmese subtitles...")
    subprocess.run(cmd, check=True)
    print("✅ Subtitles burned successfully.")

if __name__ == "__main__":
    main()
