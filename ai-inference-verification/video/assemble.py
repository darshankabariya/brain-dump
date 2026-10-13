"""Mux each scene's narration onto its rendered video, then concatenate all scenes.

usage: python3 assemble.py <quality dir, e.g. 1080p60> <output mp4>
"""
import json
import os
import subprocess
import sys

from narration import SCENES

qdir = sys.argv[1]
out = sys.argv[2]
os.makedirs("av", exist_ok=True)
aud = json.load(open("audio.json"))
parts = []
for sid, act, _ in SCENES:
    video = f"media/videos/act{act}/{qdir}/{sid}.mp4"
    audio = f"audio/{sid}.aiff"
    target = f"av/{sid}.mp4"
    if not os.path.exists(video):
        raise SystemExit(f"missing {video}")
    # the video is always longer than the narration (the scene waits for it), so pad the
    # audio with silence and cut at the video's length
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-i", audio,
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-ar", "44100",
                    "-af", "apad", "-shortest", "-movflags", "+faststart", target], check=True)
    parts.append(target)
    print("muxed", sid)
with open("av/list.txt", "w") as f:
    for p in parts:
        f.write(f"file '{os.path.abspath(p)}'\n")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "av/list.txt",
                "-c", "copy", "-movflags", "+faststart", out], check=True)
d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out],
                   capture_output=True, text=True).stdout.strip()
print("wrote", out, "duration", float(d) / 60, "min", os.path.getsize(out) / 1e6, "MB")
