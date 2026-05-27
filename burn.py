import subprocess
import os

def main():
    if not os.path.exists("output/burmese.srt"):
        print("⚠️ No burmese.srt, skipping burn")
        return
        
    # FontName ကို ပြည်ထောင်စုဖောင့်အမည် ပေးထားပါတယ်
    style = "FontName=Pyidaungsu,FontSize=24,PrimaryColour=&HFFFFFF&,OutlineColour=&H80000000&,BorderStyle=3"
    cmd = [
        "ffmpeg", "-i", "input/video.mp4",
        "-vf", f"subtitles=output/burmese.srt:force_style='{style}'",
        "-c:v", "libx264", "-crf", "23",
        "-c:a", "copy",
        "output/with_subs.mp4", "-y"
    ]
    subprocess.run(cmd, check=True)
    print("✅ Subtitles burned successfully with Pyidaungsu Font.")

if __name__ == "__main__":
    main()
