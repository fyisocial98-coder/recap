import subprocess
import os
import shutil

def main():
    input_video = "output/with_subs.mp4"
    output_video = "output/tiktok_final.mp4"
    
    if not os.path.exists(input_video):
        shutil.copy("input/video.mp4", output_video)
        return

    title_text = "Chinese Short Drama 🎬" 
    
    # Downscale Blur နည်းပညာဖြင့် ဗီဒီယို Processing ကို အချိန်ကုန် သက်သာစေသည်
    filter_complex = (
        "[0:v]scale=180:320,boxblur=5,scale=1080:1920[bg];"
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
    
    print("📱 Creating TikTok Layout (Fast Blur BG)...")
    subprocess.run(cmd, check=True)
    print("✅ TikTok Final Video Ready ->", output_video)

if __name__ == "__main__":
    main()
