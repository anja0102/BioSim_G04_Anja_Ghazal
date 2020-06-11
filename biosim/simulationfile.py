from biosim.island import Island
import numpy as np
np.random.seed(1)

listof = [{'species': 'Herbivore', 'age': 0, 'weight': 20} for _ in range(10)]
listof2 = [{'species': 'Carnivore', 'age': 0, 'weight': 20} for _ in range(10)]
listof.extend(listof2)

ini_herbs = [{'loc': (1, 1),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(10)]},
             {'loc': (1, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(10)]}
             ]

ini_carns = [{'loc': (1, 1),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(4)]},
             {'loc': (1, 2),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(4)]}
             ]

geogr = """\
WWW
WLW
WWW"""

geogr2= """\
WWWW
WLHW
WWWW"""

i = Island(geogr2)
i.place_animals(ini_herbs)
i.place_animals(ini_carns)
#i.create_new_cell()

#for cell in i.cell_list:
#    cell.place_animals(listof)


num_years = 50

num_herb=[]
num_carn=[]

num_herb2=[]
num_carn2=[]

fitness_of_one_animal = []

for year in range(num_years):
    #print(year)
    i.annual_cycle()

    cells = i.get_cells()
    num_herb.append(cells[1, 1].get_num_herb_animals())
    num_carn.append(cells[1, 1].get_num_carn_animals())

    num_herb2.append(cells[1, 2].get_num_herb_animals())
    num_carn2.append(cells[1, 2].get_num_carn_animals())


#print(i._island_map)
#print(i.get_cells())
print("herb, ", num_herb)
print("carn, ", num_carn)

print("herb, ", num_herb2)
print("carn, ", num_carn2)





# import matplotlib.pyplot as plt
# plt.plot( list( range(len(fitness_of_one_animal))), fitness_of_one_animal,'--' )
# plt.show()

