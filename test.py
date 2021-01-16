import numpy as np
from matplotlib import pyplot as plt


def PolyCoefficients(x, coeffs):
    """ Returns a polynomial for ``x`` values for the ``coeffs`` provided.

    The coefficients must be in ascending order (``x**0`` to ``x**o``).
    """
    o = len(coeffs)
    print(f'# This is a polynomial of order {ord}.')
    y = 0
    for i in range(o):
        y += coeffs[i] * x ** i
    return y


def main():
    start = 0
    end = 9
    slices = 100
    x = np.linspace(start, end, slices, endpoint=False)
    coeffs = (1, 2, 3, 4, 5)
    plt.plot(x, PolyCoefficients(x, coeffs))

    plt.savefig('test.png')


if __name__ == '__main__':
    main()
