from manim import *
from manim_slides import Slide
import math
ADDER_COLOR=GREEN
MULT_COLOR=YELLOW
ROTT_COLOR=RED
class MatEmVideo(Slide): #Scene or Slide
    def rotate_vector(self, vector, angle):
        x = vector[0] * math.cos(angle) - vector[1] * math.sin(angle)
        y = vector[0] * math.sin(angle) + vector[1] * math.cos(angle)
        return [x, y, 0]
    def multiplication(self, factor, *args, **kwargs):
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
        self.pause()
        self.play(arrow.animate.shift(MED_LARGE_BUFF*2*np.array(self.rotate_vector(line.get_unit_vector(), PI/2))))
        self.pause()
        if hasattr(target, 'numbers'):
            for number in target.numbers:
                number.stretch_to_fit_width(number.width/factor)
        self.play(
        Transform(line, target, **kwargs),
        *kwargs.get("added_anims", []))
        self.play(FadeOut(arrow))
    def addition(self, num, *args):
        line = self.number_line if len(args)==0 else args[0]
        zero_point = line.number_to_point(0)            
        num_point = line.number_to_point(num)
        arrow = Arrow(zero_point, num_point, buff = 0)
        arrow.set_color(ADDER_COLOR)
        self.play(Create(arrow))
        self.pause()
        self.play(arrow.animate.shift(MED_LARGE_BUFF*2*np.array(self.rotate_vector(line.get_unit_vector(), PI/2))))
        self.pause()
        self.play(line.animate.shift(num_point-zero_point))
        self.pause()
        self.play(FadeOut(arrow))
    def rotate(self, angle, num, p_color=ROTT_COLOR):
        target = NumberLine([-20,20], unit_size=self.number_line.get_unit_size())
        t = target.copy()
        p = t.rotate(angle).number_to_point(num)
        arrow = CurvedArrow(self.number_line.number_to_point(num), p, color=ROTT_COLOR)
        self.pause()
        self.play(Create(arrow))
        self.pause()
        self.play(Rotate(target, angle))
        self.play(Create(Dot(p, color=p_color)))
        self.play(FadeOut(arrow))
        return target
    def end_point(self, id:int=0):
        zero_point = self.number_line.number_to_point(id)
        end_point = [zero_point[0], self.shadow_line.number_to_point(0)[1], zero_point[2]]
        arrow = Arrow(zero_point, end_point)
        arrow.set_color([ADDER_COLOR, MULT_COLOR][id])
        self.play(Create(arrow))
        self.pause()
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
    def pause(self):
        # self.wait()
        self.next_slide()
    def cap1(self):
        p = self.pause
        self.number_line = NumberLine([-30,30], include_numbers=True, label_direction=UP)
        self.shadow_line = NumberLine([-30,30], include_numbers=True)
        self.shadow_line.next_to(self.number_line, DOWN*3)
        self.play(Create(self.number_line), run_time=2.5)
        self.play(Create(self.shadow_line), run_time=2.5)
        self.addition(2)
        p()
        self.addition(-5)
        p()
        self.end_point()
        p()
        self.addition(3)
        p()
        self.end_point()
        p()
        self.addition(4)
        self.end_point()
        p()
        self.addition(-4)
        p()
        self.multiplication(2)
        p()
        self.multiplication(1/2)
        p()
        self.multiplication(3)
        self.end_point(1)
        self.multiplication(2)
        p()
        self.end_point(1)
        p()
        self.multiplication(1/6)
        p()
        self.end_point(1)
        self.multiplication(2)
        self.end_point(1)
        self.multiplication(1/2)
        self.addition(2)
        self.end_point()
        p()
        self.addition(-2)
        p()
        self.remove(self.number_line, self.shadow_line)
        e = VGroup()
        e.add(MathTex(r'P_n &= 1_1+1_2 +1_3 +\cdots+1_n'))
        self.play(Create(e[0]))
        p()
        e.add(MathTex(r'P_n &= 1_1+2_2+3_3+4_4+5_5'))
        self.play(Transform(e[0], e[1]))
        p()
        e.add(MathTex(r'+\cdots+N_n'))
        e[2].next_to(e[1], RIGHT)
        self.play(Create(e[2]))
        p()
        e.add(MathTex(r'P_n &= (i)_0\:\:\:\:\:\:\:\:\:\:\:\:+(i+p)_1\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:+(i+2p)_2\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:+\cdots\\&+(i+Np)_n+(i+[N-1]p)_{N-1}+(i+[N-2]p)_{N-2}+\cdots'))
        self.play(Transform(VGroup(e[0], e[2]), e[3]))
        p()
        e.add(MathTex(r'P_n = (2i+Np)+(2i+Np)+(2i+Np)+\cdots\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:'))
        e[4].next_to(e[3], DOWN)
        self.play(Create(e[4]))
        p()
        e.add(MathTex(r'P_n = (2i+Np)\cdot\dfrac{N+1}2'))
        self.remove(VGroup(e[0], e[2]), e[0], e[1], e[2], e[3])
        self.play(Transform(e[4], e[5]))
        p()
        e.add(MathTex(r'P_n = \dfrac{N(N+1)p+2(N+1)i}2'))
        self.play(Transform(e[4], e[6]))
        p()
        self.remove(VGroup(e[0], e[2]), e[0], e[1], e[2], e[3], e[4], e[5], e[6])
        self.add(self.number_line)
        s = [-3, -2, -1, 0, 1, 2, 3, 4]
        S = [LabeledDot(str(i)).move_to(self.number_line.number_to_point(i)) for i in s]
        self.play(*[Create(i) for i in S])
        p()
        P = VGroup()
        for i in range(4):
            P.add(MathTex(r'1').move_to(self.number_line.number_to_point(0)+ 0.75*UP*(i+1)))
            self.play(Transform(VGroup(S[i],S[-1-i]), P[i]))
            p()
        self.remove(P)
        self.play(Transform(VGroup(*S), MathTex("4").move_to(self.number_line.number_to_point(0)+DOWN)))



    def construct(self):
        self.cap1()
        self.wait()