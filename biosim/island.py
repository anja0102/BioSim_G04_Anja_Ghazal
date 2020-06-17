# -*- coding: utf-8 -*-

__author__ = "Anja Stene, Student NMBU", "Ghazal Azadi, Student NMBU"
__email__ = "anja.stene@nmbu.no", "ghazal.azadi@nmbu.no"

from biosim.cell import Lowland, Highland, Water, Desert
from biosim.animal import Carnivore, Herbivore
import numpy as np


class Island:
    """
    Island class created by a map (string). Consists of Cell objects of different types.
    """

    def __init__(self, island_map):
        """
        Constructor class for the Island
        Parameters
        ----------
        island_map: string
        """
        self._map = island_map
        self._island_map = self._string_to_np_array()
        self._not_surrounded_by_ocean(self._island_map)

        self._landscape_classes = {'W': Water,
                                   'L': Lowland,
                                   'H': Highland,
                                   'D': Desert}
        self._animal_classes = {'Carnivore': Carnivore,
                                'Herbivore': Herbivore}

        self._cells = self.create_map_of_landscape_objects()
        rows = self._cells.shape[0]
        cols = self._cells.shape[1]
        self.cells_dims = rows, cols

    def get_cells(self):
        """
        Returns all cells on Island
        Returns
        -------
        _cells: all cell objects in numpy.ndarray
        """
        return self._cells

    def annual_cycle(self):
        """
        Annual Cycle of happenings on the Island
        """
        self.grow_fodder()
        self.feed_animals()
        self.procreation()
        self.death()
        self.aging()
        self.migration()

    @staticmethod
    def _edges(map_array):
        """
        Gets the border cells from the provided map array.

        Parameters
        ----------
        map_array: array

        Returns
        -------
        map_edges: list of cell objects
        """

        rows, cols = map_array.shape[0], map_array.shape[1]
        map_edges = [map_array[0, :cols], map_array[rows - 1, :cols],
                     map_array[:rows - 1, 0], map_array[:rows - 1, cols - 1]]
        return map_edges

    def _not_surrounded_by_ocean(self, map_array):
        """
        Raise an exception if a border cell in the map is not a Water Cell.

        Parameters
        ----------
        map_array: np.ndarray
        """
        edges = self._edges(map_array)
        for side in edges:
            if not np.all(side == 'W'):
                raise ValueError('The given geography string is not valid.'
                                 'The Island must be surrounded by Water')

    def _string_to_np_array(self):
        """
        Converts string map to numpy array with the same dimensions.
        Raises ValueError if dimensions not valid

        Returns
        -------
        char_map: np.ndarray
        """
        map_string_clean = self._map.replace(' ', '')

        len_ctr = len(map_string_clean.splitlines()[0])
        for i in map_string_clean.splitlines():
            if not len_ctr == len(i):
                raise ValueError('Inconsistent dimensions in map')

        char_map = np.array(
            [[j for j in i] for i in map_string_clean.splitlines()])

        return char_map

    def create_map_of_landscape_objects(self):
        """
        Builds array of same dimension for elements in geogr_array. Then,
        iterate through the given character array and build the object of
        landscapes for each character. Afterwards, save the landscape class and
        instantiate the object.

        Returns
        -------
        cells_array: np.ndarray of landscape objects
        """
        cells_array = np.empty(self._island_map.shape, dtype=object)
        for i in np.arange(self._island_map.shape[0]):
            for j in np.arange(self._island_map.shape[1]):
                cell_letter = self._island_map[i][j]
                cells_array[i][j] = self._create_cell(cell_letter)
        return cells_array

    def _create_cell(self, cell_letter):
        """
        Create cell object based on given character, each representing a cell-type.

        Parameters
        ----------
        cell_letter: str

        Returns
        -------
        object: cell object of correct landscape type
        """

        if cell_letter in self._landscape_classes:
            return self._landscape_classes[cell_letter]()
        else:
            raise ValueError(cell_letter + " is not a valid landscape type")

    def _adj_cells(self, x, y):
        """
        Returns the list of 4 adjacent cells.

        Parameters
        ----------
        x: int
            current x-coordinate
        y: int
            current y-coordinate

        Returns
        -------
        adj_cells_list: list
            List of 4 cell objects representing the adjacent cells
        """
        rows, cols = self.cells_dims
        adj_cells_list = []
        if x > 0:
            adj_cells_list.append(self._cells[x - 1, y])
        if x + 1 < rows:
            adj_cells_list.append(self._cells[x + 1, y])
        if y > 0:
            adj_cells_list.append(self._cells[x, y - 1])
        if y + 1 < cols:
            adj_cells_list.append(self._cells[x, y + 1])
        return adj_cells_list

    def get_adj_cells(self, x, y):
        """
        Gets the four adjacent cells of current location (x,y)
        Parameters
        ----------
        x: int
        y: int

        Returns
        -------
        list of adjacent cells (4 objects)
        """

        return self._adj_cells(x, y)

    def total_num_animals_per_species(self, species):
        """
        Calculates total number of animals per kind on Island.

        Parameters
        ----------
        species: str

        Returns
        -------
        num_animals: int
            total number of animals of specified specie on Island
        """
        num_animals = 0
        rows, cols = self.cells_dims
        for x in range(0, rows):
            for y in range(0, cols):
                cell = self._cells[x, y]
                num_animals += cell.get_num_animals(species)
        return num_animals

    def place_animals(self, ini_animals):
        """
        Places population of animals on Island in correct location.
        If location is not given, then ValueError is raised.
        The upper left most cell has coordinates (1,1)

        Parameters
        ----------
        ini_animals: list of dicts
        """
        for dct in ini_animals:
            if dct.get('loc') is None:
                raise ValueError('Location of animal to place was not given')

            x, y = dct.get('loc')
            # Translating so that upper rightmost corner has coordinates 1,1, and not 0,0
            x -= 1
            y -= 1
            self._cells[x, y].place_animals(dct.get('pop'))

    def grow_fodder(self):
        """
        Calls the set_fodder method in all Cells that the Island consists of.
        """

        rows, cols = self.cells_dims
        for x in range(rows):
            for y in range(cols):
                self._cells[x, y].set_fodder()

    def feed_animals(self):
        """
        Calls the animals_eat method in all Cells that the Island consists of.
        """

        rows, cols = self.cells_dims
        for x in range(rows):
            for y in range(cols):
                self._cells[x, y].animals_eat()

    def procreation(self):
        """
        Calls the procreation method in all Cells that the Island consists of.
        """

        rows, cols = self.cells_dims
        for x in range(rows):
            for y in range(cols):
                self._cells[x, y].procreation()

    def aging(self):
        """
        Calls the animals_age_by_one_year method in all Cells that the Island consists of.
        """

        rows, cols = self.cells_dims
        for x in range(rows):
            for y in range(cols):
                self._cells[x, y].animals_age_by_one_year()

    def death(self):
        """
        Calls the animals_die method in all Cells that the Island consists of.
        """

        rows, cols = self.cells_dims
        for x in range(rows):
            for y in range(cols):
                self._cells[x, y].animals_die()

    def migration(self):
        """
        Handles migration on the Island. No animal can migrate to a Water cell.
        Checks what animals will migrate, and to where.
        """

        rows, cols = self.cells_dims
        for x in range(rows):
            for y in range(cols):
                if not type(self._cells[x, y]).__name__ == "Water":
                    migration_dct = self._cells[x, y].migrate(self._adj_cells(x, y))
                    self.move_migrated_animals(migration_dct, x, y)

    def move_migrated_animals(self, migration_dct, x, y):
        """
        Moves the migrated animals by removing them from the current cell and adding to new cell.

        Parameters
        ----------
        migration_dct: dict
            of migrated animals and their new location cell
        x: int
            current x-coordinate
        y: int
            current y-coordinate
        """

        herbi_to_remove = []
        carni_to_remove = []

        for cell in migration_dct.keys():
            if not type(cell).__name__ == "Water":
                for animal in migration_dct[cell]:

                    if type(animal).__name__ == "Herbivore":
                        cell.herbivores_list.append(animal)
                        herbi_to_remove.append(animal)
                    else:
                        cell.carnivores_list.append(animal)
                        carni_to_remove.append(animal)

        self._cells[x, y].remove_migrated_animals(herbi_to_remove, carni_to_remove)
