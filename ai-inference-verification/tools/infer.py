# Run Llama-3.1-8B-Instruct (bf16) on three short prompts: greedy 4 tokens,
# top-5 logits per step, per-layer residual RMS, attention rows for two heads,
# the layer-0 norm output and its int8 requantisation for the last prompt token.
import os, json, time, math, sys, torch
from huggingface_hub import snapshot_download
from transformers import AutoTokenizer, AutoModelForCausalLM
t0 = time.time()
p = snapshot_download("unsloth/Llama-3.1-8B-Instruct", allow_patterns=["*.json","*.safetensors","tokenizer*"])
tok = AutoTokenizer.from_pretrained(p)
want = sys.argv[1] if len(sys.argv) > 1 else ("mps" if torch.backends.mps.is_available() else "cpu")
def load(dev):
    m = AutoModelForCausalLM.from_pretrained(p, dtype=torch.bfloat16, attn_implementation="eager", low_cpu_mem_usage=True)
    return m.to(dev).eval()
try:
    model = load(want); dev = want
except Exception as e:
    print("fallback to cpu:", repr(e)[:200], flush=True)
    model = load("cpu"); dev = "cpu"
print("loaded on", dev, "in", int(time.time()-t0), "s", flush=True)

cap = {}
def pre_hook(mod, args):
    cap["norm1_out"] = args[0].detach().float().cpu()
h = model.model.layers[0].self_attn.q_proj.register_forward_pre_hook(pre_hook)

def bf16_ceil(x):
    t = torch.tensor(x, dtype=torch.float32).to(torch.bfloat16)
    if float(t) < x:
        t = torch.nextafter(t.float(), torch.tensor(float("inf"))).to(torch.bfloat16)
    return float(t)

def top5(logits):
    v, i = torch.topk(logits.float(), 5)
    return [{"id": int(a), "piece": tok.decode([int(a)]), "logit": round(float(b), 3)} for b, a in zip(v, i)]

prompts = ["The capital of France is", "2 + 2 =", "Roses are red, violets are"]
runs = []
with torch.no_grad():
    for text in prompts:
        ids = tok(text).input_ids
        x = torch.tensor([ids], device=dev)
        out = model(x, output_attentions=True, output_hidden_states=True, use_cache=True)
        hs = out.hidden_states
        rms = [round(float(h_[0, -1].float().pow(2).mean().sqrt()), 3) for h_ in hs]
        emb8 = [round(float(v), 4) for v in hs[0][0, -1, :8].float()]
        att = out.attentions
        def row(layer, head):
            r = att[layer][0, head, -1].float().cpu()
            return [round(float(v), 4) for v in r]
        n1 = cap["norm1_out"][0, -1]
        mx = float(n1.abs().max())
        s_x = bf16_ceil(mx / 127)
        q8 = [int(torch.round(v / s_x).clamp(-127, 127)) for v in n1[:8]]
        W = model.model.layers[0].self_attn.q_proj.weight[0].detach().float().cpu()
        s_w = float(W.abs().max() / 127)
        w8 = [int(torch.round(v / s_w).clamp(-127, 127)) for v in W[:8]]
        steps = []
        logits = out.logits[0, -1]
        past = out.past_key_values
        gen = []
        for k in range(4):
            t5 = top5(logits)
            nxt = int(torch.argmax(logits))
            steps.append({"top5": t5, "argmax": nxt, "piece": tok.decode([nxt]),
                          "tie": bool((logits == logits.max()).sum() > 1)})
            gen.append(nxt)
            o2 = model(torch.tensor([[nxt]], device=dev), past_key_values=past, use_cache=True)
            logits = o2.logits[0, -1]; past = o2.past_key_values
        runs.append({"text": text, "ids": ids, "pieces": [tok.decode([i]) for i in ids],
                     "gen": gen, "gen_pieces": [tok.decode([g]) for g in gen], "steps": steps,
                     "rms": rms, "emb8": emb8,
                     "attn": {"l0h0": row(0, 0), "l15h0": row(15, 0), "l31h0": row(31, 0)},
                     "norm1": {"max_abs": round(mx, 4), "s_x": s_x, "h8": [round(float(v), 4) for v in n1[:8]], "q8": q8},
                     "wq": {"s_w_ch0": round(s_w, 6), "w8": w8, "wfloat8": [round(float(v), 5) for v in W[:8]]}})
        print(text, "->", [tok.decode([g]) for g in gen], flush=True)
h.remove()
json.dump({"device": dev, "model": "unsloth/Llama-3.1-8B-Instruct", "dtype": "bfloat16",
           "secs": int(time.time()-t0), "runs": runs}, open("data/llama31-8b-decode-run.json", "w"), indent=1)
print("DONE", int(time.time()-t0), "s")
