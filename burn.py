import subprocess
import os

def main():
    sub_path = "output/burmese.srt"
    if not os.path.exists(sub_path):
        print("❌ burmese.srt not found. Run translate.py first.")
        return

    # Path to Pyidaungsu font (download it in workflow)
    font_path = "/usr/share/fonts/truetype/pyidaungsu/Pyidaungsu.ttf"
    if not os.path.exists(font_path):
        print("⚠️ Pyidaungsu font not found, falling back to Noto Sans Myanmar")
        font_name = "Noto Sans Myanmar"
    else:
        font_name = font_path  # ffmpeg accepts full path

    style = f"FontName={font_name},FontSize=24,PrimaryColour=&HFFFFFF&,OutlineColour=&H80000000&,BorderStyle=3"

    cmd = [
        "ffmpeg", "-i", "input/video.mp4",
        "-vf", f"subtitles={sub_path}:force_style='{style}'",
        "-c:v", "libx264", "-crf", "23",
        "-c:a", "copy",
        "output/with_subs.mp4", "-y"
    ]
    subprocess.run(cmd, check=True)
    print("✅ Subtitles burned -> output/with_subs.mp4")

if __name__ == "__main__":
    main()
