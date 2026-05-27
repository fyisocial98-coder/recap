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
    
    subprocess.run([
        "ffmpeg", "-i", video_path, "-q:a", "0", "-map", "0:a?", audio_path, "-y"
    ], check=True)
    
    # beam_size=5 သို့ ပြန်တိုးမြှင့်လိုက်သဖြင့် တရုတ်စကားလုံးများကို အမှန်ကန်ဆုံး နားထောင်ပေးမည် ဖြစ်သည်
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(audio_path, language="zh", beam_size=5)
    
    with open("output/chinese.srt", "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments):
            f.write(f"{i+1}\n")
            f.write(f"{format_time(seg.start)} --> {format_time(seg.end)}\n")
            f.write(f"{seg.text.strip()}\n\n")
    
    print("✅ High-Quality Transcription done -> output/chinese.srt")

if __name__ == "__main__":
    main()
