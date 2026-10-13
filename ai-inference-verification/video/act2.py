from common import *

LAYER_STEPS = [
    ("norm 1", GREENC), ("requantise\n→ int8", AMBER), ("q, k, v\nmatmuls", BLUEC), ("dequantise\n→ bf16", GREENC),
    ("rotate +\nquantise", AMBER), ("attention", BLUEC), ("attn out\n→ 12-bit", AMBER), ("o matmul", BLUEC),
    ("add to\nstream", GREENC), ("norm 2", GREENC), ("requantise", AMBER), ("gate, up\nmatmuls", BLUEC),
    ("SwiGLU", GREENC), ("requantise", AMBER), ("down\nmatmul", BLUEC), ("add to\nstream", GREENC),
]


def layer_chain(scale=1.0):
    row1 = VGroup(*[box(s, 1.45, 0.85, c, 18) for s, c in LAYER_STEPS[:8]]).arrange(RIGHT, buff=0.12)
    row2 = VGroup(*[box(s, 1.45, 0.85, c, 18) for s, c in LAYER_STEPS[8:]]).arrange(RIGHT, buff=0.12)
    g = VGroup(row1, row2).arrange(DOWN, buff=0.5)
    g.scale(scale)
    return g, row1, row2


class A2Layer(Base):
    act = 2
    title = "One layer, one token"

    def build(self):
        g, row1, row2 = layer_chain(1.0)
        g.move_to(UP * 0.4)
        stream = Arrow(row1.get_left() + LEFT * 0.6, row1.get_left(), buff=0, color=GREYC)
        lab = T("residual stream →", 20, GREYC).next_to(row1, UP, buff=0.15).align_to(row1, LEFT)
        self.play(FadeIn(lab))
        fracs1 = [0.08, 0.12, 0.17, 0.22, 0.28, 0.34, 0.40, 0.44]
        for b, f in zip(row1, fracs1):
            self.until(f)
            self.play(FadeIn(b, shift=RIGHT * 0.2), run_time=0.5)
        fracs2 = [0.5, 0.54, 0.58, 0.62, 0.66, 0.7, 0.74, 0.78]
        for b, f in zip(row2, fracs2):
            self.until(f)
            self.play(FadeIn(b, shift=RIGHT * 0.2), run_time=0.5)
        self.until(0.83)
        tail = VGroup(box("× 32 layers", 2.2, 0.7, GREYC, 22), box("final norm", 2.2, 0.7, GREENC, 22),
                      box("head matmul\n→ 128,256 scores", 3.0, 0.8, BLUEC, 20), box("argmax", 1.8, 0.7, TEALC, 22))
        tail.arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.5)
        self.play(LaggedStart(*[FadeIn(t) for t in tail], lag_ratio=0.3))


class A2Fixed(Base):
    act = 2
    title = "Fixed arithmetic"

    def build(self):
        left = VGroup(T("a real GPU kernel", 28, REDC),
                      lines(["adds in an order nobody wrote down", "rounds in ways nobody specified"], 22, GREYC)).arrange(DOWN, buff=0.2)
        right = VGroup(T("the proved arithmetic", 28, GREENC),
                       lines(["int8 activations, one scale per token", "int8 weights, one scale per output channel",
                              "exact integer sums", "dequantise: a chain of correctly rounded bf16 steps",
                              "integer softmax: q 12 bits, k 11 bits,", "exp as a table → 9-bit numerator"], 22, GREYC)).arrange(DOWN, buff=0.2)
        left.to_edge(LEFT, buff=0.7).shift(UP * 1.2)
        right.to_edge(RIGHT, buff=0.7).shift(UP * 0.6)
        self.play(FadeIn(left))
        self.until(0.2)
        self.play(FadeIn(right[0]))
        for i, f in zip(right[1], [0.26, 0.31, 0.36, 0.41, 0.47, 0.52]):
            self.until(f)
            self.play(FadeIn(i, shift=RIGHT * 0.2), run_time=0.5)
        self.until(0.62)
        chart = bars([4.408, 4.715, 65.99], names=["fp32", "proved", "static int8"],
                     colors=[GREYC, GREENC, REDC], width=5.5, height=2.4, ymax=70, value_labels=True, label_fmt="{:.2f}")
        chart.to_edge(DOWN, buff=0.7).to_edge(LEFT, buff=0.8)
        cap = T("perplexity on 20,440 tokens [measured]", 20, GREYC).next_to(chart, UP, buff=0.2)
        self.play(FadeOut(left), FadeIn(chart), FadeIn(cap))
        self.until(0.8)
        self.play(Indicate(chart.bars[1], color=GREENC))


class A2Requant(Base):
    act = 2
    title = "A real requantisation"

    def build(self):
        s1 = T("max |h| over 4,096 values = 4.03125", 30, WHITE).to_edge(UP, buff=1.0)
        self.play(Write(s1))
        self.until(0.2)
        s2 = T("÷ 127 = 0.03174   →   round up to bf16   →   scale = 0.031982421875", 26, AMBER).next_to(s1, DOWN, buff=0.35)
        self.play(Write(s2))
        self.until(0.38)
        vals = ["-0.0171", "0.0201", "0.0152", "0.0093", "-0.3203", "-0.0099", "0", "0.0022"]
        ints = ["-1", "1", "0", "0", "-10", "0", "0", "0"]
        vrow = VGroup(*[box(v, 1.35, 0.6, GREYC, 20) for v in vals]).arrange(RIGHT, buff=0.1).move_to(DOWN * 0.2)
        irow = VGroup(*[box(v, 1.35, 0.6, AMBER, 22) for v in ints]).arrange(RIGHT, buff=0.1).next_to(vrow, DOWN, buff=0.7)
        self.play(FadeIn(vrow))
        arr = VGroup(*[Arrow(a.get_bottom(), b.get_top(), buff=0.05, color=GREYC, stroke_width=2) for a, b in zip(vrow, irow)])
        self.until(0.5)
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(b)) for a, b in zip(arr, irow)], lag_ratio=0.15), run_time=3)
        self.until(0.66)
        self.play(Indicate(irow[4], color=YEL), Indicate(irow[1], color=YEL))
        self.until(0.75)
        wl = T("W_q row 0:  0.00516, -0.0293, -0.00644, -0.01819, …   scale 0.00045", 22, GREYC)
        wi = T("→  11, -65, -14, -40, -7, 59, -2, -5", 24, BLUEC)
        w = VGroup(wl, wi).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(w))


class A2Witness(Base):
    act = 2
    title = "The witness"

    def build(self):
        items = lines(["int8 activations", "exact accumulators", "bf16 bit patterns", "attention scores",
                       "keys and values", "residual stream in and out"], 22, AMBER)
        items.to_edge(LEFT, buff=0.6).shift(UP * 0.3)
        disk = box("witness on disk\nper layer, per block of 512", 3.4, 1.2, AMBER, 20).next_to(items, DOWN, buff=0.4)
        self.play(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.2) for i in items], lag_ratio=0.2), run_time=2.5)
        self.play(FadeIn(disk))
        self.until(0.35)
        rms = [0.006, 0.013, 0.022, 0.031, 0.051, 0.064, 0.07, 0.086, 0.091, 0.099, 0.111, 0.116, 0.12, 0.137, 0.145,
               0.154, 0.169, 0.198, 0.221, 0.243, 0.273, 0.305, 0.343, 0.383, 0.424, 0.466, 0.512, 0.557, 0.609,
               0.671, 0.747, 0.835, 2.176]
        chart = bars(rms, colors=[GREENC] * 32 + [YEL], width=6.8, height=2.4, ymax=2.4)
        chart.to_edge(RIGHT, buff=0.5).shift(UP * 1.1)
        cap = T("residual-stream RMS, embedding then 32 layers, then final norm", 18, GREYC).next_to(chart, UP, buff=0.1)
        self.play(FadeIn(cap), Create(chart), run_time=2.5)
        self.until(0.62)
        att = bars([0.2539, 0.0083, 0.0168, 0.015, 0.1953, 0.5117], names=["<bot>", "The", "capital", "of", "France", "is"],
                   colors=[BLUEC] * 4 + [AMBER, YEL], width=6.8, height=1.7, ymax=0.6, value_labels=True, label_fmt="{:.2f}")
        att.to_edge(RIGHT, buff=0.5).to_edge(DOWN, buff=0.6)
        cap2 = T('attention of "is", layer 31 head 0 (real)', 18, GREYC).next_to(att, UP, buff=0.1)
        self.play(FadeIn(cap2), Create(att), run_time=2)
        self.until(0.85)
        self.play(Write(T("cost grows with the context", 24, YEL).next_to(disk, DOWN, buff=0.4)))
