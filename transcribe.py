import os
import subprocess
from faster_whisper import WhisperModel

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def main():
    os.makedirs("output", exist_ok=True)
    
    video_path = "input/video.mp4"
    audio_path = "input/audio.mp3"
    
    # Check if video has any audio stream
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=codec_type",
         "-of", "default=noprint_wrappers=1:nokey=1", video_path],
        capture_output=True, text=True
    )
    
    if not result.stdout.strip():
        print("⚠️ No audio stream found. Creating empty subtitle file.")
        with open("output/chinese.srt", "w", encoding="utf-8") as f:
            f.write("")
        return
    
    # Extract audio using "0:a?" -> ignore if missing
    cmd = [
        "ffmpeg", "-i", video_path,
        "-q:a", "0", "-map", "0:a?",
        audio_path, "-y"
    ]
    subprocess.run(cmd, check=True)
    
    # Load Whisper (CPU, base model)
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(audio_path, language="zh")
    
    with open("output/chinese.srt", "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments):
            f.write(f"{i+1}\n")
            f.write(f"{format_time(seg.start)} --> {format_time(seg.end)}\n")
            f.write(f"{seg.text.strip()}\n\n")
    
    print("✅ Transcription done -> output/chinese.srt")

if __name__ == "__main__":
    main()
