from manim import *


class Overlap(Scene):
    num_frames = 15
    home = (-4.1, 0, 0)

    def construct(self):
        # make drone and trace object
        drone = SVGMobject("res/drone_icon.svg").scale(0.55)
        dot = Dot(radius=0)
        drone = VGroup(drone, dot).move_to(self.home)
        trace = TracedPath(dot.get_start, dissipating_time=1)

        site = Rectangle(BLUE_A, 1.8, 9.9)

        frame = Rectangle(YELLOW, 0.9, 1.6).move_to(self.home)
        colors = color.color_gradient((GREEN, BLUE, YELLOW, RED), self.num_frames)
        frames = [frame.copy().set_color(colors[x]).shift(x * 0.58 * RIGHT) for x in range(self.num_frames)]

        # make objects
        self.play(Create(drone), Create(site))
        self.add(trace)

        # sweep across path
        self.play(drone.animate(run_time=2).shift(8 * RIGHT), 
                AnimationGroup(*[Create(rectangle, run_time=2.5 / self.num_frames) for rectangle in frames], lag_ratio=1))
        self.wait(2)

        # clear out site, drone, and frames 
        self.play(FadeOut(site), FadeOut(drone), *[FadeOut(rectangle) for rectangle in frames])
        self.wait(2)

        # create one frame
        self.play(Create(frames[0]))