from math import sqrt
from random import randint, uniform, seed
from secrets import choice
from typing import Callable, Tuple


class DiferentialEvolution:

    def __init__(self, seed_number, domain) -> None:
        seed(seed_number)
        self.F = uniform(0.4, 0.9)
        self.c = uniform(0.1, 1)
        self.domain = domain
        self.population = []

    def random_solution(self):
        return (uniform(self.domain[0],
                        self.domain[1]), uniform(self.domain[0],
                                                 self.domain[1]))

    def initial_population(self, length):
        self.population = [self.random_solution() for _ in range(length)]
        return self.population

    def distance(self, pointA, pointB):
        x1, y1 = pointA
        x2, y2 = pointB
        return sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def add_scalar(self, vector, scalar):
        return tuple(x + scalar for x in vector)

    def iteration(self, evaluate: Callable):
        test_vectors = []
        for individual in self.population:
            xr1 = choice(self.population)
            xr2 = choice(self.population)
            xr3 = choice(self.population)
            while xr1 == individual:
                xr1 = choice(self.population)
            while xr2 == individual or xr2 == xr1:
                xr2 = choice(self.population)
            while xr3 == individual or xr3 == xr2 or xr3 == xr1:
                xr3 = choice(self.population)
            v = self.add_scalar(xr1, self.distance(xr2, xr3)*self.F)
            u = [g for g in individual]
            rd = randint(0, 2)
            for d in range(2):
                r = uniform(0, 1)
                if r < self.c or d == rd:
                    u[d] = v[d]
            test_vectors.append(tuple(g for g in u))

        self.population = [
            test_vectors[i]
            if evaluate(test_vectors[i]) < evaluate(self.population[i]) else self.population[i]
            for i in range(len(test_vectors))
        ]
    
    def get_best(self, evaluate: Callable):
        min_point = None
        for individual in self.population:
            if min_point == None or evaluate(min_point) > evaluate(individual):
                min_point = individual
        return min_point

    def get_worst(self, evaluate: Callable):
        max_point = None
        for individual in self.population:
            if max_point == None or evaluate(max_point) < evaluate(individual):
                max_point = individual
        return max_point
