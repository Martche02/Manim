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
        self.wait()
        # self.next_slide()
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

    def p2016n1q6(self):
        def anel(cores:list, m:float, n:float, d:bool=False, centro=0, p:bool=False):
            cores=cores[::-1]
            a = VGroup()
            for i in range(len(cores)):
                a.add(AnnularSector(color=[WHITE, GRAY][cores[i]], start_angle=(5-i)*PI/3+[PI/6,0][d], angle=PI/3,
                                     inner_radius=m, outer_radius=n, stroke_color=BLACK, stroke_width=1))
            return a.move_to(DOWN*centro)
        def arco(i, f, color):
            d = Dot()
            c = Arc(1.5, i, f-i)
            d.set_color(color)
            c2 = VMobject()
            self.add(d, c, c2)
            c2.add_updater(lambda x: x.become(ArcBetweenPoints(d.get_center(), self.rotate_vector(RIGHT*1.5, i), radius=1.5).set_color(color)))
            self.play(MoveAlongPath(d, c), rate_func=linear)
            self.remove(d)
            self.remove(c)
            return c2
        def juncao(a, i=1, o=2):
            return AnnularSector(i, o, 0.01, a, color=BLACK, stroke_color=BLACK, stroke_width=1)
        def percurso3(a, b, c):
            c3 = VGroup()
            c3.add(juncao(a))
            c3.add(juncao(b))
            c3.add(juncao(c))
            self.play(Create(c3[0]))
            self.play(Create(c3[1]))
            self.play(Create(c3[2]))
            self.pause()
            c3.add(arco(0,a, YELLOW))
            c3.add(arco(a, b, PURPLE))
            c3.add(arco(b, c, YELLOW))
            c3.add(arco(c, -11*TAU/12, PURPLE))
            self.pause()
            self.remove(*[c3[i] for i in range(len(c3))])
        def percurso2(a, b):
            c2 = VGroup()
            c2.add(juncao(a))
            c2.add(juncao(b))
            self.play(Create(c2[0]))
            self.play(Create(c2[1]))
            self.pause()
            c2.add(arco(0,a, YELLOW))
            c2.add(arco(a, b, PURPLE))
            c2.add(arco(b, -11*TAU/12, YELLOW))
            self.pause()
            self.remove(*[c2[i] for i in range(len(c2))])
        def percurso1(a):
            c = VGroup()
            c.add(juncao(a))
            self.play(Create(c[0]))
            self.pause()
            c.add(arco(0,a, YELLOW))
            c.add(arco(a, -11*TAU/12, PURPLE))
            self.pause()
            self.remove(*[c[i] for i in range(len(c))])
        enunciado = Tex('''(OBMEP 2016N1Q6 ADAPTADA) Joãozinho pinta anéis encaixados, 
cada um deles dividido em seis partes iguais.
No primeiro anel (o menor deles) Joãozinho pinta de cinza algumas partes.
Do segundo anel em diante, ele pinta de cinza somente
as partes em contato com duas partes de cores diferentes do anel anterior.
Observe um exemplo:''', font_size=30)
        self.play(Create(enunciado))
        self.pause()
        self.play(enunciado.animate.shift(UP*3))
        self.pause()
        en = VGroup(enunciado, anel([0,1,0,1,0,0], 0.7, 1.2, False, 1.2), anel([0,1,1,1,1,0], 1.2, 1.7, True , 1.2),
                    anel([0,1,0,0,1,0], 1.7, 2.2, False, 1.2), anel([0,1,1,0,1,1], 2.2, 2.7, True , 1.2))
        self.play(Create(en[1]))
        self.next_slide()
        self.pause()
        self.play(Create(en[2]))
        self.next_slide()
        self.pause()
        self.play(Create(en[3]))
        self.next_slide()
        self.pause()
        self.play(Create(en[4]))
        self.next_slide()
        self.pause()
        self.play(FadeOut(en))
        self.next_slide()
        self.pause()
        A = Tex('''A) Joãozinho pintou o primeiro 
anel conforme a figura abaixo.
Continue o trabalho de Joãozinho, pintando,
na mesma figura, o segundo e o terceiro anéis''', font_size=30)
        self.play(Create(A))
        self.pause()
        self.play(A.animate.shift(UP*3))
        self.pause()
        iA = VGroup(A, anel([1,0,1,0,0,1], 0.7, 1.2, False, 0.8, True), anel([0,1,1,1,0,1], 1.2, 1.7, True , 0.8, True),
                    anel([1, 0, 0, 1, 1, 1], 1.7, 2.2, False, 0.8, True))
        self.play(Create(iA[1]))
        self.next_slide()
        self.pause()
        self.play(Create(iA[2]))
        self.next_slide()
        self.pause()
        self.play(Create(iA[3]))
        self.next_slide()
        self.pause()
        self.play(FadeOut(iA))
        self.next_slide()
        self.pause()
        B = Tex('''B) Na figura abaixo, pinte as partes do primeiro anel de modo que o segundo anel fique todo pintado de cinza''', font_size=30)
        self.play(Create(B))
        self.pause()
        self.play(B.animate.shift(UP*3))
        self.pause()
        iB = VGroup(B, anel([1,1,1,1,1,1], 1.2, 1.7, True, 0.8), anel([1,0,1,0,1,0], 0.7, 1.2, False, 0.8),
                    anel([0,1,0,1,0,1], 0.7, 1.2, False, 0.8), anel([0,0,0,0,0,0], 0.7, 1.2, False, 0.8))
        self.play(Create(iB[4]))
        self.next_slide()
        self.play(Create(iB[1]))
        self.next_slide()
        self.pause()
        self.play(Create(iB[2]))
        self.next_slide()
        self.pause()
        self.play(FadeOut(iB[2]))
        self.next_slide()
        self.pause()
        self.play(Create(iB[3]))
        self.next_slide()
        self.pause()
        self.play(FadeOut(iB))
        self.pause()
        C = Tex('''C) Explique por que, independentemente de como Joãozinho pintar o primeiro anel, os demais anéis sempre terão uma
quantidade par de partes pintadas de cinza.''', font_size=30)
        self.play(Create(C))
        self.pause()
        self.play(C.animate.shift(UP*3))
        self.pause()
        iC = VGroup()
        iC.add(Tex('''O que cria uma parte cinza?''', font_size=30))
        iC.add(Tex('''Junção entre cinza e branco''', font_size=30))
        iC.add(Tex('''Pode ter uma quantidade impar de junções?''', font_size=30))
        iC.add(Tex('''Implicaria cor Inicial a ser Cinza e Branca, contradição''', font_size=30))
        iC.add(Tex('''Reductio ad Absurdum''', font_size=30))
        self.play(iC[0].animate.shift(LEFT*3))
        iC[1].next_to(iC[0], RIGHT)
        self.pause()
        self.play(Create(iC[1]))
        self.pause()
        iC[2].next_to(iC[0], DOWN*2)
        self.play(Create(iC[2]))
        self.pause()
        self.play(FadeOut(C, iC[0], iC[1], iC[2]))
        self.pause()
        iC.add(AnnularSector(1, 2, TAU, color=WHITE))
        iC.add(AnnularSector(1, 2, TAU/6, color=YELLOW, stroke_color=BLACK, stroke_width=1))
        self.pause()
        self.next_slide()
        self.play(*[Create(iC[-2]), Create(iC[-1])])
        percurso1(-TAU/2)
        self.next_slide()
        self.pause
        percurso3(-TAU/3, -TAU/2, -2*TAU/3)
        self.pause()
        self.next_slide()
        percurso2(-TAU/3, -2*TAU/3)
        self.pause()
        self.next_slide()
        self.play(FadeOut(iC[-2], iC[-1]))
        self.next_slide()
        self.pause()
        self.play(Create(C))
        iC[3].next_to(iC[2])
        self.play(iC[3].animate.shift(DOWN+LEFT*2))
        self.play(*[Create(iC[i]) for i in [0,1,2]])
        iC[4].next_to(iC[2], DOWN*5)
        self.pause()
        self.play(Create(iC[4]))
        self.next_slide()
        self.play(FadeOut(iC[0], iC[1], iC[2], iC[3], iC[4]))
        self.remove(C)
        D = Tex('''D) Explique por que, independentemente de como Joãozinho pintar o primeiro anel, nenhum anel a partir do terceiro será
totalmente pintado de cinza.''', font_size=30)
        self.play(Create(D))
        self.pause()
        self.play(D.animate.shift(UP*3))
        self.pause()
        iD = VGroup()
        iD.add(Tex('''O que cria um aro todo cinza?''', font_size=30))
        iD.add(Tex('''O Item B)''', font_size=30))
        iD.add(Tex('''O que cria B)?''', font_size=30))
        iD.add(Tex('''Uma quantidade ímpar de junções, impossível por C)''', font_size=30))
        self.play(iD[0].animate.shift(LEFT*3))
        iD[1].next_to(iD[0], RIGHT)
        self.pause()
        self.play(Create(iD[1]))
        self.pause()
        iD[2].next_to(iD[0], DOWN*2)
        self.play(Create(iD[2]))
        self.pause()
        iD[3].next_to(iD[2])
        self.play(Create(iD[3]))

    def p2021n3q6(self):
        class m:
            def __init__(self, selfE, n:str, r, todas_caras:bool=False):
                self.coroa = [YELLOW, PURPLE][todas_caras]
                self.cara = [PURPLE, YELLOW][todas_caras]
                self.r = r
                self.selfE = selfE
                self.face = self.moeda(n)
                self.f = not todas_caras
            def __neg__(self) -> VGroup:
                self.selfE.play(self.face.animate.flip(UP))
                self.face.set_color(self.cara) if self.f else self.face.set_color(self.coroa)
                self.f = not self.f
                return self.face
            def __pos__(self) -> VGroup:
                self.selfE.play(self.face.animate.flip(DOWN))
                self.selfE.play(self.face.animate.flip(DOWN))
                return self.face
            def moeda(self, n:str) -> VGroup:
                return VGroup(Circle(self.r), Tex(str(n))).set_color(self.coroa)
            def move_to(self, add):
                self.face.move_to(add)
        class c:
            def __init__(self, selfE, p0, r:int=2, todas_caras:bool=False):
                self.p0 = p0
                self.mesa = VGroup()
                self.circ = Circle(r).move_to(p0)
                self.mesa.add(Arrow(self.p0, RIGHT*r*3/4+self.p0))
                self.pos = 0
                self.mesa_de_valores = []
                for i in range(10):
                    a = m(selfE, ['A','B','C','D','E','F','G','H','I','J'][i], r/4, todas_caras=todas_caras)
                    self.mesa_de_valores.append(a)
                    self.mesa.add(a.face.move_to(self.circ.point_at_angle(i*TAU/10)))
                selfE.play(Create(self.mesa))
                self.selfE = selfE
            def __pos__(self) -> VGroup:
                self.pos +=1
                self.pos %=10
                self.selfE.play(self.mesa[0].animate.rotate(TAU/10, about_point=self.p0))
                -self.mesa_de_valores[(self.pos+1)%10] if self.mesa_de_valores[self.pos].f else +self.mesa_de_valores[(self.pos+1)%10]
                return self.mesa
            def __neg__(self) -> VGroup:
                -self.mesa_de_valores[(self.pos+1)%10] if self.mesa_de_valores[self.pos].f else +self.mesa_de_valores[(self.pos+1)%10]
                self.selfE.play(self.mesa[0].animate.rotate(-TAU/10, about_point=self.p0))
                self.pos -= 1
                self.pos %= 10
                return self.mesa
        enunciado = Tex('''(OBMEP 2021N3Q6 ADAPTADA) São dispostas 10 moedas em um círculo.
Inicialmente, todas as dez moedas são colocadas com a face coroa voltada para cima e um
ponteiro aponta para a posição A. 
\n\n Esse ponteiro começa a se movimentar no sentido anti-horário,
saltando de uma posição para a outra mais próxima. 
Após cada salto,
\n      • Se o ponteiro apontar para uma moeda
com a face cara para cima, nada acontece;
\n      • Se o ponteiro apontar para uma moeda
com a face coroa para cima, deve-se, então,
virar a moeda seguinte ''', font_size=23, tex_environment="flushleft", width=400)
        self.play(Create(enunciado))
        self.next_slide()
        self.play(enunciado.animate.shift(UP*2.5))
        self.next_slide()
        e = c(self, DOWN, 1.5)
        self.next_slide()
        +e
        self.next_slide()
        +e
        self.next_slide()
        +e
        self.next_slide()
        +e
        +e
        +e
        self.next_slide()
        self.play(FadeOut(enunciado, e.mesa))
        A = Tex('''A) Como ficarão as moedas nas posições C e D logo após o segundo salto do ponteiro? ''', font_size=30)
        self.play(Create(A))
        self.next_slide()
        self.play(A.animate.shift(UP*3))
        self.next_slide()
        a = c(self, UR+DL)
        self.next_slide()
        +a
        a.mesa[3].set_color(PURPLE)
        self.next_slide()
        +a
        self.next_slide()
        self.play(FadeOut(A, a.mesa))
        self.next_slide()
        B = Tex('''B) Em quais posições as moedas ficarão com as faces coroa para cima após o décimo segundo salto? ''', font_size=30)
        self.play(Create(B))
        self.next_slide()
        self.play(B.animate.shift(UP*3))
        self.next_slide()
        b = c(self, UR+DL)
        self.next_slide()
        +b
        self.next_slide()
        +b
        +b
        +b
        +b
        +b
        +b
        +b
        +b
        +b
        +b
        +b
        b.mesa[4].set_color(PURPLE)
        self.next_slide()
        self.play(FadeOut(B, b.mesa))
        self.next_slide()
        C = Tex('''C) Explique por que nunca todas as moedas ficarão com a face cara voltada para cima ''', font_size = 30)
        self.play(Create(C))
        self.next_slide()
        self.play(C.animate.shift(UP*3))
        self.next_slide()
        c1 = c(self, UR+DL)
        self.next_slide()
        +c1
        +c1
        +c1
        +c1
        +c1
        +c1
        +c1
        self.next_slide()
        -c1
        self.next_slide()
        -c1
        self.next_slide()
        -c1
        self.next_slide()
        -c1
        c1.mesa[5].set_color(YELLOW)
        self.next_slide()
        self.play(FadeOut(c1.mesa))
        self.next_slide()
        c2 = c(self, UR+DL, todas_caras=True)
        self.next_slide()
        +c2
        self.next_slide()
        -c2
        self.next_slide()
        -c2
        self.next_slide()
        -c2
        self.next_slide()
        RAA = Tex("Terminar com caras implica começar com caras ", font_size=35).shift(DOWN*3)
        self.play(Create(RAA))
        self.next_slide()
        self.play(Transform(VGroup(RAA, c2.mesa), Tex('''Começar com coroas e terminar com caras é impossível;
\n         nunca acabará com caras - Reductio ad Absurdum ''', font_size=50)))
        self.next_slide()
        self.play(*[FadeOut(mob)for mob in self.mobjects])
        self.next_slide()
        D = Tex('''D) Explique por que todas as moedas voltarão a ser simultaneamente coroa após algum momento ''', font_size=30)
        self.play(Create(D))
        self.next_slide()
        self.play(D.animate.shift(UP*3))
        self.next_slide()
        d = c(self, UP+DOWN)
        d1 = d.mesa.copy()
        tE = VGroup()
        tE.add(Tex(r"$E_1$", font_size=40).next_to(DL*3+LEFT*0.4))
        self.next_slide()
        self.play(Transform(d1, tE[0]))
        self.next_slide()
        +d
        d2 = d.mesa.copy()
        tE.add(Tex(r"$\rightarrow E_2$", font_size=40).next_to(tE[0], RIGHT))
        self.play(Transform(d2, tE[1]))
        self.next_slide()
        +d
        d3 = d.mesa.copy()
        tE.add(Tex(r"$\rightarrow E_3$", font_size=40).next_to(tE[1], RIGHT))
        self.play(Transform(d3, tE[2]))
        self.next_slide()
        +d
        d4 = d.mesa.copy()
        tE.add(Tex(r"$\rightarrow E_4$", font_size=40).next_to(tE[2], RIGHT))
        self.play(Transform(d4, tE[3]))
        self.next_slide()
        tE.add(Tex(r"$\rightarrow \cdots \rightarrow E_n$").next_to(tE[3], RIGHT))
        self.play(Create(tE[4]))
        self.next_slide()
        self.play(FadeOut(d.mesa))
        self.play(VGroup(d1, d2, d3, d4,tE).animate.shift(UP*3))
        self.next_slide()
        conc = Tex(r'''$E_n \rightarrow E_2$ é o primeiro sucessor repetido $\Rightarrow E_n = E_1$ ''')
        conclusao =VGroup(conc, Tex(r'''$\Rightarrow E_{n-1} \rightarrow E_n$ é o primeiro sucessor repetido (Absurdo) ''').next_to(conc, DOWN))
        self.play(Create(conclusao.move_to(DOWN*3)))
        self.next_slide()
        self.play(Create(CurvedArrow(RIGHT*3.2+UP/2, LEFT*1.6+UP/2)))
        self.next_slide()
        self.play(Create(CurvedArrow(LEFT*2.9+UP/2, LEFT*1.9+UP/2, angle=-PI/2)))

    def construct(self):
        self.p2021n3q6()
        self.wait()