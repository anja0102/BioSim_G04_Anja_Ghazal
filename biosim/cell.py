# -*- coding: utf-8 -*-

__author__ = "Anja Stene, Student NMBU", "Ghazal Azadi, Student NMBU"
__email__ = "anja.stene@nmbu.no", "ghazal.azadi@nmbu.no"

from biosim.animal import Herbivore, Carnivore
import numpy as np


class Cell:
    """
    Cell class where the object works as a building block for Island.
    It has four subclasses: Water, Highland, Lowland, Desert inherited from the base class.
    Baseclass contains functionality that is common for all cells types.
    """
    def __init__(self):
        """
        Constructor for the class, all attributes start off as empty lists.
        """
        self.herbivores_list = []
        self.carnivores_list = []
        self.newborn_herb_list = []
        self.newborn_carn_list = []
        self.migratable_cells = []
        self.available_fodder = 0

    def place_animals(self, listof):
        """
        Places animal objects in cell. Information of animal type is provided by the input.
        Raises value error if carnivore species is not familias

        Parameters
        ----------
        listof: list of dictionaries
            each dictionary has a structure like: (example)
            {'species': 'Carnivore', 'age': 5, 'weight': 20}

        """
        for dct in listof:
            get = dct.get("species")
            if get == 'Herbivore':
                age = dct.get("age")
                weight = dct.get("weight")
                animal = Herbivore(age=age, weight=weight)
                self.herbivores_list.append(animal)

            elif get == 'Carnivore':
                age = dct.get("age")
                weight = dct.get("weight")
                animal = Carnivore(age=age, weight=weight)
                self.carnivores_list.append(animal)
            else:
                if get is not None:
                    raise ValueError('Cant place animals rather than herbivore or carnivore')

    def animals_die(self):
        """
        Handles removal of dead animals by creating a survivors-list where every surviving animal
        has been tested to see if died by .is_dying().
        Then, the list of animals are updated by being set to the list of survivors.

        """

        survivors_h = [animal for animal in self.herbivores_list if not animal.is_dying()]
        self.herbivores_list = survivors_h

        survivors_c = [animal for animal in self.carnivores_list if not animal.is_dying()]
        self.carnivores_list = survivors_c

    def remove_migrated_animals(self, migrated_herb_list, migrated_carni_list):
        """
        Removing all animal objects that has migrated out of this cell.
        Handles the removal by creating a list of animals that did not migrate (did not occur
        in the migrated_list), and then the list of animals are updated by being set to the list
        of animals that is still in cell.

        Parameters
        ----------
        migrated_herb_list: list of objects
            list of herbivore objects that has migrated to a different cell
        migrated_carni_list: list of objects
            list of Carnivore objects that has migrated to a different cell
        """

        not_migrated_h = [herb for herb in self.herbivores_list if herb not in migrated_herb_list]
        self.herbivores_list = not_migrated_h

        not_migrated_c = [carn for carn in self.carnivores_list if carn not in migrated_carni_list]
        self.carnivores_list = not_migrated_c

    def herb_eat(self):
        """
        Handles the eating for all Herbivores in cell.
        They eat based on appetite parameter F and available fodder in cell.
        Herbivores eat in random order, and can eat as long as there is fodder available.

        """
        np.random.shuffle(self.herbivores_list)
        for animal in self.herbivores_list:
            if self.available_fodder >= animal.get_param_f():
                self.available_fodder -= animal.eat()
            elif animal.get_param_f() > self.available_fodder > 0:
                animal.eat(self.available_fodder)
                self.available_fodder = 0

    def carn_eat(self):
        """
        Handles the eating for all Carnivores in cell.
        Carnivores eat Herbivores. Herbivores are eaten in the order of lowest to highest fitness.
        Carnivores eat/prey in the order of highest to lowest fitness.
        The list of surviving Herbivores in the cell is updated.

        Returns
        -------

        """
        # sort herbivores: Lowest to highest fitness
        self.herbivores_list.sort(key=lambda x: x.calculate_fitness())

        # sort carnivores: Highest to lowest fitness
        self.carnivores_list.sort(key=lambda x: x.calculate_fitness(), reverse=True)

        for carnivore in self.carnivores_list:
            eaten_herbivores = carnivore.eat(self.herbivores_list)
            herb_survivors = [herb for herb in self.herbivores_list if herb not in eaten_herbivores]

            # Improvement for later: check if herb_survivors needs to be sorted before sorting
            herb_survivors.sort(key=lambda x: x.calculate_fitness())
            self.herbivores_list = herb_survivors

    def animals_eat(self):
        """
        Annual eating of Herbivores and Carnivores
        """
        self.herb_eat()
        self.carn_eat()

    def procreation(self):
        """
        Procreation method for animals.
        Checks if there are at least one other animal of the same species in current cell,
        and if a mating partner exists (no genders), checks if both parent animals
        have proper weight.
        Then they will make a new offspring with a probability calculation based on fitness.
        Weight checks and probability calculations are handled in create_newborn method.
        After all animals try to procreate, the newborn animals are added to the fauna.

        """
        for animal in self.herbivores_list:
            offspring = animal.create_newborn(len(self.herbivores_list))
            if offspring is not None:
                self.newborn_herb_list.append(offspring)

        for animal in self.carnivores_list:
            offspring = animal.create_newborn(len(self.carnivores_list))
            if offspring is not None:
                self.newborn_carn_list.append(offspring)

        # adding newborn to fauna after all animans procreate to not add on iterating list
        self.add_newborn_to_fauna()

    def add_newborn_to_fauna(self):
        """
        Adds the newborn animals from procreation (stored in list) to fauna.
        """
        self.herbivores_list.extend(self.newborn_herb_list)
        self.newborn_herb_list = []

        self.carnivores_list.extend(self.newborn_carn_list)
        self.newborn_carn_list = []

    def animals_age_by_one_year(self):
        """
        All animals grow older by 1 year
        Returns
        -------

        """
        for animal in self.herbivores_list:
            animal.grow_older()

        for animal in self.carnivores_list:
            animal.grow_older()

    def migrate(self, adj_cells):
        """
        Handles annual migration by first checking if animal will migrate, then randomly choosing
        the cell which the animal will migrate to.

        Parameters
        ----------
        adj_cells: list of objects
            List of the four neighbouring cells which animals can migrate to from current cell

        Returns
        -------
        migration_dict:
            dictionary of the destination cell (keys) and all migrated animals to this cell (values)

        """
        migration_dct = {}

        animal_list = self.herbivores_list + self.carnivores_list

        for animal in animal_list:
            if animal.check_if_migrates():
                rand_choice = np.random.choice([0, 1, 2, 3])
                cell_to_migrate = adj_cells[rand_choice]

                if cell_to_migrate in migration_dct:
                    migration_dct[cell_to_migrate].append(animal)
                else:
                    migration_dct[cell_to_migrate] = [animal]

        return migration_dct

    def get_fodder(self):
        """
        Accessing available fodder in cell

        Returns
        -------
        available_fodder
        """
        return self.available_fodder

    def get_num_animals(self, species):
        """
        Get number of animals in cell of given species.
        Raises value error if specie is not valid
        Parameters
        ----------
        species: string
            Animal species: Herbivore or Carnivore
        """

        if species is Herbivore.__name__:
            return len(self.herbivores_list)
        elif species is Carnivore.__name__:
            return len(self.carnivores_list)
        else:
            raise ValueError('get_num_animals: must specify a valid specie to count')

    @property
    def cell_fauna_count(self):
        """
        Calculates the number of fauna by their species and returns a
        dictionary of animal species (key) and respectively counted animals (value)

        Returns
        -------
        dictionary: Animal species as key and counted instances in cell as value
        """
        herbivore = self.get_num_animals('Herbivore')
        carnivore = self.get_num_animals('Carnivore')
        return {'Herbivore': herbivore, 'Carnivore': carnivore}


class Water(Cell):
    """
    Water subclass of base class Cell
    """
    def __init__(self):
        """
        Constructor for Water subclass of Cell baseclass
        """
        super().__init__()

    def set_fodder(self):
        """
        Method to set fodder is passed in Water. No fodder exists in water.
        """
        pass

    def place_animals(self, listof):
        """
        Method for placing animals in water; not possible to place animals in water. Will raise
        Value error.

        Parameters
        ----------
        listof: List of animal object to be placed. (will not be placed)

        """
        raise ValueError('Cant place animals in Water Cell')

    def animals_eat(self):
        """
        Method for eating in Water is passed.
        """
        pass

    def migrate(self, adj_cells):
        """
        Method for migrating animals in Water Cell is passed.
        Parameters
        ----------
        adj_cells: adjacent cells (will not be used)
        """
        pass


class Desert(Cell):
    """
    Desert subclass from Cell base class.
    """
    def __init__(self):
        """
        Constructor for Water subclass of Cell baseclass
        """
        super().__init__()

    def set_fodder(self):
        """
        Method to set fodder is passed in Desert. No fodder exists in Desert.
        """
        pass


class Highland(Cell):
    """
    Highland subclass of Cell base class
    """
    def __init__(self):
        """
        Constructor class for Highland base class.
        Parameter for fodder max and available fodder is set.
        """
        super().__init__()
        self.parameters = {'f_max': 300.0}
        self.available_fodder = self.parameters['f_max']

    def set_fodder(self):
        """
        Setting available fodder to maximum value
        """
        self.available_fodder = self.parameters['f_max']

    def set_given_parameters(self, given_parameters):
        """
        Sets the user defined parameters.
        Parameters
        ----------
        given_parameters: dict
        """

        for parameter in given_parameters:
            if parameter in self.parameters:
                self.parameters[parameter] = given_parameters[parameter]
            else:
                raise RuntimeError('Unknown parameter, ' +
                                   str(parameter) +
                                   ' can\'t be set')


class Lowland(Cell):
    def __init__(self):
        """
         Constructor class for Highland base class.
         Parameter for fodder max and available fodder is set.
         """
        super().__init__()
        self.parameters = {'f_max': 800.0}
        self.available_fodder = self.parameters['f_max']

    def set_fodder(self):
        """
        Setting available fodder to maximum value
        """
        self.available_fodder = self.parameters['f_max']

    def set_given_parameters(self, given_parameters):
        """
        Sets the user defined parameters that applies to Savannah, Jungle.
        Parameters
        ----------
        given_parameters: dict
        """

        for parameter in given_parameters:
            if parameter in self.parameters:
                self.parameters[parameter] = given_parameters[parameter]
            else:
                raise RuntimeError('Unknown parameter, ' +
                                   str(parameter) +
                                   ' can\'t be set')
