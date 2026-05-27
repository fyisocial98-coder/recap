import subprocess
import os

def main():
    sub_path = "output/burmese.srt"
    if not os.path.exists(sub_path):
        print("❌ burmese.srt not found. Run translate.py first.")
        return

    font_candidates = [
        "/usr/share/fonts/truetype/pyidaungsu/Pyidaungsu.ttf",
        "Pyidaungsu",  # fallback to system name
        "Noto Sans Myanmar"
    ]
    font_name = None
    for candidate in font_candidates:
        if candidate.endswith(".ttf") and os.path.exists(candidate):
            font_name = candidate
            break
        elif not candidate.endswith(".ttf"):
            font_name = candidate
            break

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
