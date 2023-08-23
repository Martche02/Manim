from manim import *
import math
ADDER_COLOR=GREEN
MULT_COLOR=YELLOW
ROTT_COLOR=RED
class NumberLineExample(Scene):
    def rotate_vector(self, vector, angle):
        x = vector[0] * math.cos(angle) - vector[1] * math.sin(angle)
        y = vector[0] * math.sin(angle) + vector[1] * math.cos(angle)
        return [x, y, 0]
    def stretch(self, factor, *args, **kwargs):
        line = self.numberline if len(args)==0 else args[0]
        zero_point = line.number_to_point(0)  
        target = line.copy()
        target.stretch(factor, 1)
        arrow = Arrow(line.number_to_point(1), line.number_to_point(factor), buff = 0)
        arrow.set_color(MULT_COLOR)
        self.play(Create(arrow))
        self.wait()
        self.play(arrow.animate.shift(MED_LARGE_BUFF*2*np.array(self.rotate_vector([line.number_to_point(1)[0]-line.number_to_point(0)[0],
                                                                        line.number_to_point(1)[1]-line.number_to_point(0)[1]], PI/2))))
        self.wait()
        if hasattr(target, 'numbers'):
            for number in target.numbers:
                number.stretch_to_fit_width(number.width/factor)
        self.play(
        Transform(line, target, **kwargs),
        *kwargs.get("added_anims", []))
        self.play(FadeOut(arrow))
    def show_example_slides(self, num, *args):
        line = self.numberline if len(args)==0 else args[0]
        zero_point = line.number_to_point(0)            
        num_point = line.number_to_point(num)
        arrow = Arrow(zero_point, num_point, buff = 0)
        arrow.set_color(ADDER_COLOR)
        self.play(Create(arrow))
        self.wait()
        self.play(arrow.animate.shift(MED_LARGE_BUFF*2*np.array(self.rotate_vector([line.number_to_point(1)[0]-line.number_to_point(0)[0],
                                                                        line.number_to_point(1)[1]-line.number_to_point(0)[1]], PI/2))))
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
    def construct(self):
        self.number_line = NumberLine([-20,20],include_numbers=True, label_direction=UP)
        self.shadow_line = NumberLine([-20,20],include_numbers=True)
        self.shadow_line.next_to(self.number_line, DOWN*3)
        self.add(self.number_line)
        r = self.rotate(PI/2, 2)
        self.stretch(3.5, r)
        self.wait()