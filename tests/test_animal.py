import pytest
from biosim.animal import Herbivore, Carnivore
from scipy.stats import kstest
from scipy import stats
import numpy as np

SEED = 12345678  # random seed for tests
ALPHA = 0.01  # significance level for statistical tests


class TestAnimal:

    @pytest.fixture(autouse=True)
    def create_animal(self):
        """
        Create animal object
        """
        self.animal = [Herbivore(), Carnivore()]
        self.herb_list = [self.animal[0]]
        self.init_weight = []

    def test_age(self):
        """
        To test if the animal grows up after a year
        """
        for species in range(2):
            before_aging = self.animal[species].age
            self.animal[species].grow_older()
            after_aging = self.animal[species].age
            assert after_aging - before_aging == 1

    def test_initial_weight_gaussian_dist(self):
        """
        To test if the initial weight of the animals come from a gaussian distribution
        We assume the error percentage is equal to 5%
        """
        for species in range(2):
            for _ in range(2000):
                self.init_weight.append(self.animal[species].weight)
                ks_statistic, p_value = kstest(self.init_weight, 'norm')
                assert p_value < ALPHA

    def test_when_carnivore_prey(self):
        """
        To test the condition for carnivores to prey on herbivores:
        - If the carnivore fitness is greater than herbivore fitness
        """
        for _ in range(20):
            self.animal[0].eat()  # Increasing fitness of the herbivore by feeding it
            self.animal[1].grow_older()  # Decreasing fitness of the carnivore by aging it
        assert self.animal[1].check_carn_prey(self.animal[0].calculate_fitness(),
                                              self.animal[1].calculate_fitness()) is False

    def animal_update_weight(self):
        """
        Firstly: To test if the weight of the animal increases by eating
        Secondly: To test if the weight of the animal decreases by aging
        """
        for species in range(2):
            self.init_weight = (self.animal[species].get_weight())
            self.animal[0].eat()
            self.animal[1].eat(self.herb_list)
            weight_after_eating = (self.animal[species].get_weight())
            if self.animal[1].check_carn_prey(self.animal[0].calculate_fitness(),
                                              self.animal[1].calculate_fitness()):
                assert weight_after_eating - self.init_weight > 0
            self.animal[species].grow_older()
            weight_after_aging = self.animal[species].get_weight()
        assert weight_after_aging - weight_after_eating < 0

    def test_calculate_fitness(self):
        """
        Firstly: To test if the weight is 0 the fitness would be also zero
        Secondly: To see if the fitness is a number between 0 and 1
        Thirdly: To see if the fitness increases by increment in weight
        Lastly: If the fitness decreases by aging
        """
        animal_zero_weight = [Herbivore(weight=0), Carnivore(weight=0)]
        for species in range(2):
            assert animal_zero_weight[species].calculate_fitness() == 0
        for species in range(2):
            assert 0 < self.animal[species].calculate_fitness() < 1
            fitness_before_weighting = self.animal[species].calculate_fitness()
            self.animal[1].eat(self.herb_list)  # Feeding the carnivore
            self.animal[0].eat()  # Feeding the herbivore
            fitness_after_weighting_but_before_aging = self.animal[species].calculate_fitness()
            if self.animal[1].check_carn_prey(self.animal[0].calculate_fitness(),
                                              self.animal[1].calculate_fitness()):
                assert fitness_after_weighting_but_before_aging - fitness_before_weighting > 0
            self.animal[species].grow_older()  # aging the animals
            fitness_after_aging = self.animal[species].calculate_fitness()
            assert fitness_after_aging - fitness_after_weighting_but_before_aging < 0

    def test_create_new_born_conditions(self):
        """
        To test if the mother can give birth to child conditioned to:
        - Existence of more than two animal in cell
        - Amount of its weight
        """
        for species in range(2):
            assert self.animal[species].check_mating_weight_conditions(num_animals=1) is False
            if self.animal[species].weight < self.animal[0].params['zeta'] * \
                    (self.animal[0].params['w_birth'] + self.animal[0].params['sigma_birth']):
                assert self.animal[species].check_mating_weight_conditions(num_animals=2) is False
            else:
                assert self.animal[species].check_mating_weight_conditions(num_animals=2) is True


    def test_mother_weight_decrement(self):
        """
        To test if the mother loses weight after giving birth to the child
        If not its weight should not change
        """
        for species in range(2):
            for _ in range(10):  # Feeding the animal sufficiently to be able to give birth
                self.animal[1].eat(self.herb_list)
                self.animal[0].eat()
                before_birth_weight = self.animal[species].weight
            create_new_born = self.animal[species].create_newborn(2)
            after_birth_weight = self.animal[species].weight
            if create_new_born is None:
                assert after_birth_weight - before_birth_weight == 0
            else:
                assert after_birth_weight - before_birth_weight < 0


    def test_death(self):
        """
        Firstly: To test if the animal dies when its weight is less / equal to zero
        Secondly: Since there's a reverse relationship between death and fitness, animals with higher
        fitness should have lower probability to die. Existence of this relationship is being tested
        here
        """
        animal_zero_weight = [Herbivore(weight=0), Carnivore(weight=0)]
        die_low_weight = []
        die_high_weight = []
        sum_die_low_weight = []
        sum_die_high_weight = []
        self.animal[1].eat(self.herb_list)  # Feeding the carnivore for one time
        self.animal[0].eat()  # Feeding the herbivore for one time
        for species in range(2):
            assert animal_zero_weight[species].is_dying() is True

            for _ in range(500):
                for _ in range(100):
                    die_low_weight.append(self.animal[species].is_dying())
                sum_die_low_weight.append(sum(die_low_weight))

            for _ in range(50):  # Feeding animals for 50 times leading to fitness increment
                self.animal[1].eat(self.herb_list)
                self.animal[0].eat()

            for _ in range(500):
                for _ in range(100):
                    die_high_weight.append(self.animal[species].is_dying())
                sum_die_high_weight.append(sum(die_high_weight))

        contingency_table = np.array([sum_die_high_weight, sum_die_low_weight])
        chi2_stat, p_val, dof, ex = stats.chi2_contingency(contingency_table)
        assert p_val < ALPHA

    def test_migration_annually(self, mocker):
        """
        To test if the animal migrates once a year
        """
        for species in range(2):
            mocker.patch('numpy.random.random', return_value=0)
            assert self.animal[species].has_migrated_this_year is False
            self.animal[species].grow_older()
            assert self.animal[species].has_migrated_this_year is False
