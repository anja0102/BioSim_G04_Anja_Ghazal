from biosim.animal import Herbivore, Carnivore
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
        self.newborn_carn_list=[]
        self.available_fodder = 0

    def place_animals(self, listof):
        for dct in listof:
            if dct.get("species") == 'Herbivore':
                age = dct.get("age")
                weight = dct.get("weight")
                animal = Herbivore(age=age, weight=weight)
                self.herbivores_list.append(animal)

            if dct.get("species") == 'Carnivore':
                age = dct.get("age")
                weight = dct.get("weight")
                animal = Carnivore(age=age, weight=weight)
                self.carnivores_list.append(animal)



    def animals_die(self):
        # animal_list_c = self.herbivores_list.copy()
        # print(animal_list_c)
        survivors_h = [animal for animal in self.herbivores_list if not animal.is_dying()]
        self.herbivores_list = survivors_h

        survivors_c = [animal for animal in self.carnivores_list if not animal.is_dying()]
        self.carnivores_list = survivors_c

        # print(self.herbivores_list)

    def herb_eat(self):
        # herbivore feeding
        np.random.shuffle(self.herbivores_list)
        for animal in self.herbivores_list:
            if self.available_fodder >= animal.get_F():
                self.available_fodder -= animal.eat()
            elif animal.get_F() > self.available_fodder > 0:
                animal.eat(self.available_fodder)
                self.available_fodder = 0

    def carn_eat(self):
        #Carnivore feeding


        #sort herbivores: Lowest to highest fitness
        self.herbivores_list.sort(key=lambda x: x.calculate_fitness())

        #sort carnivores: Highest to lowest fitness
        self.carnivores_list.sort(key=lambda x: x.calculate_fitness(), reverse=True)


        for carnivore in self.carnivores_list:
            eaten_herbivores = carnivore.eat(self.herbivores_list)
            herb_survivors = [animal for animal in self.herbivores_list if animal not in eaten_herbivores]
            #Improvement for later: check if herb_survivors needs to be sorted before sorting
            herb_survivors.sort(key=lambda x: x.calculate_fitness())
            self.herbivores_list = herb_survivors


    def animals_eat(self):
        self.herb_eat()
        self.carn_eat()

    def procreation(self):
        """
        Checks if there are at least one other animal of the same species in this cell
        and having proper weight for both
        then they will make a new offspring.
        Returns
        -------

        """
        for animal in self.herbivores_list:
            offspring = animal.create_newborn(len(self.herbivores_list))
            if offspring is not None:
                self.newborn_herb_list.append(offspring)

        for animal in self.carnivores_list:
            offspring = animal.create_newborn(len(self.carnivores_list))
            if offspring is not None:
                self.newborn_carn_list.append(offspring)

        self.add_newborn_to_fauna() #adding newborn to fauna after all animans procreate to not add on iterating list

    #Maybe delete this?
    def create_new_animal(self, newborn_weight):
        new_animal = Herbivore(weight=newborn_weight, age=0)
        self.newborn_herb_list.append(new_animal)

    def add_newborn_to_fauna(self):
        self.herbivores_list.extend(self.newborn_herb_list)
        self.newborn_herb_list = []

        self.carnivores_list.extend(self.newborn_carn_list)
        self.newborn_carn_list = []

    def animals_age_by_one_year(self):
        for animal in self.herbivores_list:
            animal.grow_older()

        for animal in self.carnivores_list:
            animal.grow_older()

    def animals_update_weight_annual(self):
        for animal in self.herbivores_list:
            animal.update_weight("decrease")

        for animal in self.carnivores_list:
            animal.update_weight("decrease")

    def migrate(self):
        pass

    def get_fodder(self):
        return self.available_fodder

    def get_num_herb_animals(self):
        return len(self.herbivores_list)

    def get_num_carn_animals(self):
        return len(self.carnivores_list)

class Water(Cell):
    def __init__(self):
        self.animals = []
        self.available_fodder = 0

    def set_fodder(self):
        self.available_fodder = 0


class Desert(Cell):
    def __init__(self):
        self.available_fodder = 0

    def set_fodder(self):
        self.available_fodder = 0


class Highland(Cell):
    def __init__(self):
        self.available_fodder = 300

    def set_fodder(self):
        self.available_fodder = 300


class Lowland(Cell):
    def __init__(self):
        super().__init__()
        self.available_fodder = 800

    def set_fodder(self):
        self.available_fodder = 800


#if __name__ == "__main__":
