from biosim.island import Lowland
from biosim.animal import Herbivore
from scipy.stats import kstest


def test_animals_eat():
    """
    Test if the animal eats and the amount of fodder decreases
    """
    herb = Herbivore()
    c = Lowland()
    c.herbivores_list.append(herb)
    initial_fodder = c.get_fodder()
    c.animals_eat()
    assert initial_fodder > c.get_fodder()


def test_age():
    """
    To test if the animal grows up after a year
    """
    herb = Herbivore()
    assert herb.age == 0
    herb.grow_older()
    assert herb.age == 1


def test_initial_weight_gaussian_dist():
    """
    To test if the initial weight of the animals come from a gaussian distribution
    We assume the error percentage is equal to 5%
    """
    herb = Herbivore()
    init_weight = []
    for _ in range(20):
        init_weight.append(herb.weight)
    ks_statistic, p_value = kstest(init_weight, 'norm')
    assert p_value < 0.05


def test_update_weight():
    """
    To test if the weight changes after eating or passing a year
    """
    herb = Herbivore()
    init_weight = herb.weight
    herb.eat()  # Lets feed animal to see if the weight increases or not
    weight_after_eating = herb.weight
    assert weight_after_eating - init_weight > 0
    herb.grow_older()  # Lets see if the animal loses its weight after growing one year older
    weight_after_aging = herb.weight
    assert weight_after_aging - weight_after_eating < 0
