import subprocess
import os

def main():
    if not os.path.exists("output/burmese.srt"):
        print("⚠️ No burmese.srt, skipping burn")
        return
        
    # BorderStyle=3 (Opaque Box) နှင့် BackColour (အနက်ပိတ်) သုံးပြီး မူရင်းတရုတ်စာကို ဖုံးကွယ်ထားသည်
    # MarginV=120 သည် စာသားကို TikTok UI နှင့် မကွယ်စေရန် အပေါ်သို့ မြှင့်တင်ပေးသည်
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
        "-c:a", "copy",  # မူရင်းတရုတ်အသံကို မပျက်မစီးဘဲ ပုံစံအတိုင်း ယူဆောင်ခြင်း
        "output/with_subs.mp4", "-y"
    ]
    
    print("🎬 Burning Burmese subtitles into TikTok Safe Zone & masking Chinese text...")
    subprocess.run(cmd, check=True)
    print("✅ Subtitles burned successfully with Pyidaungsu Font.")

if __name__ == "__main__":
    main()
