amount = 2
beta = 0.9
eta = 0.05
a_half = 40
phi_age = 0.6
phi_weight = 0.1
w_half = 10
mu = 0.25
sigma_birth = 1.5



import math
import numpy as np


class Herbivore:
    """ Creating the herbivore class
Requirements:
- age
- weight
- fitness
- position
- alive
- eating_result
- species
"""
    params = {'w_birth': 8.,
              'sigma_birth': 1.5,
              'beta': 0.9,
              'eta': 0.05,
              'a_half': 40.,
              'phi_age': 0.2,
              'w_half': 10.,
              'phi_weight': 0.1,
              'mu': 0.25,
              'gamma': 0.2,
              'zeta': 3.5,
              'xi': 1.2,
              'omega': 0.4,
              'F': 10.}

    def __init__(self):
        self.age = 0
        self.weight = self.initial_weight()
        self.recompute_fitness = True
        self.fitness = self.fitness_method()
        self.position = 0
        self.alive = True
        self.eating = 0
        self.species = 0

    def eat(self):
        self.eating += amount
        self.update_weight("increase")
        self.recompute_fitness = True
        self.fitness_method()

    def grow_older(self):
        self.age += 1
        self.update_weight("decrease")
        self.recompute_fitness = True
        self.fitness_method()

    @classmethod
    def initial_weight(cls):
        """
        initialize the weights based on the normal distribution
        :return: initial weight
        """
        rn = np.random.normal(cls.params['w_birth'], cls.params['sigma_birth'])
        return rn

    def update_weight(self, direction):
        if direction == "increase":
            self.weight += self.params['beta'] * self.params['F']

        elif direction == "decrease":
            self.weight -= self.params['eta'] * self.weight

        else:
            raise ValueError("ValueError exception thrown: Not correct word")

    @staticmethod
    def _fitness_formula(age, weight, params):
        q1 = 1 / (1 + math.exp(params['phi_age'] * (age - params['a_half'])))
        q2 = 1 / (1 + math.exp(-1 * (params['phi_weight'] * (weight - params['a_half']))))
        return q1*q2

    def calculate_fitness(self):
        if self.weight == 0:
            self.fitness = 0
        else:
            self.fitness = self._fitness_formula(self.age, self.weight, self.params)

    def fitness_method(self):
        if self.recompute_fitness:
            self.calculate_fitness()
            self.recompute_fitness = False
        return self.fitness

    def get_weight(self):
        return self.weight

    def get_age(self):
        return self.age

    def get_fitness(self):
        return self.fitness
