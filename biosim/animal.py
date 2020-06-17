import math
import numpy as np


class Animal:
    """
    Animal class, where one object represents one animal
    Has two subclasses of different animal species, Carnivores and Herbivores.
    The most distinct difference between the two subclasses: the eating-method.

    """
    params = {}

    def __init__(self, age=None, weight=None):
        """
        Constructor for the class, if weight or age initialized their value is set.
        If no value is given;
        initial value for age would be 0 and
        initial value for weight is extracted from the initial_weight method.
        Specifying invalid age or weight values will raise a a value error.
        Initial fitness is set to zero.

        Parameters
        ----------
        age : int
        weight : float

        """
        if age is None:
            self.age = 0
        else:
            self.raise_non_valid_attribute('Age', age)
            self.age = age

        if weight is None:
            self.weight = self.initial_weight()
        else:
            self.raise_non_valid_attribute('Weight', weight)
            self.weight = weight

        self.has_migrated_this_year = False

    @classmethod
    def set_given_parameters(cls, parameters):
        """
        Set the user defined parameter values for Animal object.
        Includes check for valid parameter values

        Parameters
        ----------
        parameters: dict
        """

        for parameter in parameters:
            if parameter in cls.params:
                if parameter == 'eta' and parameters['eta'] > 1:
                    raise ValueError('Illegal parameter value, eta '
                                     'can\'t be more than 1')
                if parameter == 'DeltaPhiMax' and parameters[parameter] <= 0:
                    raise ValueError('Illegal parameter value, ' +
                                     str(parameter) + ' can\'t be zero or negative')
                if parameters[parameter] < 0:
                    raise ValueError('Illegal parameter value, ' +
                                     str(parameter) + ' can\'t be negative')
                else:
                    cls.params[parameter] = parameters[parameter]
            else:
                raise RuntimeError('Unknown parameter, ' + str(parameter) +
                                   ' can\'t be set')

    def grow_older(self):
        """
        Animal object grows one year older:
        increasing age by 1,
        updating the weight by annual weight loss,
        setting the "has_migrated_this_year" value to False
        """
        self.age += 1
        self.update_weight("decrease")
        self.has_migrated_this_year = False

    @classmethod
    def initial_weight(cls):
        """
        initialize the weights class attribute based on the normal distribution

        Returns
        -------
        Initial weight: float
            random number drawn from normal distribution

        """

        return np.random.normal(cls.params['w_birth'], cls.params['sigma_birth'])

    def update_weight(self, direction, amount=None):
        """
        This method updates the weight attribute.
        If it should be decreased or increased is specified by "Direction".
        The weight is updated based amount specified by argument.

        Parameters
        ----------
        direction: string
            direction of weight update (increase or decrease)
        amount : float
            amount eaten by the animal, which influences the weight update

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
        Computes fitness according to the formula:
        Phi = q(-1, a, a_half, phi_age)*q(+1, w, w_half, phi_weight)
        and 0=< Phi =< 1

        Parameters
        ----------
        age :  int
        weight : float
        params : dict
            class dictionary "params"

        Returns
        -------
        q1*q2: float
            the fitness of the animal calculated from fitness formula

        """
        q1 = 1 / (1 + math.exp(1 * params['phi_age'] * (age - params['a_half'])))
        q2 = 1 / (1 + math.exp(-1 * (params['phi_weight'] * (weight - params['w_half']))))
        return q1*q2

    def calculate_fitness(self):
        """
        Calculate the fitness of an Animal. I weight is zero, fitness is always zero.
        Else, fitness is calculated based on fitness formula.

        Returns
        -------
        fitness: float
            the fitness of the animal object

        """
        if self.weight == 0:
            return 0
        else:
            return self._fitness_formula(self.age, self.weight, self.params)

    @staticmethod
    def from_prob_to_binary(prob):
        """
        Converts a probability to a binary value (True or False).

        Parameters
        ----------
        prob: float
            between 0 and 1

        Returns
        -------
        binary: boolean
            True or False based on random number and probability
        """
        rand_nbr = np.random.random()
        if rand_nbr < prob:
            return True
        else:
            return False

    def check_mating_weight_conditions(self, num_animals):
        """
        Method to check if animals weight conditions for mating is satisfied.

        Parameters
        ----------
        num_animals: int
            number of animals of same species in cell.
            Mating partner exists if num_animals >= 2

        Returns
        -------
        binary: boolean
            True or False based on condition checks
        """
        if num_animals >= 2:
            weight_condition = self.params['zeta'] * (self.params['w_birth'] +
                                                      self.params['sigma_birth'])
            if self.weight > weight_condition:
                return True
        return False

    def check_mother_minus_newborn_weight_conditions(self, newborn_weight):
        """
        Method to check conditions for mating is satisfied.
        Checking that mothers weight can handle the weight reduction that comes from creating an offspring.
        If the weight reduction is survivable for the mother,
        the weight is reduced by this amount and a True-value is returned.

        Parameters
        ----------
        newborn_weight: float
            the weight of a possible offspring

        Returns
        -------
        binary: boolean
            True or False based on condition checks
        """
        if self.weight >= self.params['xi'] * newborn_weight:
            # Reduce weight of mother by the weight of newborn * xi
            self.weight -= self.params['xi'] * newborn_weight
            return True
        else:
            return False

    def create_newborn(self, num_animals):
        """
        Creates a new animal based on several condition checks. If all checks passed:
        create a new animal of the same class as mother-animal, and return the newborn object.
        Parameters
        ----------
        num_animals: int
            Number of animals of same species in current cell

        Returns
        -------
        newborn: object
            if no newborn object is created, returns None

        """
        if self.check_mating_weight_conditions(num_animals):
            prob = min(1, self.params['gamma'] * self.calculate_fitness() * (num_animals - 1))
            creating = self.from_prob_to_binary(prob)
            if creating:
                newborn = self.__class__()
                if self.check_mother_minus_newborn_weight_conditions(newborn.weight):
                    return newborn
        return None

    def is_dying(self):
        """
        Checks if animal object is dying based on probability calculated form formula:
        p = omega ( 1 - fitness)
        It weight is zero, the animal will die.

        Returns
        -------
        binary: boolean
            True if animal must die, False if not.
        """
        if self.weight <= 0:
            return True
        prob = self.params['omega'] * (1 - self.calculate_fitness())
        # print('prob inside is_dying, fitness', prob, self.calculate_fitness())
        return self.from_prob_to_binary(prob)

    def check_if_migrates(self):
        """
        Checks if an animal will migrate. The animal can only migrate once a year.
        Probability of migration is calculated from formula p = mu * fitness

        Returns
        -------
        binary: boolean
            Returns True if animal migrates, False if not.

        """
        if self.has_migrated_this_year:
            return False

        prob = self.params['mu']*self.calculate_fitness()
        will_migrate = self.from_prob_to_binary(prob)

        if will_migrate:
            self.has_migrated_this_year = True
            return True
        else:
            return False

    @staticmethod
    def raise_non_valid_attribute(attribute_name, attribute):
        """
        Raise an error if the input is of invalid type

        Parameters
        ----------
        attribute_name : str
        attribute : value of the attribute
        """
        if not isinstance(attribute, (int, float)):
            raise ValueError(attribute_name + ' of animal can\'t be set to '
                             + attribute_name +
                             ', it has to be integer or float')

    def get_weight(self):
        """
        Gets the weight of an animal object

        Returns
        -------
        weight: float
        """
        return self.weight

    def get_param_f(self):
        """
        Gets the parameter value F for animal object
        Returns
        -------
        parameter value F: float
        """
        return self.params['F']


class Herbivore(Animal):
    """
    Herbivore subclass of Animal Base Class
    """

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
        Constructor for the Herbivore subclass of Animal base class.
        Parameters
        ----------
        age: int
        weight: float
        """
        super().__init__(age, weight)

    def eat(self, amount=None):
        """
        Eat method for Herbivores.
        Herbivores eat a specific amount.
        If not specified, its value will be chosen based on the standard parameters for herbivore
        class. When the animal eats, the weight is updated accordingly:
        weight change = beta * amount.

        Parameters
        ----------
        amount : float

        Returns
        -------
        amount of food the herbivore consumed.

        """
        if amount is None:
            amount = self.params['F']

        self.weight += self.params['beta'] * amount
        return amount


class Carnivore(Animal):
    """
    Carnivore subclass of Animal Base Class
    """

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
        Constructor for the Carnivore subclass of Animal base class.

        Parameters
        ----------
        age: int
        weight: float
        """
        super().__init__(age, weight)

    def check_carn_prey(self, herb_fitness, carn_fitness):
        """
        Check assessing if a carnivore can prey on a herbivore.
        Condition is based on both animals fitness.
        Probability of carnivore hunting the herbivore is:
        p = (carnivore_fitness - herbivore_fitness ) DeltaPhiMax,
        where deltaPhiMax is given in the Params dictionary

        Parameters
        ----------
        herb_fitness: float
        carn_fitness: float

        Returns
        -------
        binary: boolean
            Returns True if carnivore can prey on herbivore, False if not.
        """

        if carn_fitness <= herb_fitness:
            return False

        elif (carn_fitness-herb_fitness) < self.params['DeltaPhiMax'] > 0:
            prob = (carn_fitness-herb_fitness) / self.params['DeltaPhiMax']
            return self.from_prob_to_binary(prob)

        else:
            return True

    def eat(self, herb_list):
        """
        Eat method for Carnivores.
        Loops through a list of all available herbivores, checks if the carnivore preys on it.
        If the carnivore eats the herbivore, its appended to the eaten_herbs list, to be returned.
        The weight and fitness is updates for every animal the carnivore eats, and the
        carnivore never eats more than the appetite parameter F, set in the Params dictionary.

        Parameters
        ----------
        herb_list: list
            list of all available herbivores in cell

        Returns
        -------
        eaten_herbs: List
            List of all the eaten herbivores.
            List is returned empty if no Herbivore were eaten by the Carnivore
        """
        eaten_herbs = []
        remaining_appetite = self.params['F']

        for herbivore in herb_list:
            if self.check_carn_prey(herbivore.calculate_fitness(), self.calculate_fitness()):
                eaten_herbs.append(herbivore)

                if remaining_appetite - herbivore.weight >= 0:
                    weight_to_eat = herbivore.weight

                else:
                    weight_to_eat = remaining_appetite

                remaining_appetite -= weight_to_eat
                self.weight += self.params['beta'] * weight_to_eat

            if remaining_appetite == 0:  # if no remaining appetite
                return eaten_herbs

        return eaten_herbs
