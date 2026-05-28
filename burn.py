import os
import shutil
import subprocess

def main():
    srt_path = "output/burmese.srt"
    input_video = "input/video.mp4"
    output_video = "output/with_subs.mp4"
    
    # စာတန်းဖိုင် မရှိရင် သော်လည်းကောင်း၊ ဖိုင်ထဲတွင် စာသားမရှိဘဲ အလွတ်ဖြစ်နေရင်သော်လည်းကောင်း စာတန်းထိုးခြင်းကို ကျော်ပါမည်
    if not os.path.exists(srt_path) or os.path.getsize(srt_path) == 0:
        print("⚠️ [Warning] burmese.srt အလွတ်ဖြစ်နေသောကြောင့် စာတန်းထိုးခြင်းကို ကျော်ပြီး မူရင်းဗီဒီယိုကို တိုက်ရိုက်သုံးပါမည်။")
        os.makedirs("output", exist_ok=True)
        if os.path.exists(input_video):
            shutil.copy(input_video, output_video)
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
        "ffmpeg", "-i", input_video,
        "-vf", f"subtitles={srt_path}:force_style='{style}'",
        "-c:v", "libx264", "-crf", "23",
        "-c:a", "copy",
        output_video, "-y"
    ]
    
    print("🎬 Burning High-Quality Burmese subtitles...")
    subprocess.run(cmd, check=True)
    print("✅ Subtitles burned successfully.")

if __name__ == "__main__":
    main()
