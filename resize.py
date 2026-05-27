import subprocess
import os
import shutil

def main():
    input_video = "output/with_subs.mp4"
    output_video = "output/tiktok_final.mp4"
    
    if not os.path.exists(input_video):
        print("⚠️ with_subs.mp4 not found, using original video")
        shutil.copy("input/video.mp4", output_video)
    else:
        cmd = [
            "ffmpeg", "-i", input_video,
            "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
            "-c:v", "libx264", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k",
            output_video, "-y"
        ]
        subprocess.run(cmd, check=True)
    
    print("✅ TikTok ready ->", output_video)

if __name__ == "__main__":
    main()
