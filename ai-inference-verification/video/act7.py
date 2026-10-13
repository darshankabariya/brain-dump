from common import *


class A7Numbers(Base):
    act = 7
    title = "The numbers"

    def build(self):
        head = T("one request, one H100: 4,096 prompt + 512 generated", 24, GREYC).to_edge(UP, buff=0.9)
        self.play(FadeIn(head))
        rows = [("segments", "290", "measured"), ("proving loop", "3,683 s (61 min)", "measured"),
                ("whole run", "5,485 s (91 min)", "measured"), ("throughput", "1.25 positions / s", "derived"),
                ("cost at 3.29 USD / GPU-h", "3.37 to 5.01 USD per request", "derived"),
                ("unproved vLLM, end to end", "1,342 positions / s  (≈ 1,000×)", "measured"),
                ("proof size", "18.46 GiB, ≈ 65 MiB per segment", "measured"),
                ("context 16,384", "1,058 segments, 6.0 h loop, 108.9 GiB", "measured")]
        g = VGroup()
        for k, v, gr in rows:
            g.add(VGroup(T(k, 22, GREYC), T(v, 24, WHITE), T(gr, 18, TEALC)).arrange(RIGHT, buff=0.5))
        g.arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(DOWN * 0.3)
        kx = max(r[0].get_right()[0] for r in g) + 0.5
        for r in g:
            r[1].align_to([kx, 0, 0], LEFT)
        vx = max(r[1].get_right()[0] for r in g) + 0.5
        for r in g:
            r[2].align_to([vx, 0, 0], LEFT)
        g.move_to(DOWN * 0.3)
        fr = [0.1, 0.18, 0.26, 0.34, 0.44, 0.56, 0.68, 0.8]
        for r, f in zip(g, fr):
            self.until(f)
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.5)


class A7Time(Base):
    act = 7
    title = "Where the time goes"

    def build(self):
        head = T("serial loop over 32 layer segments, 748 s [measured]", 24, GREYC).to_edge(UP, buff=0.9)
        self.play(FadeIn(head))
        parts = [("lookups + GKR 41.8 %", 41.8, AMBER), ("base trace 35.4 %", 35.4, "#d9962b"), ("load, decode 11.8 %", 11.8, GREYC),
                 ("other host 6.4 %", 6.4, "#6e7681"), ("STARK 4.6 %", 4.6, TEALC)]
        bar = stacked_bar(parts, total_w=10.0, h=0.9).move_to(UP * 0.9)
        labs = VGroup(*[T(n, 18, c if c not in ("#d9962b", "#6e7681") else WHITE) for n, _, c in parts]).arrange(RIGHT, buff=0.35).next_to(bar, DOWN, buff=0.2)
        for p, f in zip(bar, [0.1, 0.2, 0.28, 0.34, 0.4]):
            self.until(f)
            self.play(FadeIn(p), run_time=0.4)
        self.play(FadeIn(labs))
        self.until(0.5)
        msg = lines(["the cryptography is the cheap part; building the tables on the host is the ceiling",
                     "constraint kernels on the GPU already: on the CPU the same loop took 4,737 s"], 22, WHITE, align=ORIGIN).next_to(labs, DOWN, buff=0.4)
        self.play(FadeIn(msg))
        self.until(0.75)
        proj = lines(["projected, from the cost model, not measured:", "70B ≈ 5 to 8 h per request   ·   405B ≈ 16 to 24 h"], 24, "#8a7a40", align=ORIGIN).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(proj))


class A7Honesty(Base):
    act = 7
    title = "Seven things this proof is not"

    def build(self):
        items = ["1  not hiding: only the weights, behind their root",
                 "2  not the served model: a quantised stand-in, +6.96 % perplexity",
                 "3  greedy only: sampling and early stop are outside",
                 "4  ids, not text: the tokeniser is unproved",
                 "5  no binding to traffic: ids map to ids under a commitment",
                 "6  not formally verified: digest gate, negative controls, self-tests",
                 "7  a measurement tool: \"not something anyone should rely on yet\""]
        g = lines(items, 24, WHITE, buff=0.3).move_to(DOWN * 0.1)
        fr = [0.08, 0.2, 0.32, 0.42, 0.52, 0.66, 0.8]
        for it, f in zip(g, fr):
            self.until(f)
            self.play(FadeIn(it, shift=RIGHT * 0.2), run_time=0.5)


class A7Next(Base):
    act = 7
    title = "What is next"

    def build(self):
        items = ["witness generation on the GPU", "real 70B and 405B runs", "close the gap to real serving: float arithmetic, tokenisation, batching, traffic",
                 "prove a random sample of segments after the roots are committed"]
        g = lines(items, 24, WHITE, buff=0.25).to_edge(UP, buff=1.0)
        for it, f in zip(g, [0.05, 0.12, 0.2, 0.3]):
            self.until(f)
            self.play(FadeIn(it, shift=RIGHT * 0.2), run_time=0.5)
        self.until(0.4)
        samp = T("prove 1 % of requests: (0.99)^m < 1 % after m ≈ 460 cheats", 24, YEL).next_to(g, DOWN, buff=0.4)
        self.play(Write(samp))
        self.until(0.6)
        stmt = lines(["For these published prompt ids,", "under the model whose weight commitment is this root,",
                      "greedy decoding in this fixed arithmetic", "produces these 512 ids."], 28, TEALC, align=ORIGIN).to_edge(DOWN, buff=0.7)
        self.play(FadeOut(g), FadeOut(samp))
        self.play(Write(stmt), run_time=4)
