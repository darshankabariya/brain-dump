"""Shared helpers for the explainer scenes."""
import json
import os

from manim import *

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIO = json.load(open(os.path.join(HERE, "audio.json")))

BG = "#0d1117"
AMBER = "#f0a830"      # the prover: chooses values and commits
TEALC = "#2dd4bf"      # the verifier: holds no weights, no GPU
BLUEC = "#58a6ff"      # trees, commitments
YEL = "#ffd866"        # challenges, dice
GREYC = "#8b949e"
REDC = "#ff6b6b"
GREENC = "#7ee787"
PLUM = "#c678dd"       # outside every proof

config.background_color = BG


def T(s, size=30, color=WHITE, **kw):
    return Text(s, font_size=size, color=color, **kw)


def lines(items, size=28, color=WHITE, buff=0.22, align=LEFT):
    return VGroup(*[T(s, size, color) for s in items]).arrange(DOWN, aligned_edge=align, buff=buff)


def box(label, w=2.4, h=0.8, color=BLUEC, size=24, fill=0.18, tcolor=WHITE):
    r = RoundedRectangle(corner_radius=0.12, width=w, height=h, color=color,
                         fill_color=color, fill_opacity=fill, stroke_width=2)
    t = T(label, size, tcolor)
    if t.width > w - 0.25:
        t.scale((w - 0.25) / t.width)
    t.move_to(r)
    return VGroup(r, t)


def tree(color=BLUEC, w=1.6, h=1.2, label=None, size=22):
    tri = Polygon([-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], [0, h / 2, 0],
                  color=color, fill_color=color, fill_opacity=0.18, stroke_width=2)
    root = Dot(tri.get_top(), radius=0.07, color=color)
    g = VGroup(tri, root)
    if label:
        t = T(label, size, color).next_to(tri, DOWN, buff=0.15)
        g.add(t)
    return g


def hashbox(w=2.6, h=1.4):
    r = RoundedRectangle(corner_radius=0.15, width=w, height=h, color=GREYC,
                         fill_color="#30363d", fill_opacity=0.9, stroke_width=2)
    slot = Rectangle(width=w * 0.5, height=0.12, color=GREYC, fill_color=BG, fill_opacity=1).move_to(r.get_top() + DOWN * 0.25)
    tray = Rectangle(width=w * 0.5, height=0.12, color=GREYC, fill_color=BG, fill_opacity=1).move_to(r.get_bottom() + UP * 0.25)
    lab = T("hash channel\n(Blake2s)", 20, WHITE).move_to(r)
    return VGroup(r, slot, tray, lab)


def die(label="r", color=YEL, size=0.55):
    sq = RoundedRectangle(corner_radius=0.1, width=size, height=size, color=color,
                          fill_color=color, fill_opacity=0.9, stroke_width=1)
    t = T(label, 22, BG).move_to(sq)
    return VGroup(sq, t)


def merkle(n_leaves=8, leaf_w=0.5, gap=0.12, level_h=0.75, color=BLUEC, leaf_labels=None):
    """A binary Merkle tree; returns (group, levels) where levels[0] is the leaves."""
    levels = []
    leaves = VGroup()
    for i in range(n_leaves):
        s = Square(side_length=leaf_w, color=color, fill_color=color, fill_opacity=0.25, stroke_width=1.5)
        if leaf_labels:
            t = T(str(leaf_labels[i]), 16, WHITE).move_to(s)
            if t.width > leaf_w - 0.08:
                t.scale((leaf_w - 0.08) / t.width)
            s = VGroup(s, t)
        leaves.add(s)
    leaves.arrange(RIGHT, buff=gap)
    levels.append(leaves)
    edges = VGroup()
    cur = leaves
    while len(cur) > 1:
        nxt = VGroup()
        for j in range(0, len(cur), 2):
            a, b = cur[j], cur[j + 1]
            node = Circle(radius=leaf_w * 0.32, color=color, fill_color=color, fill_opacity=0.5, stroke_width=1.5)
            node.move_to((a.get_center() + b.get_center()) / 2 + UP * level_h)
            edges.add(Line(a.get_top(), node.get_bottom(), color=GREYC, stroke_width=1.5),
                      Line(b.get_top(), node.get_bottom(), color=GREYC, stroke_width=1.5))
            nxt.add(node)
        levels.append(nxt)
        cur = nxt
    g = VGroup(edges, *levels)
    return g, levels


def bars(values, names=None, colors=None, width=6.0, height=2.4, ymax=None, ymin=0.0,
         value_labels=False, name_size=18, value_size=18, label_fmt="{:g}"):
    """A bar chart from rectangles and Text only (no LaTeX). Returns a VGroup with .bars."""
    n = len(values)
    ymax = ymax if ymax is not None else max(values) * 1.1
    colors = colors or [BLUEC] * n
    slot = width / n
    bw = slot * 0.7
    g = VGroup()
    base = Line([-width / 2, 0, 0], [width / 2, 0, 0], color=GREYC, stroke_width=1.5)
    g.add(base)
    g.bars = VGroup()
    for i, (v, c) in enumerate(zip(values, colors)):
        hh = max((v - ymin) / (ymax - ymin), 0) * height
        r = Rectangle(width=bw, height=max(hh, 0.001), color=c, fill_color=c, fill_opacity=0.75, stroke_width=1)
        r.move_to([-width / 2 + slot * (i + 0.5), hh / 2, 0])
        g.bars.add(r)
    g.add(g.bars)
    if names:
        g.names = VGroup()
        for r, nm in zip(g.bars, names):
            t = T(nm, name_size, GREYC).next_to(r, DOWN, buff=0.1)
            t.set_y(base.get_y() - 0.25)
            if t.width > slot * 0.95:
                t.scale(slot * 0.95 / t.width)
            g.names.add(t)
        g.add(g.names)
    if value_labels:
        g.values = VGroup()
        for r, v in zip(g.bars, values):
            g.values.add(T(label_fmt.format(v), value_size, WHITE).next_to(r, UP, buff=0.08))
        g.add(g.values)
    return g


def stacked_bar(parts, total_w=8.0, h=0.7, label_size=20):
    """parts: list of (label, value, color). Returns VGroup of rectangles and labels."""
    total = sum(v for _, v, _ in parts)
    g = VGroup()
    x = -total_w / 2
    for lab, v, col in parts:
        w = total_w * v / total
        r = Rectangle(width=w, height=h, color=col, fill_color=col, fill_opacity=0.75, stroke_width=1)
        r.move_to([x + w / 2, 0, 0])
        g.add(r)
        x += w
    return g


class Base(Scene):
    act = 0
    title = ""

    def construct(self):
        self.camera.background_color = BG
        name = type(self).__name__
        self.dur = AUDIO.get(name, 30.0)
        hdr = T(f"ACT {self.act}   {self.title}", 20, GREYC).to_corner(UL, buff=0.3)
        self.add(hdr)
        self.build()
        self.until(1.0)
        self.wait(0.8)

    def now(self):
        return self.renderer.time

    def until(self, frac):
        gap = frac * self.dur - self.now()
        if gap > 0.05:
            self.wait(gap)

    def build(self):
        raise NotImplementedError
