from numpy import linspace, sin, cos
import math
import matplotlib.pyplot as plt

x_start = 0
x_end = 2 * math.pi

slices = 1000


def main():
    x = linspace(x_start, x_end, slices)

    a = sin((*x,))
    b = cos((*x,))
    c = a + b
    d = a - b
    e = (a + b) / 2

    plt.plot((*x,), a, 'red')
    plt.plot((*x,), b, 'green')
    plt.plot((*x,), c, 'blue')
    plt.plot((*x,), d, 'orange')
    plt.plot((*x,), e, 'yellow')

    plt.savefig('plot.png')


if __name__ == '__main__':
    main()
