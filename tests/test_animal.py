from biosim.island import Lowland
from biosim.animal import Herbivore
from scipy.stats import kstest


def test_animals_eat():
    """
    To test if the animal eats and the amount of fodder decreases
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


def test_calculate_fitness():
    """
    To test firstly if the weight is 0 the fitness would be also zero or not
    Secondly to see if the fitness is a number between 0 and 1
    Thirdly to see if the fitness increases by increment in weight
    Lastly if the fitness decreases by aging
    """
    herb = Herbivore(weight=0)
    assert herb.calculate_fitness() == 0
    herb = Herbivore()
    assert 0 < herb.calculate_fitness() < 1
    fitness_before_weighting = herb.calculate_fitness()
    herb.eat()  # Feeding the animal to increase the weight
    fitness_after_weighting_but_before_aging = herb.calculate_fitness()
    assert fitness_after_weighting_but_before_aging - fitness_before_weighting > 0
    herb.grow_older()
    fitness_after_aging = herb.calculate_fitness()
    assert fitness_after_aging - fitness_after_weighting_but_before_aging < 0
