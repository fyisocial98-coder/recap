import subprocess

def main():
    cmd = [
        "ffmpeg", "-i", "output/with_subs.mp4",
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
        "-c:v", "libx264", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        "output/tiktok_final.mp4", "-y"
    ]
    subprocess.run(cmd, check=True)
    print("✅ TikTok ready -> output/tiktok_final.mp4")

if __name__ == "__main__":
    main()
