import os
import re
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL = "Qwen/Qwen2-1.5B-Instruct"

def main():
    if not os.path.exists("output/chinese.srt"):
        print("❌ Run transcribe.py first")
        return
    
    print("Loading model (~3GB download on first run)...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL, torch_dtype="auto", device_map="cpu")
    
    with open("output/chinese.srt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        line = line.strip()
        if re.match(r'^\d+$', line) or '-->' in line:
            new_lines.append(line)
        elif line == "":
            new_lines.append("")
        else:
            prompt = f"Translate Chinese to Burmese. Only output Burmese.\nChinese: {line}\nBurmese:"
            inputs = tokenizer(prompt, return_tensors="pt")
            out = model.generate(inputs.input_ids, max_new_tokens=100, temperature=0.3)
            full = tokenizer.decode(out[0], skip_special_tokens=True)
            trans = full.split("Burmese:")[-1].strip() if "Burmese:" in full else line
            new_lines.append(trans)
    
    with open("output/burmese.srt", "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))
    print("✅ Translated -> output/burmese.srt")

if __name__ == "__main__":
    main()