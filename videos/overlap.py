from manim import *


class Overlap(Scene):
    num_frames = 15
    home = (-4, 0, 0)

    def construct(self):        
        self.wait(0.5)

        # make drone and trace object
        drone = SVGMobject("res/drone_icon.svg").scale(0.55)
        dot = Dot(radius=0)
        drone = VGroup(drone, dot).move_to(self.home)
        trace = TracedPath(dot.get_start, dissipating_time=2)

        site = Rectangle(BLUE_A, 1.5, 9.8)

        frame_a = Rectangle(YELLOW, 0.9, 1.6).move_to(self.home)
        colors = color.color_gradient((GREEN, BLUE, YELLOW, PINK, BLUE, ORANGE), self.num_frames)
        frames = [frame_a.copy().set_color(colors[x]).shift(x * 0.5714 * RIGHT) for x in range(self.num_frames)]

        # make objects
        self.play(Create(drone), Create(site))
        self.add(trace)

        # sweep across path
        self.play(drone.animate(run_time=2, rate_func=rate_functions.linear).shift(8 * RIGHT))
        self.play(AnimationGroup(*[FadeIn(rectangle, run_time=2 / self.num_frames, scale=1.5) for rectangle in frames], lag_ratio=1))
        self.remove(trace)
        self.wait(2)

        # clear out site, drone, and frames 
        self.play(AnimationGroup(*[Uncreate(rectangle, run_time=0.1) for rectangle in frames], lag_ratio=0.4))
        self.play(drone.animate.shift(RIGHT * 10), Uncreate(site))
        self.wait(2)

        # make image demo objects
        frame_a.move_to((-1, 0, 0)).scale(3)
        frame_b = Rectangle(BLUE, 2.7, 4.8).move_to((1, 0, 0))

        frame_a.set_fill(YELLOW, opacity=0.5)
        frame_b.set_fill(BLUE, opacity=0.5)

        # create two frames
        self.play(Create(frame_a))
        self.play(Create(frame_b))
        self.wait(1)

        # change overlaop
        self.play(frame_b.animate.shift(LEFT * 1.5))
        self.wait(0.2)

        self.play(frame_b.animate.shift(3 * RIGHT))
        self.wait(1)

        # change area
        self.play(Uncreate(frame_a), frame_b.animate.move_to((0, 0, 0)))
        self.play(frame_b.animate.scale(2))
        self.wait(0.5)

        self.play(frame_b.animate.scale(0.25))
        self.wait(0.5)

        self.play(frame_b.animate.scale(2))
        self.wait(2)

        # end scene
        self.play(Uncreate(frame_b))
        self.wait(0.5)
