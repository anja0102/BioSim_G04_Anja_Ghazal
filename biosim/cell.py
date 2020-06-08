from biosim.animal import Herbivore
import numpy as np


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
        self.herbivores_list = []
        self.carnivores_list = []
        self.newborn_herb_list=[]
        self.available_fodder = 0

    def place_animals(self, listof):
        for dict in listof:
            if dict.get("species") == 'Herbivore':
                age=dict.get("age")
                weight=dict.get("weight")
                animal = Herbivore(age=age, weight=weight)
                self.herbivores_list.append(animal)

    def randomise_list(self):
        rnd_list = self.herbivores_list.copy()
        np.random.shuffle(rnd_list)
        return rnd_list

    def animals_die(self):
        animal_list_c = self.herbivores_list.copy()
        self.herbivores_list = [animal for animal in animal_list_c if not animal.is_dying()]

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
        for animal in self.herbivores_list:
            newborn_weight = animal.get_initial_weight()
            if animal.check_if_will_create_newborn(len(self.herbivores_list), newborn_weight):
                self.create_new_animal(newborn_weight)

        self.add_newborn_to_fauna() #adding newborn to fauna after all animans procreate to not add on iterating list

    def create_new_animal(self, newborn_weight):
        new_animal = Herbivore(weight=newborn_weight, age=0)
        self.newborn_herb_list.append(new_animal)

    def add_newborn_to_fauna(self):
        self.herbivores_list.extend(self.newborn_herb_list)

    def animals_age_by_one_year(self):
        for animal in self.herbivores_list:
            animal.grow_older()

    def animals_update_weight_annual(self):
        for animal in self.herbivores_list:
            animal.update_weight("decrease")

    def migrate(self):
        pass

    def get_fodder(self):
        return self.available_fodder

    def get_num_animals(self):
        return len(self.herbivores_list)


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


#if __name__ == "__main__":
