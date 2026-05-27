import os
import subprocess
from faster_whisper import WhisperModel

def fmt(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def main():
    os.makedirs("output", exist_ok=True)
    subprocess.run(["ffmpeg", "-i", "input/video.mp4", "-q:a", "0", "-map", "a", "input/audio.mp3", "-y"], check=True)
    
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, _ = model.transcribe("input/audio.mp3", language="zh")
    
    with open("output/chinese.srt", "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments):
            f.write(f"{i+1}\n{fmt(seg.start)} --> {fmt(seg.end)}\n{seg.text.strip()}\n\n")
    print("✅ Transcribed -> output/chinese.srt")

if __name__ == "__main__":
    main()