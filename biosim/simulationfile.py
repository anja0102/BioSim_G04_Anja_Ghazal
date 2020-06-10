from biosim.island import Island
import numpy as np
np.random.seed(1)

listof = [{'species': 'Herbivore', 'age': 0, 'weight': 20} for _ in range(50)]
listof2 = [{'species': 'Carnivore', 'age': 0, 'weight': 100} for _ in range(10)]

listof.extend(listof2)

i = Island()
i.create_new_cell()

for cell in i.cell_list:
    cell.place_animals(listof)

for cell in i.cell_list:
    print(  len(cell.carnivores_list))

num_years = 50

num_herb_animals_everyyear=[]
num_carn_animals_everyyear=[]

fitness_of_one_animal = []
for year in range(num_years):
    print(year)
    i.grow_fodder()
    i.feed_animals()
    # for cell in i.cell_list:
    #     # for anim in cell.herbivores_list:
    #     fitness_of_one_animal.append(cell.herbivores_list[0].calculate_fitness())

    i.procreation()
    # for cell in i.cell_list:
    #     # for anim in cell.herbivores_list:
    #     print(cell.herbivores_list[0].calculate_fitness(), end=',')
    # print('\n')
    # for cell in i.cell_list:
    #     print('after proc', len(cell.herbivores_list))
    i.death()
    i.aging()

    for cell in i.cell_list:
        num_herb_animals_everyyear.append(cell.get_num_herb_animals())
        num_carn_animals_everyyear.append(cell.get_num_carn_animals())

print(num_herb_animals_everyyear)
print(num_carn_animals_everyyear)


# import matplotlib.pyplot as plt
# plt.plot( list( range(len(fitness_of_one_animal))), fitness_of_one_animal,'--' )
# plt.show()

