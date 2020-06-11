from biosim.cell import Cell, Lowland, Highland, Water, Desert
from biosim.animal import Carnivore, Herbivore
import numpy as np


class Island:
    """
    - age
    - cells of type "celltype"
    - animals (inside celltype)
    -
    :return:
    """

    def __init__(self, island_map):
        self._map = island_map
        self._island_map = self._string_to_np_array()
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
        return self._cells

    def annual_cycle(self):
        self.grow_fodder()
        self.feed_animals()
        self.procreation()
        self.death()
        self.aging()
        self.migration()

    def _string_to_np_array(self):
        """
        Converts string to numpy array with the same diemsions.
        Returns
        -------
        char_map: np.ndarray
        """
        map_string_clean = self._map.replace(' ', '')
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
        create cell object based on given string
        Parameters
        ----------
        cell_letter: str
        Returns
        -------
        class of landscape ()
        """
        return self._landscape_classes[cell_letter]()

    def place_animals(self, ini_animals):
        for dict in ini_animals:
            print(dict)
            print(type(dict))
            x, y = dict.get('loc')
            print("X, ", x, "Y, ", y)
            self._cells[x, y].place_animals(dict.get('pop'))

    def grow_fodder(self):

        rows, cols = self.cells_dims
        for x in range(rows):
            for y in range(cols):
                self._cells[x, y].set_fodder()

    def feed_animals(self):

        rows, cols = self.cells_dims
        for x in range(rows):
            for y in range(cols):
                self._cells[x, y].animals_eat()

    def procreation(self):
        rows, cols = self.cells_dims
        for x in range(rows):
            for y in range(cols):
                self._cells[x, y].procreation()

    def aging(self):
        rows, cols = self.cells_dims
        for x in range(rows):
            for y in range(cols):
                self._cells[x, y].animals_age_by_one_year()

    def death(self):
        rows, cols = self.cells_dims
        for x in range(rows):
            for y in range(cols):
                self._cells[x, y].animals_die()

    def migration(self):
        pass

