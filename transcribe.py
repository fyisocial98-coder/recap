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
    
    # --- ဗီဒီယိုဖိုင် တကယ် ရှိမရှိ နှင့် ပျက်မပျက် ကြိုတင်စစ်ဆေးခြင်း ---
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"❌ [Error] '{video_path}' ဖိုင်ကို ရှာမတွေ့ပါ။ ရှေ့က 'Download video' အဆင့်မှာ ဗီဒီယိုလင့်ခ် ဒေါင်းလုဒ်ဆွဲတာ အောင်မြင်မှု ရှိမရှိ ပြန်စစ်ပေးပါ။")
        
    if os.path.getsize(video_path) == 0:
        raise ValueError(f"❌ [Error] '{video_path}' ဖိုင်က 0 Bytes ဖြစ်နေပါတယ်။ ဗီဒီယို ဒေါင်းလုဒ်ဆွဲတာ မပြည့်စုံခဲ့ပါ။")
    
    print("🎵 Extracting audio using FFmpeg...")
    subprocess.run([
        "ffmpeg", "-i", video_path, "-q:a", "0", "-map", "0:a?", audio_path, "-y"
    ], check=True)
    
    print("🎙️ Starting Whisper Transcription...")
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
