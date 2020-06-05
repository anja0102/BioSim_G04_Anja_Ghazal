from biosim.animal import Animal
import numpy as np
from numpy import random


class BioSim:
    pass


class Island:
    """
    - age
    - cells of type "celltype"
    - animals (inside celltype)
    -
    :return:
    """

    def __init__(self):
        self.cell_list = []  # list to be populated in biosim class

    # def grow_fodder:
    #    for cell in cell_list:
    #        cell.set_fodder()

    def feed_animals(self):
        for cell in cell_list:
            cell.animals_eat()

    def procreation(self):
        pass

    def migration(self):
        pass

    def aging(self):
        pass

    def loose_weight(self):
        pass

    def death(self):
        pass

    # def eating for every cell


class Cell:
    """
    Creating cell structure to describe properties in every square (cell)
    Common for all cells:
     - coordinates
     - edge_cells for migration
     - animals
     - fodder_amount
     -

    :return:
    """

    def __init__(self):
        self.animal_list = []
        self.available_fodder = 0

    def place_animals(self):
        pass

    def randomise_list(self):
        rnd_list = self.animal_list.copy()
        np.random.shuffle(rnd_list)
        return rnd_list

    def animals_eat(self):  # herbivore feeding
        randomized_order = self.randomise_list()
        for animal in randomized_order:
            if self.available_fodder >= animal.get_F():
                self.available_fodder -= animal.eat()

    def procreation(self):
        """
        Checks if there are at least one other animal of the same species in this cell
        and having proper weight for both
        then they will make a new offspring.
        Returns
        -------

        """
        for animal in self.animal_list:
            newborn_weight = animal.get_initial_weight()
            if animal.check_if_will_create_newborn(len(self.animal_list), newborn_weight):
                self.create_new_animal(newborn_weight)

    def create_new_animal(self, newborn_weight):
        new_animal = Animal(weight=newborn_weight)
        self.animal_list.append(new_animal)

    def animal_death(self):
        pass

    def migrate(self):
        pass

    def get_fodder(self):
        return self.available_fodder

    def get_num_animals(self):
        return len(self.animal_list)


class Water(Cell):
    def __init__(self):
        self.animals = []
        self.available_fodder = 0

    def set_fodder(self):
        self.available_fodder = 0


class Desert(Cell):
    def __init__(self):
        self.animals = []
        self.available_fodder = 0

    def set_fodder(self):
        self.available_fodder = 0


class Highland(Cell):
    def __init__(self):
        self.animals = []
        self.available_fodder = 300

    def set_fodder(self):
        self.available_fodder = 300


class Lowland(Cell):
    def __init__(self):
        super().__init__()
        self.animals = []
        self.available_fodder = 800

    def set_fodder(self):
        self.available_fodder = 800


if __name__ == "__main__":
    a=Animal()
    b=Animal()
    c=Lowland()
    c.animal_list.append(a)
    c.animal_list.append(b)

    print(c.get_fodder())
    for _ in range(30):
        c.animals_eat()
    print(c.get_fodder())

    print(c.get_num_animals())
    c.procreation()
    print(c.get_num_animals())