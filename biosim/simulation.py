from biosim.animal import Carnivore, Herbivore
from biosim.cell import Highland, Lowland
from biosim.island import Island
import numpy as np
import pandas as pd
from biosim.visualisation import Visualisation
import matplotlib.pyplot as plt
import matplotlib
import os

_DEFAULT_GRAPHICS_DIR = os.path.join('../results', '')
_DEFAULT_GRAPHICS_NAME = 'biosim'
_DEFAULT_MOVIE_FORMAT = 'mp4'


class BioSim:

    def __init__(
                self,
                island_map,
                ini_pop,
                seed,
                ymax_animals=None,
                cmax_animals=None,
                hist_specs=None,
                img_base=None,
                img_fmt="png"
    ):

        self._animal_species = {'Carnivore': Carnivore, 'Herbivore': Herbivore}
        self._landscapes_with_changeable_parameters = {'H': Highland, 'L': Lowland}
        self._island_map = island_map
        self._island = Island(island_map)
        self._vis = None
        self._fig = None
        self.add_population(ini_pop)
        self._final_year = None
        self._year = 0
        np.random.seed(seed)
        self.maximum = 0

        if ymax_animals is None:  #the y-axis limit should be adjusted automatically.
            # matplotlib.pyplot.autoscale(enable=True, axis='both', tight=None)
            self.ymax_animals = 20000  # or call a function to get max num animals updated?
        else:
            self.ymax_animals = ymax_animals

        if cmax_animals is None: #If cmax_animals is None, sensible, fixed default values should be used.
            self._cmax_animals = {'Herbivore': 5, 'Carnivore': 5}
        else:
            self._cmax_animals = cmax_animals

        if img_base is None:
            self._img_base = _DEFAULT_GRAPHICS_DIR + _DEFAULT_GRAPHICS_NAME
        else:
            self._img_base = img_base
        self._img_ctr = 0
        self._img_fmt = img_fmt


    """
    :param island_map: Multi-line string specifying island geography
    :param ini_pop: List of dictionaries specifying initial population
    :param seed: Integer used as random number seed
    :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
    :param cmax_animals: Dict specifying color-code limits for animal densities
    :param hist_specs: Specifications for histograms, see below
    :param img_base: String with beginning of file name for figures, including path
    :param img_fmt: String with file type for figures, e.g. 'png'
    If ymax_animals is None, the y-axis limit should be adjusted automatically.
    If cmax_animals is None, sensible, fixed default values should be used.
    cmax_animals is a dict mapping species names to numbers, e.g.,
    {'Herbivore': 50, 'Carnivore': 20}
    hist_specs is a dictionary with one entry per property for which a histogram shall be shown.
    For each property, a dictionary providing the maximum value and the bin width must be
    given, e.g.,
    {'weight': {'max': 80, 'delta': 2}, 'fitness': {'max': 1.0, 'delta': 0.05}}
    Permitted properties are 'weight', 'age', 'fitness'.
    If img_base is None, no figures are written to file.
    Filenames are formed as
    '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)
    where img_no are consecutive image numbers starting from 0.
    img_base should contain a path and beginning of a file name.
    """

    def set_animal_parameters(self, species, params):


        """
        Sets given parameters for corresponding animal species class.
        Parameters
        ----------
        species: str
            Name of animal species
        params: dict
            With valid parameter specification for species
        """

        if species in self._animal_species:
            species_class = self._animal_species[species]
            animal = species_class()
            animal.set_given_parameters(params)
        else:
            raise TypeError(species + ' parameters can\'t be assigned, '
                                      'there is no such data type')

    def set_landscape_parameters(self, landscape, params):


        """
        Set parameters for landscape type.
        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """

        if landscape in self._landscapes_with_changeable_parameters:
            landscape = self._landscapes_with_changeable_parameters[landscape]
            land = landscape()
            land.set_given_parameters(params)
        else:
            raise TypeError(landscape + 'parameters can not be assigned')

    def simulate(self, num_years, vis_years=1, img_years=None):


        """
        Run simulation while visualizing the result.
        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)
        Image files will be numbered consecutively.
        """
        if img_years is None:
            img_years = vis_years

        self._final_year = self._year + num_years
        self._setup_graphics()

        while self._year < self._final_year:

            if self._year % vis_years == 0:
                self._update_graphics()

            if self._year % img_years == 0:
                self._save_graphics()

            self._island.annual_cycle()
            self._year += 1

            print("Year " + str(self._year))
            print(self.num_animals_per_species)

    def _save_to_csv(self):
        pass
    #     df = self._animal_distribution
    #     df.to_csv('../results/data.csv', sep='\t', encoding='utf-8')


    def y_max(self):
        """
        Maximum number of animals
        """
        new_value = self.num_animals
        if new_value > self.maximum:
            self.maximum = new_value
        return self.maximum

    def _setup_graphics(self):
        """
        Creates subplots.
        """
        map_dims = self._island.cells_dims

        if self._fig is None:
            self._fig = plt.figure()
            self._vis = Visualisation(self._island_map, self._fig, map_dims)

        self._vis.visualise_map()
        self._vis.animal_graphs(self._final_year, self.ymax_animals)

        self._vis.animal_dist_graphs()
        self._fig.tight_layout()

    def _update_graphics(self):
        """
        Updates graphics with current data.
        """
        df = self._animal_distribution
        rows, cols = self._island.cells_dims
        dist_matrix_carnivore = np.array(df[['Carnivore']]).reshape(rows, cols)
        dist_matrix_herbivore = np.array(df[['Herbivore']]).reshape(rows, cols)
        self._update_animals_graph()
        self._vis.update_herbivore_dist(dist_matrix_herbivore)
        self._vis.update_carnivore_dist(dist_matrix_carnivore)
        plt.pause(1e-6)
        self._fig.suptitle('Year: ' + str(self.year), x=0.5)

    def _update_animals_graph(self):
        herb_count, carn_count = list(self.num_animals_per_species.values())
        self._vis.update_graphs(self._year, herb_count, carn_count)

    def _save_graphics(self):
        """
        Saves graphics to file if file name is given.
        """
        pass
        # if self._img_base is None:
        #     return
        #
        # plt.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
        #                                              num=self._img_ctr,
        #                                              type=self._img_fmt))
        # self._img_ctr += 1


    def add_population(self, population):


        """
        Add a population to the island
        :param population: List of dictionaries specifying population
        """
        self._island.place_animals(population)

    @property
    def year(self):
        """
        Simulates last year.
        """
        return self._year

    @property
    def num_animals(self):
        """
        Calculates total number of animals on island.
        Returns
        -------
        total_num: int
        """
        total_num = 0
        for species in self._animal_species:
            total_num += self._island.total_num_animals_per_species(species)
        return total_num


    @property
    def num_animals_per_species(self):
        """
        Calculates number of animals per species in island, as dictionary.
        Returns
        -------
        num_per_species: dict
        """
        num_per_species = {}
        for species in self._animal_species:
            print(species)
            num_per_species[species] = self._island.total_num_animals_per_species(species)
        return num_per_species


    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
        pass




    @property
    def _animal_distribution(self):
        """
        Calculates Pandas DataFrame with animal count per species for each cell
        on island.
        Returns
        -------
        pd.DataFrame(count_df): data frame
        """
        count_df = []
        rows, cols = self._island.cells_dims
        for i in range(rows):
            for j in range(cols):
                cell = self._island.get_cells()[i, j]
                animals_count = cell.cell_fauna_count
                count_df.append({'Row': i, 'Col': j,
                                 'Herbivore': animals_count['Herbivore'],
                                 'Carnivore': animals_count['Carnivore']})
        return pd.DataFrame(count_df)