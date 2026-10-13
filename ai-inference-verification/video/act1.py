from common import *


class A1Hook(Base):
    act = 1
    title = "The question"

    def build(self):
        b = box("8,000,000,000 numbers", w=4.2, h=1.6, color=GREYC, size=30)
        b.move_to(ORIGIN)
        self.play(FadeIn(b))
        self.until(0.08)
        inp = T("The capital of France is", 30, WHITE).next_to(b, LEFT, buff=0.9)
        a1 = Arrow(inp.get_right(), b.get_left(), buff=0.1, color=GREYC)
        self.play(Write(inp), GrowArrow(a1))
        self.until(0.18)
        out = T("a city of romance", 30, AMBER).next_to(b, RIGHT, buff=0.9)
        a2 = Arrow(b.get_right(), out.get_left(), buff=0.1, color=GREYC)
        self.play(GrowArrow(a2), Write(out))
        self.until(0.30)
        chart = bars([16, 15.938, 15.062, 14.875, 14.312], names=['" a"', '" Paris"', '" known"', '" home"', '" the"'],
                     colors=[AMBER, BLUEC, GREYC, GREYC, GREYC], width=6.0, height=2.0, ymin=14, ymax=16.5, value_labels=True)
        chart.to_edge(DOWN, buff=0.6)
        cap = T("first-step scores, real run, no chat template", 20, GREYC).next_to(chart, UP, buff=0.15)
        self.play(FadeIn(chart), FadeIn(cap))
        self.until(0.48)
        self.play(Indicate(chart.bars[1], color=BLUEC))
        self.until(0.62)
        q = lines(["How would you know this box ran the model it claims,",
                   "on your prompt, without rerunning it yourself",
                   "and without seeing its weights?"], 28, YEL, align=ORIGIN)
        q.to_edge(UP, buff=0.9)
        self.play(FadeOut(chart), FadeOut(cap), VGroup(b, inp, out, a1, a2).animate.shift(DOWN * 1.2))
        self.play(Write(q), run_time=3)


class A1Receipt(Base):
    act = 1
    title = "A receipt for a computation"

    def build(self):
        head = T("A receipt must", 32, WHITE).to_edge(UP, buff=1.0)
        self.play(FadeIn(head))
        items = lines(["1. fix the input: which token ids went in",
                       "2. fix the machine: which weights, without revealing them",
                       "3. make every step checkable, so a wrong step cannot hide"], 28)
        items.next_to(head, DOWN, buff=0.4)
        for i, frac in zip(items, [0.12, 0.2, 0.3]):
            self.until(frac)
            self.play(FadeIn(i, shift=RIGHT * 0.3))
        self.until(0.42)
        self.play(FadeOut(items), FadeOut(head))
        cards = VGroup(
            VGroup(box("PUBLISHER", 3.6, 0.7, BLUEC, 26), lines(["holds the weights", "commits to them once", "publishes the 32-byte root"], 22, GREYC)),
            VGroup(box("PROVER", 3.6, 0.7, AMBER, 26), lines(["holds the weights, a GPU", "reruns the decode", "commits tables, answers", "challenges, writes proofs"], 22, GREYC)),
            VGroup(box("VERIFIER", 3.6, 0.7, TEALC, 26), lines(["prompt ids, model root,", "calibration file, a CPU", "no weights, no GPU"], 22, GREYC)),
        )
        for c in cards:
            c.arrange(DOWN, buff=0.25)
        cards.arrange(RIGHT, buff=0.6, aligned_edge=UP).move_to(ORIGIN)
        for c, frac in zip(cards, [0.5, 0.65, 0.8]):
            self.until(frac)
            self.play(FadeIn(c, shift=UP * 0.3))


class A1Shape(Base):
    act = 1
    title = "The answer in one line"

    def build(self):
        steps = ["rerun the model\nin rule-shaped\narithmetic", "write every\nintermediate value\ninto tables",
                 "commit\nto the tables", "let a random audit\ncheck the rules"]
        cols = [AMBER, AMBER, BLUEC, TEALC]
        bs = VGroup(*[box(s, 2.9, 1.5, c, 22) for s, c in zip(steps, cols)]).arrange(RIGHT, buff=0.45)
        arrows = VGroup(*[Arrow(bs[i].get_right(), bs[i + 1].get_left(), buff=0.05, color=GREYC) for i in range(3)])
        for i, frac in enumerate([0.15, 0.35, 0.55, 0.72]):
            self.until(frac)
            anims = [FadeIn(bs[i])]
            if i:
                anims.append(GrowArrow(arrows[i - 1]))
            self.play(*anims)
        self.until(0.88)
        self.play(Write(T("the rest of the video unpacks this line", 24, GREYC).to_edge(DOWN, buff=1.0)))


class A1Honest(Base):
    act = 1
    title = "What ZK means here"

    def build(self):
        zk = T("ZK", 96, WHITE)
        self.play(Write(zk))
        self.until(0.15)
        sub = T("names a family of proof systems", 30, GREYC).next_to(zk, DOWN, buff=0.4)
        self.play(FadeIn(sub))
        self.until(0.32)
        self.play(VGroup(zk, sub).animate.to_edge(UP, buff=0.8))
        hidden = VGroup(tree(BLUEC, 1.8, 1.3, "model tree"), T("weights hidden\nbehind the root", 22, BLUEC)).arrange(DOWN, buff=0.3)
        pub = lines(["public: the architecture", "public: the prompt ids", "public: every committed table (no blinding)"], 24, GREYC)
        row = VGroup(hidden, pub).arrange(RIGHT, buff=1.2).move_to(DOWN * 0.6)
        self.play(FadeIn(hidden))
        self.until(0.55)
        self.play(FadeIn(pub, shift=RIGHT * 0.3))
        self.until(0.8)
        self.play(Write(T("a proof of correctness, not a privacy tool", 28, YEL).to_edge(DOWN, buff=0.7)))
