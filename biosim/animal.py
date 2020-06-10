import math
import numpy as np


class Animal:
    """
    Creating the animal class
    Fauna which are common among herbivores and carnivores are listed as methods in Animal
    class

    """
    params = {}

    def __init__(self, age=None, weight=None):
        """
        Constructor for the class, if weight or age initialized their value is set
        if not, initial value for age would be 0 and for weight would be extracted
        from the initial_weight method.
        Parameters
        ----------
        age : int
        weight : int

        """
        if age is None:
            self.age = 0
        else:
            # CHECK VALUE ERROR
            self.age = age

        if weight is None:
            self.weight = self.initial_weight()
        else:
            # CHECK VALUE ERROR
            self.weight = weight

    # Move this down to herb class, since not used by carnivores
    def eat(self, amount=None):
        """
        Herbivores eat based on the specific amount. If amount is initialized the value would
        be set. If not its value will be chosen based on the standard parameters for herbivore
        class
        Parameters
        ----------
        amount : int

        Returns
        -------
        amount of food the herbivore consumed.

        """
        if amount is None:
            amount = self.params['F']

        self.weight += self.params['beta'] * amount
        return amount

    def grow_older(self):
        """
        When the method is called the animal grows older for one year

        """
        self.age += 1
        self.update_weight("decrease")

    @classmethod
    def initial_weight(cls):
        """
        initialize the weights based on the normal distribution

        Returns
        -------
        Initial weight

        """
        rn = np.random.normal(cls.params['w_birth'], cls.params['sigma_birth'])
        return rn

    def update_weight(self, direction, amount=None):
        """
        This method determines if the weight should either be decreased or increased.
        In addition it updates the weight based on the parameters been given to.
        Parameters
        ----------
        direction
        amount : int

        """
        if amount is None:
            amount = self.params['F']

        if direction == "increase":
            self.weight += self.params['beta'] * amount

        elif direction == "decrease":
            self.weight -= self.params['eta'] * self.weight

        else:
            raise ValueError("ValueError exception thrown: Not correct word")

    @staticmethod
    def _fitness_formula(age, weight, params):
        """
        The formula which would be used to calculate the fitness
        Parameters
        ----------
        age :  int
        weight : int
        params : int

        Returns
        -------
        Output of fitness formula

        """
        q1 = 1 / (1 + math.exp(params['phi_age'] * (age - params['a_half'])))
        q2 = 1 / (1 + math.exp(-1 * (params['phi_weight'] * (weight - params['w_half']))))
        return q1*q2

    def calculate_fitness(self):
        """

        Returns
        -------

        """
        if self.weight == 0:
            return 0
        else:
            return self._fitness_formula(self.age, self.weight, self.params)

    def from_prob_to_binary(self, prob):
        rand_nbr = np.random.random()
        if rand_nbr < prob:
            return True
        else:
            return False

    def check_mating_weight_conditions(self, num_animals):
        if num_animals >= 2:
            weight_condition = self.params['zeta'] * (self.params['w_birth'] + self.params['sigma_birth'])
            if self.weight > weight_condition:
                return True
            else:
                return False
        else:
            return False

    def check_mother_minus_newborn_weight_conditions(self, newborn_weight):
        if self.weight >= self.params['xi'] * newborn_weight:
            # Reduce weight of mother by the weight of newborn * xi
            self.weight -= self.params['xi'] * newborn_weight
            return True
        else:
            return False

    def create_newborn(self, num_animals):
        if self.check_mating_weight_conditions(num_animals):
            prob = min(1, self.params['gamma'] * self.calculate_fitness() * (num_animals - 1))
            creating = self.from_prob_to_binary(prob)
            if creating:
                newborn = self.__class__()  # OBS HOW TO MAKE THE ANIMAL OBJECT OF CORRECT SPECIES
                if self.check_mother_minus_newborn_weight_conditions(newborn.weight):
                    return newborn
            else:
                return None

    def is_dying(self):
        if self.weight <= 0:
            return True
        prob = self.params['omega'] * (1 - self.calculate_fitness())
        # print('prob inside is_dying, fitness', prob, self.calculate_fitness())
        return self.from_prob_to_binary(prob)

    def get_weight(self):
        return self.weight
    #
    # def get_age(self):
    #     return self.age

    # def get_fitness(self):
    #     return self.fitness

    def get_F(self):
        return self.params['F']

    # def get_initial_weight(self):
    #     return self.initial_weight()


class Herbivore(Animal):
    # HERBIVORE PARAMS HERE
    params = {'w_birth': 8.,
              'sigma_birth': 1.5,
              'beta': 0.9,
              'eta': 0.05,
              'a_half': 40.,
              'phi_age': 0.6,
              'w_half': 10.,
              'phi_weight': 0.1,
              'mu': 0.25,
              'gamma': 0.2,
              'zeta': 3.5,
              'xi': 1.2,
              'omega': 0.4,
              'F': 10.}

    def __init__(self, age=None, weight=None):
        """
        subclass of Animal class.
        Parameters
        ----------
        age: int
        weight: float
        """
        super().__init__(age, weight)


class Carnivore(Animal):
    # CARNIVORE params
    params = {'w_birth': 6.,
              'sigma_birth': 1.0,
              'beta': 0.75,
              'eta': 0.125,
              'a_half': 40.,
              'phi_age': 0.3,
              'w_half': 4.,
              'phi_weight': 0.4,
              'mu': 0.4,
              'gamma': 0.8,
              'zeta': 3.5,
              'xi': 1.1,
              'omega': 0.8,
              'F': 50.,
              'DeltaPhiMax': 10.}

    def __init__(self, age=None, weight=None):
        """
        subclass of Animal class.
        Parameters
        ----------
        age: int
        weight: float
        """
        super().__init__(age, weight)

    # Carnivore eating method

    def check_carn_prey(self, herb_fitness, carn_fitness):

        if carn_fitness <= herb_fitness:
            return False

        elif (carn_fitness-herb_fitness) < self.params['DeltaPhiMax'] > 0:
            prob = (carn_fitness-herb_fitness) / self.params['DeltaPhiMax']
            return self.from_prob_to_binary(prob)

        else:
            return True

    def eat(self, herb_list):
        eaten_herbs = []

        for herbivore in herb_list:
            if self.check_carn_prey(herbivore.calculate_fitness(), self.calculate_fitness()):
                eaten_herbs.append(herbivore)
                self.weight += self.params['beta'] * herbivore.weight

            if sum(herb.weight for herb in eaten_herbs) >= self.params['F']:
                return eaten_herbs

        return eaten_herbs

# if __name__ == "__main__":
#     num_animals=2
#     h = Animal()
#     print(h.age)
#     print(h.weight)
#     print(h.fitness)
#     for i in range(30):
#         h.eat()
#     # h.if_create_new_born(num_animals)
#     print(h.check_if_will_create_newborn(num_animals, 10))
