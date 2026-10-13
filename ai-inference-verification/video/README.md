# Explainer video source

The Manim source of the 27-minute explainer "How the zk-inference-prover works", made on
12 October 2026 from `../zk-prover-video-brief.md`. The rendered mp4 is not committed.

- `narration.py` — the script, one entry per scene (39 scenes, about 4,300 words).
- `common.py`, `act1.py` … `act7.py` — the scenes, one file per act, Text and shapes only
  (no LaTeX).
- `render.sh` — renders every scene in parallel: `./render.sh -qh 7` (1080p60) or `-ql` for
  a quick preview.
- `assemble.py` — adds each scene's narration and joins the scenes:
  `python3 assemble.py 1080p60 out.mp4`.
- `audio.json` — the length of each scene's narration, which the scenes pace themselves by.

To rebuild from scratch on a Mac: `uv venv --python 3.12 .venv && uv pip install manim`
(needs `brew install cairo pango pkg-config ffmpeg`), then synthesise the narration with the
system voice (`say -v Samantha -r 160 -o audio/<scene>.aiff "<text>"`, durations into
`audio.json`), then render and assemble.
