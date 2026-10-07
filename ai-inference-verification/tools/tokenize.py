import json
from huggingface_hub import snapshot_download
p=snapshot_download("unsloth/Llama-3.1-8B-Instruct", allow_patterns=["tokenizer*","*.json"], ignore_patterns=["*.safetensors*"])
from transformers import AutoTokenizer
tok=AutoTokenizer.from_pretrained(p)
prompts=["The capital of France is","2 + 2 =","Roses are red, violets are"]
out=[]
for s in prompts:
    ids=tok(s).input_ids
    out.append({"text":s,"ids":ids,"pieces":[tok.decode([i]) for i in ids]})
    print(s, "->", ids, [tok.decode([i]) for i in ids])
print("vocab", len(tok), "bos", tok.bos_token_id, "eos", tok.eos_token_id)
json.dump(out, open("data/llama31-8b-tokens.json","w"), indent=1)
