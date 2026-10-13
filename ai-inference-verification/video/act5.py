from common import *


def matrix(rows, color=WHITE, size=28):
    cells = VGroup()
    for r in rows:
        row = VGroup(*[T(str(v), size, color) for v in r]).arrange(RIGHT, buff=0.4)
        cells.add(row)
    cells.arrange(DOWN, buff=0.25)
    br = SurroundingRectangle(cells, color=GREYC, buff=0.2, stroke_width=1.5)
    return VGroup(br, cells)


class A5Freivalds(Base):
    act = 5
    title = "Trick 1: matmuls by Freivalds"

    def build(self):
        prob = T("7 matmuls, 218M weights per layer: a rule per output cell is hopeless", 24, GREYC).to_edge(UP, buff=0.9)
        self.play(FadeIn(prob))
        self.until(0.18)
        W = matrix([[1, 2], [3, 4]])
        X = matrix([[1], [1]])
        Y = matrix([[3], [7]], GREENC)
        Yp = matrix([[3], [8]], REDC)
        eq = VGroup(T("W", 26, GREYC), W, T("×", 30), X, T("=", 30), Y).arrange(RIGHT, buff=0.3).move_to(UP * 0.6)
        self.play(FadeIn(eq))
        self.until(0.32)
        claim = VGroup(T("prover claims", 24, REDC), Yp).arrange(RIGHT, buff=0.3).next_to(eq, RIGHT, buff=0.8)
        self.play(FadeIn(claim))
        self.until(0.45)
        d = die("r")
        rl = VGroup(d, T("random r = (r1, r2), drawn after the claim", 24, YEL)).arrange(RIGHT, buff=0.3).next_to(eq, DOWN, buff=0.5)
        self.play(FadeIn(rl))
        self.until(0.58)
        left = T("r · Y'  =  3 r1 + 8 r2", 28, REDC)
        right = T("(r W) · X  =  3 r1 + 7 r2", 28, GREENC)
        chk = VGroup(left, right).arrange(DOWN, buff=0.25).next_to(rl, DOWN, buff=0.4)
        self.play(Write(left))
        self.until(0.72)
        self.play(Write(right))
        self.until(0.84)
        self.play(Write(T("they differ by r2: a random r2 is zero with probability 1 / p", 26, YEL).to_edge(DOWN, buff=0.4)))


class A5FreivaldsGeneral(Base):
    act = 5
    title = "Freivalds, in the code"

    def build(self):
        idn = T("rᵀ (W X)  =  (rᵀ W) X     at a random r", 34, WHITE).to_edge(UP, buff=0.9)
        self.play(Write(idn))
        self.until(0.2)
        cost = lines(["one pass over the weights: linear, not cubic", "a wrong product survives with probability ≈ degree / 2^124"], 24, GREYC, align=ORIGIN).next_to(idn, DOWN, buff=0.3)
        self.play(FadeIn(cost))
        self.until(0.4)
        fg = box("Freivalds gadget\nfolds inputs × weights\n→ acc_m", 3.4, 1.5, AMBER, 22)
        dg = box("dequant gadget\nfolds the same committed\naccumulators → h_m", 3.4, 1.5, AMBER, 22)
        pair = VGroup(fg, dg).arrange(RIGHT, buff=2.8).move_to(DOWN * 0.4)
        eq = T("acc_m = h_m", 30, TEALC).move_to(pair.get_center())
        self.play(FadeIn(fg))
        self.until(0.55)
        self.play(FadeIn(dg))
        self.until(0.66)
        self.play(Write(eq))
        self.until(0.8)
        wt = VGroup(tree(BLUEC, 1.2, 0.9), T("weights from tree 1: the committed model, no other", 22, BLUEC)).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(wt))


class A5LogUp(Base):
    act = 5
    title = "Trick 2: lookups by LogUp"

    def build(self):
        qs = lines(["is this float correctly rounded?", "is this numerator exp(score)?", "is this value below 2^15?"], 22, GREYC)
        qs.to_edge(LEFT, buff=0.6).to_edge(UP, buff=1.0)
        self.play(FadeIn(qs))
        self.until(0.15)
        ans = T("each is a table membership: my row must be a row of a committed table", 22, YEL).next_to(qs, DOWN, buff=0.3).align_to(qs, LEFT)
        self.play(Write(ans))
        self.until(0.27)
        tbl = VGroup(T("table", 22, BLUEC), *[box(str(v), 0.7, 0.55, BLUEC, 22) for v in [1, 2, 3]]).arrange(RIGHT, buff=0.15)
        uses = VGroup(T("uses", 22, AMBER), *[box(str(v), 0.7, 0.55, AMBER, 22) for v in [2, 2, 3]]).arrange(RIGHT, buff=0.15)
        mult = VGroup(T("multiplicity", 22, GREENC), *[box(str(v), 0.7, 0.55, GREENC, 22) for v in [0, 2, 1]]).arrange(RIGHT, buff=0.15)
        g = VGroup(tbl, uses, mult).arrange(DOWN, buff=0.25, aligned_edge=RIGHT).to_edge(RIGHT, buff=0.8).shift(UP * 1.2)
        self.play(FadeIn(tbl))
        self.until(0.36)
        self.play(FadeIn(uses))
        self.play(FadeIn(mult))
        self.until(0.5)
        d = die("z").next_to(g, DOWN, buff=0.3)
        self.play(FadeIn(d))
        fu = T("uses:   1/(z−2) + 1/(z−2) + 1/(z−3)", 26, AMBER)
        ft = T("table:  2/(z−2) + 1/(z−3)", 26, BLUEC)
        fr = VGroup(fu, ft).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(DOWN * 1.0)
        self.until(0.56)
        self.play(Write(fu))
        self.until(0.66)
        self.play(Write(ft))
        eqt = T("equal for every z", 24, GREENC).next_to(fr, RIGHT, buff=0.5)
        self.play(FadeIn(eqt))
        self.until(0.78)
        cheat = T("cheat with a 4:  + 1/(z−4)   a pole nothing in the table can cancel", 24, REDC).to_edge(DOWN, buff=0.7)
        self.play(Write(cheat))
        self.until(0.92)
        self.play(FadeIn(T("the running sums of these fractions are the interaction tree", 22, GREYC).to_edge(DOWN, buff=0.25)))


class A5Tables(Base):
    act = 5
    title = "The tables"

    def build(self):
        rule = lines(["multi-column rows fold into one number with a second challenge α",
                      "cost: 1 multiplicity cell + 1 extension-field fraction (4 cells)",
                      "= 5 cells per table row, used or not"], 24, YEL, align=ORIGIN).to_edge(UP, buff=0.9)
        self.play(FadeIn(rule))
        self.until(0.3)
        rows = [("NORM, FRAC", "correctly rounded bf16: |acc| = M2·2^k + r"),
                ("rsqrt, silu", "all 65,536 bf16 inputs with rounded outputs"),
                ("exp", "integer softmax: shifted score → 9-bit numerator"),
                ("range tables", "int8 activations, 15-bit comparisons, remainders"),
                ("embedding", "128,256 × 4,096 rows in tree 1, one pass per lookup")]
        g = VGroup()
        for name, desc in rows:
            g.add(VGroup(box(name, 2.6, 0.55, BLUEC, 20), T(desc, 20, GREYC)).arrange(RIGHT, buff=0.3))
        g.arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to(DOWN * 0.8)
        for r, f in zip(g, [0.36, 0.5, 0.6, 0.68, 0.8]):
            self.until(f)
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.6)


class A5Gkr(Base):
    act = 5
    title = "The biggest optimisation"

    def build(self):
        t = lines(["for the five largest lookup families, the running sums", "are not committed: a sumcheck (GKR) proves them,",
                   "and a link ties its final claim to the committed columns"], 26, WHITE, align=ORIGIN).to_edge(UP, buff=0.9)
        self.play(FadeIn(t))
        self.until(0.35)
        big = Rectangle(width=8.0, height=0.7, color=AMBER, fill_color=AMBER, fill_opacity=0.5)
        small = Rectangle(width=8.0 * 5600 / 93184, height=0.7, color=GREENC, fill_color=GREENC, fill_opacity=0.7)
        bl = T("93,184 columns", 24, AMBER)
        sl = T("5,600 columns", 24, GREENC)
        g = VGroup(VGroup(big, bl).arrange(RIGHT, buff=0.3), VGroup(small, sl).arrange(RIGHT, buff=0.3)).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(DOWN * 0.3)
        self.play(FadeIn(g[0]))
        self.until(0.55)
        self.play(TransformFromCopy(big, small), FadeIn(sl))
        self.until(0.75)
        self.play(Write(T("41.8 % of proving time [measured]: the largest phase", 26, YEL).to_edge(DOWN, buff=0.6)))


class A5Seams(Base):
    act = 5
    title = "Trick 3: seams and bindings"

    def build(self):
        a = box("gadget A\n(producer)", 2.8, 1.1, AMBER, 22)
        b = box("gadget B\n(consumer)", 2.8, 1.1, AMBER, 22)
        pair = VGroup(a, b).arrange(RIGHT, buff=3.0).move_to(UP * 0.8)
        self.play(FadeIn(pair))
        self.until(0.2)
        d = die("w").move_to(pair.get_center() + UP * 1.2)
        self.play(FadeIn(d))
        ha = T("Σ w^(N−1−q) · out_q", 24, AMBER).next_to(a, DOWN, buff=0.3)
        hb = T("Σ w^(N−1−q) · in_q", 24, AMBER).next_to(b, DOWN, buff=0.3)
        self.until(0.4)
        self.play(Write(ha), Write(hb))
        eq = T("=", 36, TEALC).move_to((ha.get_center() + hb.get_center()) / 2)
        self.until(0.55)
        self.play(Write(eq))
        note = T("equal sums under a random weight ⇒ equal sequences, position by position", 22, GREYC).next_to(VGroup(ha, hb), DOWN, buff=0.4)
        self.play(FadeIn(note))
        self.until(0.75)
        seam = VGroup(box("bf16\nproducer", 2.2, 0.9, GREENC, 20), box("SEAM\nrequantise", 2.2, 0.9, YEL, 20), box("int8\nmatmul", 2.2, 0.9, BLUEC, 20)).arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(seam))


class A5Edges(Base):
    act = 5
    title = "The 16 edges"

    def build(self):
        groups = [("residual-stream bindings", 7, AMBER), ("seams", 3, YEL), ("attention itself", 1, BLUEC),
                  ("Freivalds itself", 1, BLUEC), ("boundaries", 2, GREENC), ("embedding (layer 0)", 1, TEALC), ("argmax (head)", 1, TEALC)]
        locks = VGroup()
        legend = VGroup()
        for name, n, col in groups:
            for _ in range(n):
                locks.add(Circle(radius=0.22, color=col, fill_color=col, fill_opacity=0.5, stroke_width=1.5))
            legend.add(VGroup(Dot(color=col, radius=0.1), T(f"{name}: {n}", 22, col)).arrange(RIGHT, buff=0.2))
        locks.arrange(RIGHT, buff=0.15).move_to(UP * 1.6)
        for i, l in enumerate(locks):
            l.add(T(str(i + 1), 16, WHITE).move_to(l))
        legend.arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to(DOWN * 0.6)
        idx = 0
        for (name, n, col), lg, f in zip(groups, legend, [0.05, 0.3, 0.42, 0.5, 0.58, 0.68, 0.72]):
            self.until(f)
            self.play(FadeIn(locks[idx:idx + n]), FadeIn(lg), run_time=0.6)
            idx += n
        self.until(0.82)
        off = T("--unsound-skip: one edge off, loudly → a control, never a result", 24, REDC).to_edge(DOWN, buff=0.5)
        self.play(locks[4].animate.set_fill(opacity=0.05).set_stroke(REDC), Write(off))


class A5Argmax(Base):
    act = 5
    title = "The argmax edge"

    def build(self):
        tie = T("ties are real: 15 of 512 positions had equal top scores", 24, GREYC).to_edge(UP, buff=0.9)
        self.play(FadeIn(tie))
        vals = [3, 7, 9, 9, 4, 9, 2]
        chart = bars(vals, names=[str(i) for i in range(7)], colors=[GREYC, GREYC, YEL, GREYC, GREYC, GREYC, GREYC],
                     width=6.0, height=2.2, ymax=10, value_labels=True).move_to(LEFT * 3 + DOWN * 0.3)
        self.until(0.15)
        self.play(Create(chart))
        tok = T("token = 2, the first maximum", 22, YEL).next_to(chart, DOWN, buff=0.2)
        self.play(FadeIn(tok))
        self.until(0.3)
        brow = VGroup(T("b:", 22, TEALC), *[box(str(v), 0.5, 0.5, TEALC, 20) for v in [1, 1, 0, 0, 0, 0, 0]]).arrange(RIGHT, buff=0.1).move_to(RIGHT * 3 + UP * 0.9)
        self.play(FadeIn(brow))
        self.until(0.45)
        rules = lines(["range check: pm − k_i − b_i ≥ 0", "  b = 1: strictly below the max", "  b = 0: at most the max",
                       "b ∈ {0, 1}, never increases", "Σ b_i = token  (the binding)"], 22, WHITE).next_to(brow, DOWN, buff=0.3).align_to(brow, LEFT)
        for r, f in zip(rules, [0.5, 0.56, 0.62, 0.7, 0.78]):
            self.until(f)
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.5)
        self.until(0.88)
        self.play(Write(T("the lax form (\"attains the max\") is a flagged control only", 22, REDC).to_edge(DOWN, buff=0.35)))
