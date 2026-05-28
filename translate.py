import os
import re
import unicodedata
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

MODEL_NAME = "facebook/m2m100_418M"

def main():
    srt_path = "output/chinese.srt"
    out_path = "output/burmese.srt"

    if not os.path.exists(srt_path):
        print("❌ chinese.srt not found. Run transcribe.py first.")
        return

    if os.path.getsize(srt_path) == 0:
        print("⚠️ chinese.srt is empty. Creating empty burmese.srt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("")
        return

    print("🔄 Loading m2m100 model (~1.5GB)...")
    tokenizer = M2M100Tokenizer.from_pretrained(MODEL_NAME, src_lang="zh", tgt_lang="my")
    model = M2M100ForConditionalGeneration.from_pretrained(MODEL_NAME, device_map="cpu")

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
            tokenizer.src_lang = "zh"
            encoded = tokenizer(line, return_tensors="pt")
            generated_tokens = model.generate(**encoded, forced_bos_token_id=tokenizer.get_lang_id("my"))
            translation = tokenizer.decode(generated_tokens[0], skip_special_tokens=True)
            translation = unicodedata.normalize('NFC', translation)
            new_lines.append(translation)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))

    print("✅ Translation done -> output/burmese.srt")

if __name__ == "__main__":
    main()
