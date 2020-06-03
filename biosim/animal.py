amount = 2
beta = 0.9
eta = 0.05


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

    def __init__(self):
        self.age = 0
        self.weight = 8
        self.fitness = 0
        self.position = 0
        self.alive = True
        self.eating = 0
        self.species = 0

    def eat(self):
        self.eating =+ amount
        self.update_weight("increase")
        self.update_fitness()

    def get_older(self):
        self.age += 1
        self.update_weight("decrease")
        self.update_fitness()

    def update_weight(self, direction):
        if direction == "increase":
            self.weight += beta*amount

        elif direction == "decrease":
            self.weight -= eta * self.weight

        else:
            raise ValueError("ValueError exception thrown: Not correct word")

    def update_fitness(self):
        if self.weight == 0:
            self.fitness = 0
        else:
            self.fitness += 1

    def get_weight(self):
        return self.weight

    def get_age(self):
        return self.age

    def get_fitness(self):
        return self.fitness

