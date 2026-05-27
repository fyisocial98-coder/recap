import subprocess
import os
import shutil

def main():
    input_video = "output/with_subs.mp4"
    output_video = "output/tiktok_final.mp4"
    
    if not os.path.exists(input_video):
        print("⚠️ with_subs.mp4 not found, using original video")
        shutil.copy("input/video.mp4", output_video)
        return

    # ဗီဒီယိုကို ဘေးအမည်းကွက်များမချန်ဘဲ Blurred Background ပြုလုပ်ပြီး အပေါ်တွင် Title တပ်ဆင်ခြင်း
    title_text = "Chinese Short Drama 🎬" 
    
    filter_complex = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20:10[bg];"
        "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease[fg];"
        "[bg][fg]overlay=(W-w)/2:(H-h)/2[combined];"
        f"[combined]drawtext=text='{title_text}':fontcolor=white:fontfile=/usr/share/fonts/truetype/pyidaungsu/Pyidaungsu.ttf:"
        "fontsize=45:box=1:boxcolor=red@0.8:boxborderw=20:x=(w-text_w)/2:y=150"
    )

    cmd = [
        "ffmpeg", "-i", input_video,
        "-filter_complex", filter_complex,
        "-c:v", "libx264", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        output_video, "-y"
    ]
    
    print("📱 Transforming video to Premium TikTok Layout (Blur BG + Top Title)...")
    subprocess.run(cmd, check=True)
    print("✅ TikTok Premium Video Ready ->", output_video)

if __name__ == "__main__":
    main()
