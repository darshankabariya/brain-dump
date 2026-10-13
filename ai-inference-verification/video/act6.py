from common import *
from act4 import grid_tiles


class A6Grid(Base):
    act = 6
    title = "The grid"

    def build(self):
        g = grid_tiles(32, 9, side=0.17, gap=0.03).move_to(LEFT * 3 + DOWN * 0.2)
        heads = VGroup(*[Square(side_length=0.17, color=TEALC, fill_color=TEALC, fill_opacity=0.6, stroke_width=0.5) for _ in range(2)])
        heads[0].next_to(g[-1][7], UP, buff=0.03)
        heads[1].next_to(g[-1][8], UP, buff=0.03)
        xl = T("blocks B0 … B8", 18, GREYC).next_to(g, DOWN, buff=0.12)
        yl = T("layers L0 … L31", 18, GREYC).rotate(PI / 2).next_to(g, LEFT, buff=0.12)
        self.play(FadeIn(g), FadeIn(xl), FadeIn(yl))
        self.until(0.12)
        self.play(FadeIn(heads), Indicate(heads, color=TEALC))
        self.until(0.3)
        va = VGroup(*[Arrow(g[r][c].get_center(), g[r + 1][c].get_center(), buff=0.02, color=AMBER, stroke_width=2, max_tip_length_to_length_ratio=0.5)
                      for r in range(0, 31, 4) for c in [1, 4, 7]])
        vt = lines(["vertical: residual-stream root out = root in above", "281 layer links"], 24, AMBER).to_edge(RIGHT, buff=0.6).shift(UP * 1.6)
        self.play(FadeIn(va), FadeIn(vt))
        self.until(0.52)
        ha = VGroup(*[Arrow(g[r][c].get_center(), g[r][c + 1].get_center(), buff=0.02, color=GREENC, stroke_width=2, max_tip_length_to_length_ratio=0.5)
                      for r in [2, 10, 18, 26] for c in range(0, 8, 2)])
        ht = lines(["horizontal: keys and values written = prefix attended", "256 token links"], 24, GREENC).next_to(vt, DOWN, buff=0.5).align_to(vt, LEFT)
        self.play(FadeIn(ha), FadeIn(ht))
        self.until(0.75)
        tot = lines(["537 links in all [measured]", "layer 0 binds the embedding row", "the head binds the emitted id"], 24, WHITE).next_to(ht, DOWN, buff=0.5).align_to(vt, LEFT)
        self.play(FadeIn(tot))


class A6Roots(Base):
    act = 6
    title = "Why a root and not a challenge"

    def build(self):
        a = box("tile k\nchallenge w_k", 2.8, 1.2, AMBER, 22)
        b = box("tile k+1\nchallenge w_k+1", 2.8, 1.2, AMBER, 22)
        pair = VGroup(a, b).arrange(RIGHT, buff=2.5).move_to(UP * 1.4)
        self.play(FadeIn(pair))
        self.until(0.15)
        bad1 = T("claims under different challenges cannot be compared", 24, GREYC).next_to(pair, DOWN, buff=0.3)
        self.play(Write(bad1))
        self.until(0.32)
        bad2 = lines(["share a public challenge?  unsound:", "a challenge known before commitment makes", "\"my image equals yours\" one linear equation to solve"], 24, REDC, align=ORIGIN).next_to(bad1, DOWN, buff=0.4)
        self.play(FadeIn(bad2))
        self.until(0.6)
        self.play(FadeOut(bad1), FadeOut(bad2))
        ta = tree(GREENC, 1.2, 0.9, "root out").next_to(a, DOWN, buff=0.4)
        tb = tree(GREENC, 1.2, 0.9, "root in").next_to(b, DOWN, buff=0.4)
        eq = T("=", 40, TEALC).move_to((ta.get_center() + tb.get_center()) / 2)
        self.play(FadeIn(ta), FadeIn(tb))
        self.play(Write(eq))
        self.until(0.82)
        self.play(FadeIn(lines(["bound to the table by a plain equality rule", "link check: 5 integer comparisons, then one 32-byte comparison", "constant time, no recursion anywhere"], 22, WHITE, align=ORIGIN).to_edge(DOWN, buff=0.3)))


class A6Verifier(Base):
    act = 6
    title = "What the verifier does"

    def build(self):
        items = ["parse Fixed, Claims, Proof; refuse on shape or security drift",
                 "replay the hash channel, redraw every challenge",
                 "verify the GKR sumchecks",
                 "STARK verifier: out-of-domain sampling and FRI",
                 "every lookup's fractions cancel",
                 "every Freivalds equality, attention identity, binding equality",
                 "rebuild the shape tree, compare its root",
                 "compare the model root with the published manifest",
                 "then the grid: every link, every id chained to the prompt or an argmax"]
        g = lines(items, 22, WHITE, buff=0.2).move_to(DOWN * 0.2).to_edge(LEFT, buff=1.2)
        fr = [0.06, 0.18, 0.28, 0.36, 0.48, 0.58, 0.68, 0.76, 0.86]
        for it, f in zip(g, fr):
            self.until(f)
            tick = T("✓", 24, GREENC).next_to(it, LEFT, buff=0.25)
            self.play(FadeIn(it, shift=RIGHT * 0.2), FadeIn(tick), run_time=0.5)


class A6Cost(Base):
    act = 6
    title = "What verification costs"

    def build(self):
        a = lines(["run host, CPU cores, 290 proofs:", "119 s total  ·  median 0.41 s per segment  [measured]"], 26, TEALC, align=ORIGIN).to_edge(UP, buff=1.0)
        self.play(FadeIn(a))
        self.until(0.3)
        parts = [("shape tree 42.25 s", 42.25, BLUEC), ("proof 0.92 s", 0.92, GREENC)]
        bar = stacked_bar(parts, total_w=9.0, h=0.8).move_to(DOWN * 0.2)
        l1 = T("consumer machine, 4 cores, no card, one segment at context 16,384: 43.2 s", 22, GREYC).next_to(bar, UP, buff=0.25)
        l2 = VGroup(T("rebuilding the shape tree: 42.25 s", 22, BLUEC), T("checking the proof: 0.92 s", 22, GREENC)).arrange(RIGHT, buff=0.8).next_to(bar, DOWN, buff=0.25)
        self.play(FadeIn(l1), FadeIn(bar), FadeIn(l2))
        self.until(0.6)
        self.play(FadeIn(T("peak memory 28.5 GiB [measured]", 22, GREYC).next_to(l2, DOWN, buff=0.3)))
        self.until(0.8)
        self.play(Write(T("a grid pays the shape tree once per (layer, context) shape, not per proof", 24, YEL).to_edge(DOWN, buff=0.5)))
