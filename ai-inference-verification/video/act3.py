import numpy as np

from common import *

FIB = [1, 1, 2, 3, 5, 8, 13, 21]
XS = np.arange(8)


def interp(ys):
    return np.polyfit(XS, ys, 7)


def P(coef, x):
    return np.polyval(coef, x)


def C(coef, x):
    return P(coef, x + 2) - P(coef, x + 1) - P(coef, x)


def tape(values, color=BLUEC, side=0.8):
    cells = VGroup()
    for v in values:
        s = Square(side_length=side, color=color, fill_color=color, fill_opacity=0.15, stroke_width=2)
        t = T(str(v), 26, WHITE).move_to(s)
        cells.add(VGroup(s, t))
    cells.arrange(RIGHT, buff=0.08)
    return cells


def tape_axes():
    ax = Axes(x_range=[-0.5, 7.8, 1], y_range=[-2, 24, 4], x_length=9.5, y_length=4.4,
              axis_config={"color": GREYC, "stroke_width": 1.5, "include_tip": False})
    return ax


class A3Tape(Base):
    act = 3
    title = "A tape and a rule"

    def build(self):
        cells = tape(FIB).move_to(UP * 0.5)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cells], lag_ratio=0.15), run_time=2.5)
        self.until(0.35)
        rule = T("rule: every cell = the two before it", 28, YEL).next_to(cells, DOWN, buff=0.8)
        self.play(Write(rule))
        self.until(0.5)
        for i in [4, 5]:
            a = CurvedArrow(cells[i].get_top(), cells[i + 2].get_top(), angle=-0.9, color=AMBER)
            b = CurvedArrow(cells[i + 1].get_top(), cells[i + 2].get_top(), angle=-0.6, color=AMBER)
            eq = T(f"{FIB[i]} + {FIB[i+1]} = {FIB[i+2]}", 24, AMBER).next_to(cells, UP, buff=1.1)
            self.play(Create(a), Create(b), FadeIn(eq))
            self.wait(1.2)
            self.play(FadeOut(a), FadeOut(b), FadeOut(eq))
        self.until(0.82)
        self.play(Write(T("a computation = a tape + a rule every hop obeys", 26, WHITE).to_edge(DOWN, buff=0.8)))


class A3Curve(Base):
    act = 3
    title = "The tape becomes a curve"

    def build(self):
        ax = tape_axes().move_to(DOWN * 0.3)
        self.play(Create(ax))
        dots = VGroup(*[Dot(ax.c2p(x, y), color=BLUEC, radius=0.08) for x, y in zip(XS, FIB)])
        labs = VGroup(*[T(str(y), 18, BLUEC).next_to(d, UP, buff=0.1) for d, y in zip(dots, FIB)])
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.1), FadeIn(labs))
        self.until(0.4)
        coef = interp(FIB)
        curve = ax.plot(lambda x: P(coef, x), x_range=[-0.3, 7.3, 0.02], color=YEL, stroke_width=3)
        self.play(Create(curve), run_time=3)
        self.until(0.7)
        lab = T("P: the unique degree-7 curve through the 8 cells", 26, YEL).to_edge(UP, buff=0.9)
        self.play(Write(lab))


class A3Rule(Base):
    act = 3
    title = "Apply the rule to the curve"

    def build(self):
        coef = interp(FIB)
        eq = T("C(x) = P(x + 2) − P(x + 1) − P(x)", 30, YEL).to_edge(UP, buff=0.9)
        self.play(Write(eq))
        self.until(0.3)
        ys = [abs(C(coef, x)) for x in np.linspace(-0.3, 5.3, 200)]
        m = max(max(ys), 1.0)
        ax = Axes(x_range=[-0.5, 5.8, 1], y_range=[-m, m, m / 2], x_length=9.5, y_length=3.6,
                  axis_config={"color": GREYC, "stroke_width": 1.5, "include_tip": False}).move_to(DOWN * 0.6)
        self.play(Create(ax))
        curve = ax.plot(lambda x: C(coef, x), x_range=[-0.3, 5.3, 0.02], color=TEALC, stroke_width=3)
        self.play(Create(curve), run_time=2.5)
        self.until(0.6)
        zeros = VGroup(*[Dot(ax.c2p(x, 0), color=GREENC, radius=0.09) for x in range(6)])
        self.play(LaggedStart(*[Flash(z, color=GREENC, flash_radius=0.3) for z in zeros], lag_ratio=0.15), FadeIn(zeros))
        self.until(0.8)
        self.play(Write(T("zero at the six hops: six facts became one curve", 24, GREENC).to_edge(DOWN, buff=0.6)))


class A3Divide(Base):
    act = 3
    title = "Division"

    def build(self):
        l1 = T("C is zero at six known points", 28, WHITE)
        l2 = T("so Z(x) = (x − 0)(x − 1)(x − 2)(x − 3)(x − 4)(x − 5) divides C", 26, GREYC)
        l3 = T("C = Z · Q        the prover computes Q", 30, YEL)
        g = VGroup(l1, l2, l3).arrange(DOWN, buff=0.35).to_edge(UP, buff=0.9)
        self.play(Write(l1))
        self.until(0.15)
        self.play(Write(l2))
        self.until(0.3)
        self.play(Write(l3))
        self.until(0.45)
        bad = list(FIB)
        bad[6] = 14
        cells = tape(bad).move_to(DOWN * 0.6)
        cells[6][0].set_color(REDC)
        cells[6][1].set_color(REDC)
        self.play(FadeIn(cells))
        self.play(Indicate(cells[6], color=REDC))
        self.until(0.62)
        calc = T("at that hop:  C = 14 − 8 − 5 = 1 ≠ 0", 28, REDC).next_to(cells, DOWN, buff=0.5)
        self.play(Write(calc))
        self.until(0.8)
        self.play(Write(T("Z no longer divides C: there is no polynomial Q at all", 26, REDC).to_edge(DOWN, buff=0.5)))


class A3Audit(Base):
    act = 3
    title = "The random audit"

    def build(self):
        coef = interp(FIB)
        ax = Axes(x_range=[-0.5, 12.5, 2], y_range=[-2, 24, 8], x_length=10.5, y_length=3.2,
                  axis_config={"color": GREYC, "stroke_width": 1.5, "include_tip": False}).move_to(DOWN * 1.0)
        dots = VGroup(*[Dot(ax.c2p(x, y), color=BLUEC, radius=0.07) for x, y in zip(XS, FIB)])
        curve = ax.plot(lambda x: min(P(coef, x), 23.5), x_range=[-0.3, 7.4, 0.02], color=YEL, stroke_width=3)
        self.play(Create(ax), FadeIn(dots), Create(curve))
        self.until(0.12)
        r = 11.3
        rl = DashedLine(ax.c2p(r, -2), ax.c2p(r, 24), color=TEALC)
        rt = T("r, far outside the tape", 22, TEALC).next_to(rl, UP, buff=0.1)
        d = die("r").next_to(rt, RIGHT, buff=0.2)
        self.play(Create(rl), FadeIn(rt), FadeIn(d))
        self.until(0.3)
        chk = T("check:  C(r) = Z(r) · Q(r)", 30, TEALC).to_edge(UP, buff=0.9)
        self.play(Write(chk))
        self.until(0.48)
        prob = lines(["two different low-degree curves agree at only a few points",
                      "a lie survives one question with probability ≈ degree / field size"], 24, GREYC, align=ORIGIN)
        prob.next_to(chk, DOWN, buff=0.3)
        self.play(FadeIn(prob))
        self.until(0.72)
        fld = lines(["field: integers mod 2^31 − 1  (Mersenne 31)", "challenges from an extension with ≈ 2^124 elements"], 24, YEL, align=ORIGIN)
        fld.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(fld))


class A3Commit(Base):
    act = 3
    title = "Commit before you are asked"

    def build(self):
        q = T("what stops the prover inventing P after it sees r?", 28, REDC).to_edge(UP, buff=0.9)
        self.play(Write(q))
        self.until(0.15)
        vals = [1, 4, 1, 5, 2, 9, 3, 7, 5, 2, 8, 6, 13, 1, 21, 4]
        g, levels = merkle(16, leaf_w=0.5, gap=0.1, level_h=0.7, leaf_labels=vals)
        g.move_to(DOWN * 0.5)
        cap = T("P evaluated on twice as many points (blowup 2), hashed pairwise", 22, GREYC).next_to(g, DOWN, buff=0.3)
        self.play(FadeIn(levels[0]), FadeIn(cap))
        self.until(0.35)
        for lv in levels[1:]:
            self.play(FadeIn(lv), run_time=0.6)
        self.play(FadeIn(g[0]))
        root = T("root: 32 bytes, published first", 24, BLUEC).next_to(levels[-1], UP, buff=0.15)
        self.play(Write(root))
        self.until(0.65)
        path = VGroup()
        idx = 5
        for lv in levels:
            path.add(lv[idx].copy().set_color(AMBER))
            idx //= 2
        self.play(FadeIn(path), run_time=1.5)
        self.until(0.82)
        self.play(Write(T("open leaf r with its hash path; change any leaf and the root changes", 22, AMBER).to_edge(DOWN, buff=0.3)))


class A3Fri(Base):
    act = 3
    title = "Low degree, by folding"

    def build(self):
        q = T("are the committed values really a low-degree curve?", 28, WHITE).to_edge(UP, buff=0.9)
        self.play(Write(q))
        self.until(0.15)
        rows = VGroup()
        n = 16
        y = 1.2
        while n >= 1:
            row = VGroup(*[Square(side_length=0.35, color=BLUEC, fill_color=BLUEC, fill_opacity=0.3, stroke_width=1) for _ in range(n)]).arrange(RIGHT, buff=0.08)
            row.move_to(UP * y)
            rows.add(row)
            y -= 0.75
            n //= 2
        self.play(FadeIn(rows[0]))
        self.until(0.3)
        for i in range(1, len(rows)):
            self.play(TransformFromCopy(rows[i - 1], rows[i]), run_time=0.7)
        lab = T("FRI: fold in half, commit, fold again, random queries at every level", 22, GREYC).next_to(rows, DOWN, buff=0.3)
        self.play(FadeIn(lab))
        self.until(0.72)
        params = lines(["blowup 2  ·  100 queries  ·  0 proof-of-work bits", "= 100 conjectured bits of security"], 24, YEL, align=ORIGIN)
        params.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(params))


class A3FiatShamir(Base):
    act = 3
    title = "Where the randomness comes from"

    def build(self):
        hb = hashbox().move_to(ORIGIN)
        self.play(FadeIn(hb))
        self.until(0.2)
        for k in range(2):
            rt = tree(BLUEC, 1.2, 0.9).next_to(hb, UP, buff=1.0)
            self.play(FadeIn(rt))
            self.play(rt.animate.move_to(hb[1].get_center()).scale(0.2), run_time=1.0)
            self.remove(rt)
            d = die(["r", "z"][k]).move_to(hb[2].get_center())
            self.play(d.animate.next_to(hb, DOWN, buff=0.8), run_time=1.0)
            self.wait(0.5)
            self.play(FadeOut(d))
        self.until(0.7)
        self.play(Write(T("the root goes in before the die comes out", 28, YEL).to_edge(DOWN, buff=0.9)))


class A3Scale(Base):
    act = 3
    title = "Scale up"

    def build(self):
        one = Rectangle(width=0.5, height=3.0, color=BLUEC, fill_color=BLUEC, fill_opacity=0.3).move_to(LEFT * 4)
        l1 = T("Fibonacci: 1 column, 1 rule", 22, GREYC).next_to(one, DOWN, buff=0.2)
        self.play(FadeIn(one), FadeIn(l1))
        self.until(0.25)
        many = VGroup(*[Rectangle(width=0.12, height=3.0, color=BLUEC, fill_color=BLUEC, fill_opacity=0.3, stroke_width=0.5) for _ in range(40)]).arrange(RIGHT, buff=0.04)
        many.move_to(RIGHT * 2)
        l2 = T("a layer segment: thousands of columns, hundreds of rules (the AIR)", 22, GREYC).next_to(many, DOWN, buff=0.2)
        self.play(TransformFromCopy(one, many), FadeIn(l2), run_time=2)
        self.until(0.55)
        cell = Square(side_length=0.12, color=YEL, fill_color=YEL, fill_opacity=1).move_to(many[12].get_center() + UP * 0.6)
        ct = T("one cell: one field element, one column, one row", 24, YEL).to_edge(UP, buff=0.9)
        self.play(FadeIn(cell), Flash(cell, color=YEL), Write(ct))
        self.until(0.8)
        self.play(Write(T("one proof here commits tens of millions of cells", 26, WHITE).to_edge(DOWN, buff=0.7)))
