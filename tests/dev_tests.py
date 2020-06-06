from biosim.island import Lowland
from biosim.animal import Animal
from scipy.stats import kstest


def test_animals_eat():
    """
    Test if the animal eats and the amount of fodder decreases
    """
    animal = Animal()
    c = Lowland()
    c.animal_list.append(animal)
    initial_fodder = c.get_fodder()
    c.animals_eat()
    assert initial_fodder > c.get_fodder()


def test_age():
    """
    To test if the animal grows up after a year
    """
    animal = Animal()
    assert animal.age == 0
    animal.grow_older()
    assert animal.age == 1


def test_initial_weight_gaussian_dist():
    """
    To test if the initial weight of the animals come from a gaussian distribution
    We assume the error percentage is equal to 5%
    """
    animal = Animal()
    init_weight = []
    for _ in range(20):
        init_weight.append(animal.initial_weight())
    ks_statistic, p_value = kstest(init_weight, 'norm')
    assert p_value < 0.05
