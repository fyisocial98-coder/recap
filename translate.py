import os
import re
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "Qwen/Qwen2-1.5B-Instruct"

def main():
    srt_path = "output/chinese.srt"
    out_path = "output/burmese.srt"

    if not os.path.exists(srt_path):
        print("❌ chinese.srt not found. Run transcribe.py first.")
        return

    # If empty file (no audio)
    if os.path.getsize(srt_path) == 0:
        print("⚠️ chinese.srt is empty. Creating empty burmese.srt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("")
        return

    print("🔄 Loading translation model (~3GB download on first run)...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype="auto", device_map="cpu")

    with open(srt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        line = line.strip()
        if re.match(r'^\d+$', line) or '-->' in line:
            new_lines.append(line)
        elif line == "":
            new_lines.append("")
        else:
            prompt = f"Translate Chinese to Burmese. Only output Burmese text.\nChinese: {line}\nBurmese:"
            inputs = tokenizer(prompt, return_tensors="pt")
            outputs = model.generate(inputs.input_ids, max_new_tokens=100, temperature=0.3)
            full = tokenizer.decode(outputs[0], skip_special_tokens=True)
            translation = full.split("Burmese:")[-1].strip() if "Burmese:" in full else line
            new_lines.append(translation)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))

    print("✅ Translation done -> output/burmese.srt")

if __name__ == "__main__":
    main()
