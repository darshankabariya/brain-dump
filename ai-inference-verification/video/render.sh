#!/bin/zsh
# usage: ./render.sh <quality flag: -ql|-qm|-qh> [parallel]
Q=${1:--ql}; P=${2:-8}
export PYTHONPATH=.
mkdir -p logs
python3 -c "from narration import SCENES; print('\n'.join('act%s.py %s' % (s[1], s) for s,_,_ in SCENES))" | \
  xargs -P $P -L 1 zsh -c '.venv/bin/manim '"$Q"' --disable_caching $0 $1 > logs/$1.log 2>&1 && echo "ok   $1" || echo "FAIL $1"'
