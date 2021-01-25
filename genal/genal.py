from collections import namedtuple
from PyQt5.QtCore import QObject, pyqtSignal

import random
import time

from queue import PriorityQueue

# Declaring namedtuple, x0 is the constant
Polinomial = namedtuple(
    'Polinomial', [
        'x6', 'x5', 'x4', 'x3', 'x2', 'x1', 'x0'])

MAX_POPULATION_SIZE = 50
INITIAL_POPULATION_SIZE = 10
MUTATION_THRESHOLD = 1
MUTATION_CHANCE_SPACE = 100
ERROR_THRESHOLD = 0.05
MUTATION_RATE = 0.1

f1_data = (
    (-1.500000000000000, 1.037500000000000),
    (-1.438775510204080, 1.614668405292740),
    (-1.377551020408160, 2.080179252935180),
    (-1.316326530612240, 2.444890992334340),
    (-1.255102040816330, 2.719189966401270),
    (-1.193877551020410, 2.912990411551070),
    (-1.132653061224490, 3.035734457702880),
    (-1.071428571428570, 3.096392128279880),
    (-1.010204081632650, 3.103461340209320),
    (-0.948979591836734, 3.064967903922440),
    (-0.887755102040816, 2.988465523354580),
    (-0.826530612244897, 2.881035795945080),
    (-0.765306122448979, 2.749288212637350),
    (-0.704081632653061, 2.599360157878820),
    (-0.642857142857143, 2.436916909620990),
    (-0.581632653061224, 2.267151639319380),
    (-0.520408163265306, 2.094785411933560),
    (-0.459183673469388, 1.924067185927150),
    (-0.397959183673469, 1.758773813267790),
    (-0.336734693877551, 1.602210039427210),
    (-0.275510204081632, 1.457208503381120),
    (-0.214285714285714, 1.326129737609330),
    (-0.153061224489796, 1.210862168095650),
    (-0.091836734693877, 1.112822114327970),
    (-0.030612244897959, 1.032953789298190),
    (0.030612244897960, 0.971729299502272),
    (0.091836734693878, 0.929148644940216),
    (0.153061224489796, 0.904739719116063),
    (0.214285714285715, 0.897558309037901),
    (0.275510204081633, 0.906188095217857),
    (0.336734693877551, 0.928740651672105),
    (0.397959183673470, 0.962855445920857),
    (0.459183673469388, 1.005699838988370),
    (0.520408163265306, 1.053969085402950),
    (0.581632653061225, 1.103886333196930),
    (0.642857142857143, 1.151202623906710),
    (0.704081632653061, 1.191196892572700),
    (0.765306122448980, 1.218675967739390),
    (0.826530612244898, 1.227974571455290),
    (0.887755102040816, 1.212955319272950),
    (0.948979591836735, 1.167008720248970),
    (1.010204081632650, 1.083053176944010),
    (1.071428571428570, 0.953534985422740),
    (1.132653061224490, 0.770428335253897),
    (1.193877551020410, 0.525235309510249),
    (1.255102040816330, 0.208985884768613),
    (1.316326530612250, -0.187762068890152),
    (1.377551020408160, -0.674922787881147),
    (1.438775510204080, -1.262882615115430),
    (1.500000000000000, -1.962500000000010)
)

f2_data = (
    (-3.000000000000000, -5.500000000000000),
    (-2.775510204081630, 0.699742454249506),
    (-2.551020408163270, 6.076698484475010),
    (-2.326530612244900, 10.664808030667500),
    (-2.102040816326530, 14.498011032818000),
    (-1.877551020408160, 17.610247430917400),
    (-1.653061224489800, 20.035457164956800),
    (-1.428571428571430, 21.807580174927100),
    (-1.204081632653060, 22.960556400819400),
    (-0.979591836734694, 23.528325782624600),
    (-0.755102040816326, 23.544828260333700),
    (-0.530612244897959, 23.044003773937700),
    (-0.306122448979591, 22.059792263427600),
    (-0.081632653061224, 20.626133668794500),
    (0.142857142857143, 18.776967930029200),
    (0.367346938775510, 16.546234987122700),
    (0.591836734693878, 13.967874780066100),
    (0.816326530612245, 11.075827248850400),
    (1.040816326530610, 7.904032333466490),
    (1.265306122448980, 4.486429973905430),
    (1.489795918367350, 0.856960110158177),
    (1.714285714285710, -2.950437317784260),
    (1.938775510204080, -6.901822369930910),
    (2.163265306122450, -10.963255106290700),
    (2.387755102040820, -15.100795586872800),
    (2.612244897959180, -19.280503871686100),
    (2.836734693877550, -23.468440020739700),
    (3.061224489795920, -27.630664094042400),
    (3.285714285714290, -31.733236151603500),
    (3.510204081632650, -35.742216253431800),
    (3.734693877551020, -39.623664459536400),
    (3.959183673469390, -43.343640829926300),
    (4.183673469387760, -46.868205424610500),
    (4.408163265306120, -50.163418303598000),
    (4.632653061224490, -53.195339526897800),
    (4.857142857142860, -55.930029154518900),
    (5.081632653061220, -58.333547246470400),
    (5.306122448979590, -60.371953862761200),
    (5.530612244897960, -62.011309063400400),
    (5.755102040816320, -63.217672908397000),
    (5.979591836734690, -63.957105457759900),
    (6.204081632653060, -64.195666771498300),
    (6.428571428571420, -63.899416909621000),
    (6.653061224489790, -63.034415932137200),
    (6.877551020408160, -61.566723899055700),
    (7.102040816326530, -59.462400870385700),
    (7.326530612244890, -56.687506906136100),
    (7.551020408163260, -53.208102066316000),
    (7.775510204081630, -48.990246410934400),
    (7.999999999999990, -43.999999999999900)
)

f3_data = (
    (-2.500000000000000, 1.437500000000000),
    (-2.387755102040820, -1.348831182019770),
    (-2.275510204081630, -3.230821669219940),
    (-2.163265306122450, -4.371032253519670),
    (-2.051020408163270, -4.914686227296680),
    (-1.938775510204080, -4.990524596369150),
    (-1.826530612244900, -4.711661292977570),
    (-1.714285714285720, -4.176438388766590),
    (-1.602040816326530, -3.469281307766900),
    (-1.489795918367350, -2.661554039377100),
    (-1.377551020408160, -1.812414351345530),
    (-1.265306122448980, -0.969669002752172),
    (-1.153061224489800, -0.170628956990499),
    (-1.040816326530610, 0.557035405250669),
    (-0.928571428571429, 1.194439073005290),
    (-0.816326530612245, 1.730627192048250),
    (-0.704081632653062, 2.161719851913470),
    (-0.591836734693878, 2.490056872912070),
    (-0.479591836734695, 2.723342593150520),
    (-0.367346938775511, 2.873790655548730),
    (-0.255102040816327, 2.957268794858200),
    (-0.142857142857143, 2.992443624680190),
    (-0.030612244897960, 2.999925424483830),
    (0.081632653061224, 3.001412926624240),
    (0.193877551020408, 3.018838103360690),
    (0.306122448979591, 3.073510953874760),
    (0.418367346938775, 3.185264291288400),
    (0.530612244897959, 3.371598529682150),
    (0.642857142857142, 3.646826471113220),
    (0.755102040816326, 4.021218092633660),
    (0.867346938775510, 4.500145333308470),
    (0.979591836734693, 5.083226881233760),
    (1.091836734693880, 5.763472960554850),
    (1.204081632653060, 6.526430118484460),
    (1.316326530612240, 7.349326012320810),
    (1.428571428571430, 8.200214196465750),
    (1.540816326530610, 9.037118909442920),
    (1.653061224489800, 9.807179860915880),
    (1.765306122448980, 10.445797018706200),
    (1.877551020408160, 10.875775395811800),
    (1.989795918367350, 11.006469837424600),
    (2.102040816326530, 10.732929807949300),
    (2.214285714285710, 9.935044178021070),
    (2.326530612244900, 8.476686011523810),
    (2.438775510204080, 6.204857352608290),
    (2.551020408163260, 2.948834012710300),
    (2.663265306122450, -1.480689642431220),
    (2.775510204081630, -7.292455905756080),
    (2.887755102040810, -14.715498941864700),
    (3.000000000000000, -23.999999999999800)
)


def polimerize(x, coeffs):
    return coeffs.x6 * (x ** 6) \
        + coeffs.x5 * (x ** 5) \
        + coeffs.x4 * (x ** 4) \
        + coeffs.x3 * (x ** 3) \
        + coeffs.x2 * (x ** 2) \
        + coeffs.x1 * (x ** 1) \
        + coeffs.x0  # constant, so no multiplication required


class PolyFinder(QObject):
    generated = pyqtSignal(tuple, tuple, int)
    initialized = pyqtSignal()
    finished = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()

        self.f_data = ()
        self.looking_for_function = -1
        self.end = False
        self.g_no = 0
        self.previous_fitness = 999
        self.repeated_fitness = 0
        self.gen = PriorityQueue()
        self.mutation_rate = MUTATION_RATE
        self.mutation_probability = MUTATION_THRESHOLD

        self.stuck = False
        self.stuck_checker = 0

    def reset(self):
        self.looking_for_function = -1
        self.g_no = 0
        while not self.gen.empty():
            self.gen.get()
            self.gen.task_done()
        self.end = False
        self.mutation_rate = MUTATION_RATE
        self.mutation_probability = MUTATION_THRESHOLD

    def set_data(self, index):
        switcher = {
            1: f1_data,
            2: f2_data,
            3: f3_data
        }
        self.f_data = switcher.get(index)
        self.looking_for_function = index

    def initialize(self):
        self.g_no = 0
        g0 = generate_generation(size=MAX_POPULATION_SIZE)
        for p in g0:
            self.gen.put(
                (self.judge(p=p, f_data=self.f_data), 0, p))
        self.initialized.emit()
        self.start_time = time.monotonic()

    def finish(self):
        self.end = True

    def finalize_execution(self, p):
        if not self.end:
            print(f'found almost perfect individual')
        print(f'looking for function:{self.looking_for_function}')
        print(f'fitness of best individual: {p[0]}')
        print(f'g_no:{self.g_no}')
        f_x = (*(x[0] for x in self.f_data),)
        f_y = (*(x[1] for x in self.f_data),)
        f_f = (*(polimerize(x, p[2]) for x in f_x),)
        cummulative_error = 0
        for i, y in enumerate(f_y):
            error = abs(100 * (y - f_f[i]) / y)
            cummulative_error += error
            print(f'p{i:02d}: {f_f[i]:08f} vs {f_y[i]:08f}', end='')
            print(f' | error: {error:04f}%')
        print(f'avg error: {cummulative_error / len(f_y):08f}%')
        print(f'p(x): ', end='')
        print(f'{p[2].x6:04f}x^6 +', end='')
        print(f'{p[2].x5:04f}x^5 + ', end='')
        print(f'{p[2].x4:04f}x^4 + ', end='')
        print(f'{p[2].x3:04f}x^3 + ', end='')
        print(f'{p[2].x2:04f}x^2 + ', end='')
        print(f'{p[2].x1:04f}x + ', end='')
        print(f'{p[2].x0:04f}')
        print(f'END\n')
        self.finished.emit(p[2])

    def get_the_a_team(self, gen):
        tg = ()
        for i in range(5):
            p = gen[i][2]
            tg = (*tg, p)
        return tg

    def show_the_a_team(self, *, gen):
        print(f'gen[0]:{gen[0]}')
        print(f'gen[1]:{gen[1]}')
        print(f'gen[2]:{gen[2]}')
        print(f'gen[3]:{gen[3]}')
        print(f'gen[4]:{gen[4]}')
        print(f'')

    def start_crunching(self):
        while not self.end:
            i = 0
            tmp_gen = ()
            while not self.gen.empty():
                tmp_p = self.gen.get()
                if i < MAX_POPULATION_SIZE:
                    tmp_gen = (*tmp_gen, tmp_p)
                self.gen.task_done()
                i += 1

            should_update_ui = self.g_no % 50 == 0
            century = self.g_no % 100 == 0

            if should_update_ui:
                self.show_the_a_team(gen=tmp_gen)

            self.g_no += 1

            if century:
                for p in tmp_gen:
                    self.gen.put(p)
                tg = self.get_the_a_team(tmp_gen)
                self.generated.emit(tg, self.f_data, self.g_no)
                return

            fittest = tmp_gen[0][0]

            self.stuck = self.stuck_checker > 25

            poor_change = (self.previous_fitness - fittest * 100 <= 5)

            if poor_change:
                self.stuck_checker += 1

            if not poor_change:
                self.previous_fitness = fittest
                self.mutation_rate = MUTATION_RATE
                self.mutation_probability = MUTATION_THRESHOLD
                self.repeated_fitness = 0
            else:
                if century:
                    self.mutation_rate += 0.5
                if self.mutation_probability < MUTATION_CHANCE_SPACE / 2:
                    self.mutation_probability += 6
                self.repeated_fitness += 1

            if fittest <= ERROR_THRESHOLD:
                tg = self.get_the_a_team(tmp_gen)
                self.generated.emit(tg, self.f_data, self.g_no)
                self.finish()
                self.finalize_execution(tmp_gen[0])
                return

            self.make_new_polinomials(tmp_gen, self.f_data)
            time_so_far = time.monotonic() - self.start_time
            if time_so_far >= 300:
                self.finish()
                print(f'it\'s been :{time_so_far} (s)')
                tg = self.get_the_a_team(tmp_gen)
                self.generated.emit(tg, self.f_data, self.g_no)
                self.finish()
                self.finalize_execution(tmp_gen[0])
                return
        if self.end:
            return
        self.finish()
        tmp_gen = ()
        i = 0
        while not self.gen.empty() and i < 5:
            tmp_p = self.gen.get()
            tmp_gen = (*tmp_gen, tmp_p)
            self.gen.task_done()
            i += 1
        tg = self.get_the_a_team(tmp_gen)
        self.generated.emit(tg, self.f_data, self.g_no)
        self.finalize_execution(tmp_gen[0])
        return

    def mutate(self, poly):
        p = poly
        mutation_type = random.randint(0, 100)
        if mutation_type > 2:
            return self.make_polynomial(p=p, delta=self.mutation_rate)
        else:
            return Polinomial(
                round(p[0], 2),
                round(p[1], 2),
                round(p[2], 2),
                round(p[3], 2),
                round(p[4], 2),
                round(p[5], 2),
                round(p[6], 2)
            )

    def mix_genetic_material(self, *, g1, g2, i):
        switcher = {
            0: lambda: g1[i] - g2[i],
            1: lambda: g1[i] + g2[i],
            2: lambda: g1[i],
            3: lambda: g2[i],
            4: lambda: g1[i] - (g1[i] + g2[i]) / 2,
            5: lambda: g1[i] + (g1[i] + g2[i]) / 2,
            6: lambda: (g1[i] - g2[i]) / 2,
            7: lambda: (g1[i] + g2[i]) / 2,
            8: lambda: g1[i] + 1,
            9: lambda: g2[i] + 1,
            10: lambda: g1[i] - 1,
            11: lambda: g2[i] - 1,
            12: lambda: (g1[i] + g2[i]) / 2,
            13: lambda: g2[i] * 0.75,
            14: lambda: g1[i] * 0.75,
            15: lambda: (g2[i] + g1[i]) * 0.7
        }
        switch = random.getrandbits(4)  # from 0 to 7
        res = switcher.get(switch)()

        return 0 if abs(res) < 1e-4 else round(res, 6)

    def judge(self, *, p, f_data):
        """
        the lower the fitness, the better (the more fit it is)
        """
        fitness = 0
        for point in f_data:
            f_f = polimerize(point[0], p)
            y = point[1]
            fitness += abs(100 * (y - f_f) / y)
        return fitness / len(f_data)

    def mix(self, *, ind1, ind2):
        p = Polinomial(
            self.mix_genetic_material(g1=ind1, g2=ind2, i=0),  # x ^ 6
            self.mix_genetic_material(g1=ind1, g2=ind2, i=1),  # x ^ 5
            self.mix_genetic_material(g1=ind1, g2=ind2, i=2),  # x ^ 4
            self.mix_genetic_material(g1=ind1, g2=ind2, i=3),  # x ^ 3
            self.mix_genetic_material(g1=ind1, g2=ind2, i=4),  # x ^ 2
            self.mix_genetic_material(g1=ind1, g2=ind2, i=5),  # x ^ 1
            self.mix_genetic_material(g1=ind1, g2=ind2, i=6),  # x ^ 0
        )

        self.gen.put((self.judge(p=p, f_data=self.f_data), 0, p))

        if random.randint(0, 100) < self.mutation_probability:
            switcher = {
                0: ind1,
                1: ind2,
                2: p
            }
            mutant = self.mutate(switcher.get(random.randint(0, 2)))
            self.gen.put((self.judge(p=mutant, f_data=self.f_data), 0, mutant))

    def make_polynomial(self, *, p, delta):
        rng = random.uniform
        return Polinomial(
            rng(p[0] - delta, p[0] + delta),
            rng(p[1] - delta, p[1] + delta),
            rng(p[2] - delta, p[2] + delta),
            rng(p[3] - delta, p[3] + delta),
            rng(p[4] - delta, p[4] + delta),
            rng(p[5] - delta, p[5] + delta),
            rng(p[6] - delta, p[6] + delta)
        )

    def make_new_polinomials(self, gen, f_data):
        if self.stuck:
            for i in range(len(gen)):
                for j in range(50):
                    _, _, s = gen[i]
                    p = self.make_polynomial(p=s, delta=((j + 1) * 0.001))
                    self.gen.put((self.judge(p=p, f_data=f_data), 0, p))
            self.gen.put(gen[0])
            self.stuck = False
            self.stuck_checker = 0
        else:
            for p in gen:
                self.gen.put(p)
            for _ in range(MAX_POPULATION_SIZE):
                select1 = random.randint(0, int((MAX_POPULATION_SIZE / 2) - 1))
                select2 = select1
                while select2 == select1:
                    select2 = random.randint(0, MAX_POPULATION_SIZE / 2 - 1)
                _, _, i1 = gen[select1]
                _, _, i2 = gen[select2]
                self.mix(ind1=i1, ind2=i2)


def generate_generation(*, size):
    gen = ()
    for _ in range(size):
        gen = (*gen,
               Polinomial(
                   random.uniform(-5.0, 5.0),  # x ^ 6
                   random.uniform(-5.0, 5.0),  # x ^ 5
                   random.uniform(-5.0, 5.0),  # x ^ 4
                   random.uniform(-5.0, 5.0),  # x ^ 3
                   random.uniform(-5.0, 5.0),  # x ^ 2
                   random.uniform(-5.0, 5.0),  # x ^ 1
                   random.uniform(-5.0, 5.0)   # x ^ 0
               )
               )
    return gen
