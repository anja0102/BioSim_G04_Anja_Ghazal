import pytest
from biosim.animal import Herbivore, Carnivore
from biosim.island import Island


class TestIsland:

    @pytest.fixture(autouse=True)
    def create_island(self):
        """
        Creating island object
        """
        self.island = Island("""\
                        WWWWWWWW
                        WLLLLLWW
                        WHLLLLWW
                        WLDDLLWW
                        WHWWWWWW
                        WWWWWWWW""")

    def test_get_cells(self):
        """
        To test if the cells are being recognized correctly.
        In the island object we see that coordinate of (1,1) is Lowland. We'll tests this below
        """
        assert type(self.island._cells[1, 1]).__name__ is 'Lowland'

    def test_annual_cycle(self, mocker):
        """
        To test during an annual cycle, the animal either eats, procreates, ages, migrates and dies
        or not
        """
        ini_herbs = [{'loc': (2, 3),
                      'pop': [{'species': 'Herbivore',
                               'age': 5,
                               'weight': 20}
                              for _ in range(100)]}

                     ]
        ini_carns = [{'loc': (2, 4),
                      'pop': [{'species': 'Carnivore',
                               'age': 5,
                               'weight': 20}
                              for _ in range(50)]}
                     ]
        self.island.place_animals(ini_herbs + ini_carns)
        mocker.patch('numpy.random.random', return_value=0)  # To be assured that migration, death
        # and procreation happen
        num_animals_before_cycle = self.island.total_num_animals_per_species('Herbivore') + \
                                   self.island.total_num_animals_per_species('Carnivore')
        self.island.annual_cycle()
        num_animals_after_cycle = self.island.total_num_animals_per_species('Herbivore') + \
                                  self.island.total_num_animals_per_species('Carnivore')

        assert num_animals_after_cycle is not num_animals_before_cycle

    def test_adj_cell(self):
        """
        To test if the corresponding method recognizes the adjacent cell correctly
        """
        pass


