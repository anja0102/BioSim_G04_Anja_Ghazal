import pytest
from biosim.cell import Cell, Water, Desert, Highland, Lowland
from biosim.island import Island


class TestCell:

    @pytest.fixture(autouse=True)
    def create_animal_cell(self):
        """
        Create animals including herbivore and carnivore and a cell
        """
        self.cell = Cell()

        self.ini_herb = [{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(30)]

        self.ini_carn = [{'species': 'Carnivore', 'age': 5, 'weight': 20} for _ in range(20)]

    def test_place_herb_carn(self):
        """
        To test if we can are allowed to just place herbivores or carnivores
        """
        ini_rabbit = [{'species': 'Rabbit', 'age': 1,'weight': 0.5}]

        with pytest.raises(ValueError):
            self.cell.place_animals(ini_rabbit)

    def test_place_animals(self):
        """
        To test if the carnivores and herbivores are being placed successfully
        """
        self.cell.place_animals(self.ini_herb + self.ini_carn)
        assert self.cell.get_num_animals("Herbivore") is 30
        assert self.cell.get_num_animals("Carnivore") is 20

    def test_survivors_after_die(self):
        """
        To test if the animals die, the number of animals decrease in the cell
        """
        self.cell.place_animals(self.ini_herb + self.ini_carn)
        num_before_dying = self.cell.get_num_animals("Herbivore") +\
                           self.cell.get_num_animals("Carnivore")
        self.cell.animals_die()
        num_after_dying = self.cell.get_num_animals("Herbivore") +\
                          self.cell.get_num_animals("Carnivore")
        assert num_after_dying <= num_before_dying

    def available_fodder(self):
        """
        To test if the herbivores eat, the amount of fodder decreases in a cell
        """
        self.cell.place_animals(self.ini_herb)
        fodder_before_eat = self.cell.get_fodder()
        self.cell.herb_eat()
        fodder_after_eat = self.cell.get_fodder()
        assert fodder_after_eat < fodder_before_eat

    def test_carn_eat(self, mocker):
        """
        To test if the number of herbivores decrease after carnivores prey them
        """
        self.cell.place_animals(self.ini_herb + self.ini_carn)
        num_herb_before_prey = self.cell.get_num_animals("Herbivore")
        mocker.patch('numpy.random.random', return_value=0)  # Carnivores will definitely prey
        self.cell.carn_eat()
        num_herb_after_prey = self.cell.get_num_animals("Herbivore")
        assert num_herb_after_prey < num_herb_before_prey

    def test_procreation(self, mocker):
        """
        Firstly: To test if the number of animals is less than 2 in the cell, there should not
         be any newborn
        Secondly: If the procreation happens in the cell the number of animals should increase
        """
        one_herb = [{'species': 'Herbivore', 'age': 5, 'weight': 20}]
        self.cell.place_animals(one_herb)
        self.cell.procreation()
        assert len(self.cell.newborn_herb_list) is 0

        self.cell.place_animals(self.ini_carn + self.ini_herb)
        num_carns_before_proc = len(self.cell.carnivores_list)
        for _ in range(30):
            self.cell.carn_eat()
        mocker.patch('numpy.random.random', return_value=0)  # Animals will definitely procreate
        self.cell.procreation()
        num_carns_after_proc = len(self.cell.carnivores_list)
        assert num_carns_after_proc > num_carns_before_proc

    def test_water_cell(self):
        """
        Firstly: To test the animal can't go through the water
        Secondly: To test if the available fodder in water is 0
        """
        i = Island("WWWW\nWLHW\nWWWW")
        ini_herb = [{'loc': (0, 1),
                      'pop': [{'species': 'Herbivore',
                               'age': 5,
                               'weight': 20}]}]
        with pytest.raises(ValueError):
            i.place_animals(ini_herb)

        w = Water()
        assert w.set_fodder() is None

    def test_desert_cell(self):
        """
        To test that there is no fodder in the desert
        """
        d = Desert()
        assert d.set_fodder() is None

    def test_fodder_high_low(self):
        """
        To test if the available fodder in lowland is higher than highland
        Returns
        """
        h = Highland()
        l = Lowland()
        assert h.available_fodder < l.available_fodder






