from manim import *
from manim_slides import Slide
import math
ADDER_COLOR=GREEN
MULT_COLOR=YELLOW
ROTT_COLOR=RED
class MatEmVideo(Scene): #Scene or Slide
    def rotate_vector(self, vector, angle):
        x = vector[0] * math.cos(angle) - vector[1] * math.sin(angle)
        y = vector[0] * math.sin(angle) + vector[1] * math.cos(angle)
        return [x, y, 0]
    def stretch(self, factor, *args, **kwargs):
        line = self.number_line if len(args)==0 else args[0]
        zero_point = line.number_to_point(0)  
        target = line.copy()
        # target.stretch(factor, 0)
        print(line.get_unit_vector())
        for d in [0,1,2]:
            target.stretch_about_point(factor, d, zero_point) if line.get_unit_vector()[d] >0.1 else 0
        arrow = Arrow(line.number_to_point(1), line.number_to_point(factor), buff = 0)
        arrow.set_color(MULT_COLOR)
        self.play(Create(arrow))
        self.wait()
        self.play(arrow.animate.shift(MED_LARGE_BUFF*2*np.array(self.rotate_vector(line.get_unit_vector(), PI/2))))
        self.wait()
        if hasattr(target, 'numbers'):
            for number in target.numbers:
                number.stretch_to_fit_width(number.width/factor)
        self.play(
        Transform(line, target, **kwargs),
        *kwargs.get("added_anims", []))
        self.play(FadeOut(arrow))
    def show_example_slides(self, num, *args):
        line = self.number_line if len(args)==0 else args[0]
        zero_point = line.number_to_point(0)            
        num_point = line.number_to_point(num)
        arrow = Arrow(zero_point, num_point, buff = 0)
        arrow.set_color(ADDER_COLOR)
        self.play(Create(arrow))
        self.wait()
        self.play(arrow.animate.shift(MED_LARGE_BUFF*2*np.array(self.rotate_vector(line.get_unit_vector(), PI/2))))
        self.wait()
        self.play(line.animate.shift(num_point-zero_point))
        self.wait()
        self.play(FadeOut(arrow))
    def rotate(self, angle, num, p_color=ROTT_COLOR):
        target = NumberLine([-20,20], unit_size=self.number_line.get_unit_size())
        t = target.copy()
        p = t.rotate(angle).number_to_point(num)
        arrow = CurvedArrow(self.number_line.number_to_point(num), p, color=ROTT_COLOR)
        self.wait()
        self.play(Create(arrow))
        self.wait()
        self.play(Rotate(target, angle))
        self.play(Create(Dot(p, color=p_color)))
        self.play(FadeOut(arrow))
        return target
    def end_point(self, id:int):
        zero_point = self.number_line.number_to_point(id)
        end_point = [zero_point[0], self.shadow_line.number_to_point(0)[1], zero_point[2]]
        arrow = Arrow(zero_point, end_point)
        arrow.set_color([ADDER_COLOR, MULT_COLOR][id])
        self.play(Create(arrow))
        self.wait()
        self.play(FadeOut(arrow))
    class Relogio:
        def __init__(self, selfU, horas:int=12, lap=0):
            self.selfU = selfU
            self.horas = horas
            self.phase = lap
            self.circle = Circle(radius=3.0)
            self.hours = self.distCirc(lap)
            self.selfU.add(self.circle)
            self.selfU.play(Create(self.hours))
        def moveCirc(self, lap):
            self.phase += lap
            n_hours = self.distCirc(self.phase)
            self.selfU.play(*[Transform(self.hours[i], n_hours[(i-self.phase)%self.horas],
                        path_arc=lap*2*PI/len(self.hours)
                        ) for i in range(len(self.hours))])
            # self.hours = n_hours
        def distCirc(self, lap:int=0):
            angles = [PI/2-(n+1) * (2*PI / self.horas) for n in range(self.horas)]
            points = [self.circle.point_at_angle(n) for n in angles]
            dots = [LabeledDot(str((p+lap)%self.horas+1)).move_to(points[p]) for p in range(self.horas)]
            return VGroup(*dots)
    def construct(self):
        self.number_line = NumberLine([-20,20],include_numbers=True, label_direction=UP)
        self.shadow_line = NumberLine([-20,20],include_numbers=True)
        # self.shadow_line.next_to(self.number_line, DOWN*3)
        r = self.Relogio(self, 12)
        # self.Relogio.moveCirc(r, 2)
        self.wait()
        r.moveCirc(2)
        self.wait()
        r.moveCirc(-4)
        self.wait()
        r.moveCirc(2)
        # self.torre = arrow(
        self.wait()