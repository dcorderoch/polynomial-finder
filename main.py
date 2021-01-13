#!/usr/bin/env python3

from genal import genal

def main():
    print(f'start a generation')
    print(f'calculate population\'s fitness')
    print(f'select mating pool')
    print(f'do crossover')
    print(f'check if going to mutate')
    print(f'do mutation')
    print(f'kill the weak ones')
    print(f'check the fitness against confidence level/error')
    print(f'if candidate is a chad, or too many generations, finish')

if __name__ == '__main__':
    genal.run()
