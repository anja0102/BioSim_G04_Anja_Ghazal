import matplotlib.pyplot as plt
import numpy as np
from biosim.island import Island

ini_herbs = [{'loc': (1, 3),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(150)]}


             ]

ini_carns = [{'loc': (1, 3),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(40)]}
             ]


geogr = """\
WWWWW
WLHHW
WWWWW"""

geogr2 = """\
WWWWWWWW
WWLLLLWW
WWLLLLWW
WWDDLLWW
WWLLDLWW
WWWWWWWW"""

geogr3 = """\
WWWWWWWWW
WDDDDDDDW
WDDDDDDDW
WDDDDDDDW
WDDDDDDDW
WDDDDDDDW
WDDDDDDDW
WDDDDDDDW
WWWWWWWWW"""

i = Island(geogr3)

i.place_animals(ini_herbs)
i.place_animals(ini_carns)


num_years = 50



# def replot(n_steps):
#     fig = plt.figure()
#     ax = fig.add_subplot(1, 1, 1)
#     ax.set_xlim(0, n_steps)
#     ax.set_ylim(0, 300)
#
#     num_herbs_every_year = []
#     num_carns_every_year = []
#     for _ in range(n_steps):
#         i.grow_fodder()
#         i.feed_animals()
#         i.procreation()
#         i.death()
#         i.aging()
#         for cell in i.get_cells():
#             num_herbs_every_year.append(cell.get_num_herb_animals())
#             num_carns_every_year.append(cell.get_num_carn_animals())
#         # data.append(np.random.random())
#         ax.plot(num_herbs_every_year, 'b-')
#         ax.plot(num_carns_every_year, 'r-')
#         plt.pause(1e-6)


def update(n_steps):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlim(0, n_steps)
    ax.set_ylim(0, 3000)

    line1 = ax.plot(np.arange(n_steps),
                   np.full(n_steps, np.nan), 'b-')[0]
    line2 = ax.plot(np.arange(n_steps),
                   np.full(n_steps, np.nan), 'r-')[0]


    num_herbs_cell = []
    num_carns_cell = []
    sum_herbs_one_year=[]
    sum_carn_one_year=[]
    for n in range(n_steps):
        i.annual_cycle()

        for rows in range(i.cells_dims[0]):
            for clmns in range(i.cells_dims[1]):
        #         if (rows!= 0) and ( clmns!=0):
                    # print( rows, " :", clmns, ": ", i.get_cells()[rows, clmns].get_num_herb_animals())
                    # print( rows, " :", clmns, ": ", i.get_cells()[rows, clmns].get_num_carn_animals())


                sum_herbs_one_year.append(i.get_cells()[rows, clmns].get_num_herb_animals())
                sum_carn_one_year.append(i.get_cells()[rows, clmns].get_num_carn_animals())
        #print('Year: ', n)

        num_herbs_cell.append(sum(sum_herbs_one_year))
        num_carns_cell.append(sum(sum_carn_one_year))

        sum_herbs_one_year = []
        sum_carn_one_year = []





        ydata1 = line1.get_ydata()
        ydata2 = line2.get_ydata()
        ydata1[n] = num_herbs_cell[n]
        ydata2[n] = num_carns_cell[n]
        line1.set_ydata(ydata1)
        line2.set_ydata(ydata2)
        plt.pause(1e-6)


if __name__ == '__main__':
    #replot(100)
    update(200)
    #plt.show()
