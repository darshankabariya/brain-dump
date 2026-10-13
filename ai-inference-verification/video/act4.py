from common import *


def grid_tiles(rows=32, cols=9, side=0.16, gap=0.03, color=AMBER):
    g = VGroup()
    for r in range(rows):
        row = VGroup(*[Square(side_length=side, color=color, fill_color=color, fill_opacity=0.35, stroke_width=0.5) for _ in range(cols)]).arrange(RIGHT, buff=gap)
        g.add(row)
    g.arrange(UP, buff=gap)
    return g


class A4Segment(Base):
    act = 4
    title = "The unit of proof"

    def build(self):
        seg = box("one layer\n× 512 positions\n(+ context C)", 3.2, 1.6, AMBER, 24).move_to(LEFT * 3.5)
        lab = T("a segment = one STARK proof", 26, AMBER).next_to(seg, DOWN, buff=0.3)
        self.play(FadeIn(seg), Write(lab))
        self.until(0.3)
        g = grid_tiles(32, 9, side=0.12, gap=0.025).move_to(RIGHT * 3 + DOWN * 0.3)
        heads = VGroup(*[Square(side_length=0.12, color=TEALC, fill_color=TEALC, fill_opacity=0.5, stroke_width=0.5) for _ in range(2)])
        heads[0].next_to(g[-1][7], UP, buff=0.03)
        heads[1].next_to(g[-1][8], UP, buff=0.03)
        xl = T("9 token blocks →", 18, GREYC).next_to(g, DOWN, buff=0.1)
        yl = T("32 layers ↑", 18, GREYC).rotate(PI / 2).next_to(g, LEFT, buff=0.15)
        self.play(TransformFromCopy(seg, g), FadeIn(xl), FadeIn(yl), run_time=2.5)
        self.play(FadeIn(heads))
        self.until(0.62)
        n = T("9 × 32 + 2 = 290 proofs  [measured]", 28, WHITE).to_edge(UP, buff=0.9)
        self.play(Write(n))
        self.until(0.8)
        self.play(Write(T("no recursion: the proofs are chained, act 6", 24, GREYC).to_edge(DOWN, buff=0.4).to_edge(LEFT, buff=0.8)))


class A4Trees(Base):
    act = 4
    title = "Five kinds of tree"

    def build(self):
        specs = [("tree 0\nshape", TEALC, "selectors, masks,\nlookup tables, angles\n— verifier rebuilds it"),
                 ("tree 1\nmodel", BLUEC, "int8 weights, scales\n— publisher's root"),
                 ("tree 2\nbase trace", AMBER, "everything the\nprover chose\n— most cells"),
                 ("tree 3\ninteraction", AMBER, "lookup bookkeeping\n— after challenges"),
                 ("trees 4+\nboundary", AMBER, "stream in / out,\nkeys and values\n— compared with\na neighbour")]
        cols = VGroup()
        for name, col, desc in specs:
            tr = tree(col, 1.7, 1.3)
            nm = T(name, 22, col)
            ds = T(desc, 17, GREYC)
            cols.add(VGroup(tr, nm, ds).arrange(DOWN, buff=0.2))
        cols.arrange(RIGHT, buff=0.35, aligned_edge=UP).move_to(DOWN * 0.3)
        for c, f in zip(cols, [0.06, 0.32, 0.48, 0.66, 0.8]):
            self.until(f)
            self.play(FadeIn(c, shift=UP * 0.3))


class A4Transcript(Base):
    act = 4
    title = "The transcript of one segment"

    def build(self):
        hb = hashbox(2.4, 1.3).to_edge(RIGHT, buff=0.8).shift(UP * 1.5)
        self.add(hb)
        steps = ["1  commit trees 0, 1, 2; mix each root into the channel",
                 "2  draw challenges: (z, α) per table, fold weights r, s, rv, binding w",
                 "3  build lookup fractions; 5 GKR sumchecks; commit tree 3",
                 "4  commit the boundary trees",
                 "5  STARK: out-of-domain point, quotients (CUDA kernels),",
                 "    composition polynomial, FRI",
                 "6  write Fixed (statement), Claims (sums), Proof (~65 MiB)"]
        g = lines(steps, 22, WHITE, buff=0.28).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        fr = [0.04, 0.2, 0.36, 0.5, 0.58, 0.66, 0.82]
        for s, f in zip(g, fr):
            self.until(f)
            self.play(FadeIn(s, shift=RIGHT * 0.2), run_time=0.6)
            if s is g[0]:
                for _ in range(3):
                    r = Dot(color=BLUEC, radius=0.1).next_to(s, RIGHT, buff=0.2)
                    self.play(r.animate.move_to(hb[1].get_center()), run_time=0.5)
                    self.remove(r)
            if s is g[1]:
                for lab in ["z", "r", "w"]:
                    d = die(lab).move_to(hb[2].get_center())
                    self.play(d.animate.next_to(hb, DOWN, buff=0.3 + 0.0), run_time=0.5)
                    self.play(FadeOut(d), run_time=0.2)


class A4Order(Base):
    act = 4
    title = "Why the order is the argument"

    def build(self):
        hb = hashbox(2.4, 1.3).move_to(UP * 1.2)
        self.add(hb)
        d = die("r").next_to(hb, DOWN, buff=0.6)
        rt = tree(AMBER, 1.2, 0.9).next_to(d, DOWN, buff=0.5)
        bad = T("die first, then values chosen to pass it", 24, REDC).next_to(rt, DOWN, buff=0.3)
        self.play(FadeIn(d))
        self.play(FadeIn(rt), Write(bad))
        cross = Cross(VGroup(d, rt), stroke_color=REDC, stroke_width=6)
        self.until(0.3)
        self.play(Create(cross))
        self.until(0.42)
        self.play(FadeOut(cross), FadeOut(d), FadeOut(rt), FadeOut(bad))
        rt2 = tree(AMBER, 1.2, 0.9).next_to(hb, UP, buff=0.5)
        self.play(FadeIn(rt2))
        self.play(rt2.animate.move_to(hb[1].get_center()).scale(0.2), run_time=0.8)
        self.remove(rt2)
        d2 = die("r").move_to(hb[2].get_center())
        self.play(d2.animate.next_to(hb, DOWN, buff=0.6), run_time=0.8)
        good = T("root in, then the die out", 24, GREENC).next_to(d2, DOWN, buff=0.3)
        self.play(Write(good))
        self.until(0.7)
        gate = lines(["the byte order of the proof is load-bearing", "digest gate: SHA-256 of the proof bytes must match",
                      "on the CPU backend and the GPU backend before a merge"], 24, YEL, align=ORIGIN).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(gate))


class A4Bf16(Base):
    act = 4
    title = "A float as two cells"

    def build(self):
        why = T("blowup 2  ⇒  every rule must stay low degree", 26, GREYC).to_edge(UP, buff=0.9)
        self.play(Write(why))
        self.until(0.25)
        sm = box("sm\nsigned significand\n0 or ±[128, 256)", 3.6, 1.5, AMBER, 22)
        ef = box("ef\nexponent field\n[1, 255)", 3.0, 1.5, BLUEC, 22)
        pair = VGroup(sm, ef).arrange(RIGHT, buff=0.5).move_to(UP * 0.2)
        self.play(FadeIn(pair))
        self.until(0.5)
        val = T("value = sm · 2^(ef − 134)", 32, WHITE).next_to(pair, DOWN, buff=0.5)
        self.play(Write(val))
        self.until(0.68)
        ex = lines(["1.5 = 192 · 2^(127 − 134) = 192 / 128", "zero: sm = 0, nothing else to check"], 26, YEL, align=ORIGIN).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(ex))


class A4Cells(Base):
    act = 4
    title = "How much is committed"

    def build(self):
        head = T("fresh cells per proved position, context 4,096 [measured]", 24, GREYC).to_edge(UP, buff=0.9)
        self.play(FadeIn(head))
        parts = [("base trace 58.5M", 58.5, AMBER), ("interaction 17.8M", 17.8, AMBER), ("boundary 2.6M", 2.6, GREENC)]
        bar = stacked_bar(parts, total_w=9.0, h=0.8).move_to(UP * 0.8)
        labs = VGroup(T("base trace  58.5M", 22, AMBER), T("interaction  17.8M", 22, AMBER), T("boundary  2.6M", 22, GREENC)).arrange(RIGHT, buff=0.6).next_to(bar, DOWN, buff=0.2)
        bar[1].set_fill(opacity=0.5)
        for p, f in zip(bar, [0.1, 0.2, 0.28]):
            self.until(f)
            self.play(FadeIn(p), run_time=0.5)
        self.play(FadeIn(labs))
        tot = T("≈ 79.0M fresh cells per position", 28, WHITE).next_to(labs, DOWN, buff=0.3)
        self.until(0.38)
        self.play(Write(tot))
        self.until(0.55)
        pre = lines(["preprocessed and cached, not paid per segment:", "model 22.9M   ·   shape 4.5M"], 24, BLUEC, align=ORIGIN).next_to(tot, DOWN, buff=0.4)
        self.play(FadeIn(pre))
        self.until(0.8)
        self.play(Write(T("context 16,384: ≈ 105M fresh cells per position", 26, YEL).to_edge(DOWN, buff=0.5)))
