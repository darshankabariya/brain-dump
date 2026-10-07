# Inject the run data into the page template and write decode-and-prove.html,
# wrapped in the same standalone skeleton the claude.ai artifact viewer adds, so
# the file opens directly in a browser.  Run from the topic directory:
#     python3 tools/build.py
import json, os, sys
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
tpl = open(os.path.join(here, "decode-and-prove.template.html"), encoding="utf-8").read()
runp = os.path.join(root, "data", "llama31-8b-decode-run.json")
if os.path.exists(runp):
    run = json.load(open(runp))
    runs = run["runs"]
    runs[0]["meta"] = {"device": run["device"], "secs": run["secs"], "model": run["model"]}
else:
    runs = json.load(open(os.path.join(root, "data", "llama31-8b-tokens.json")))
    print("WARNING: no decode run, tokens only", file=sys.stderr)
js = json.dumps(runs, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
body = tpl.replace("__RUNS__", js)
HEAD = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<style>:root{color-scheme:light;box-sizing:border-box}body{margin:0;padding:0;'
        'font:14px -apple-system,BlinkMacSystemFont,sans-serif;background:#faf9f5;color:#141413}'
        'img{max-width:100%}[hidden]{display:none!important}</style>\n</head>\n<body>\n')
TAIL = '</body>\n</html>\n'
dst = os.path.join(root, "decode-and-prove.html")
open(dst, "w", encoding="utf-8").write(HEAD + body + TAIL)
print("wrote", dst, "runs:", [r["text"] for r in runs])
