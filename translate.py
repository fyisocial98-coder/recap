import os
import re
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

def main():
    srt_path = "output/chinese.srt"
    out_path = "output/burmese.srt"

    if not os.path.exists(srt_path):
        print("❌ chinese.srt not found.")
        return

    print("🔄 Loading High-Quality Qwen2.5-1.5B Model...")
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
            messages = [
                {"role": "system", "content": "You are a professional Chinese to Burmese translator. Translate the given text into natural and fluent Burmese subtitle. Output ONLY the Burmese translation, no English, no explanations."},
                {"role": "user", "content": line}
            ]
            text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs = tokenizer([text], return_tensors="pt")
            outputs = model.generate(inputs.input_ids, max_new_tokens=100, temperature=0.1)
            
            generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(inputs.input_ids, outputs)]
            translation = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
            
            new_lines.append(translation)
            print(f"Chinese: {line} ➡️ Burmese: {translation}")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))

    print("✅ High-Quality Translation done -> output/burmese.srt")

if __name__ == "__main__":
    main()
