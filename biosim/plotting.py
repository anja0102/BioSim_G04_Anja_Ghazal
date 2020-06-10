import matplotlib.pyplot as plt
import numpy as np
from biosim.island import Island

listof = [{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(50)]
listof2 = [{'species': 'Carnivore', 'age': 5, 'weight': 50} for _ in range(20)]

listof.extend(listof2)

i = Island()
i.create_new_cell()


for cell in i.cell_list:
    cell.place_animals(listof)


def replot(n_steps):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlim(0, n_steps)
    ax.set_ylim(0, 300)

    num_herbs_every_year = []
    num_carns_every_year = []
    for _ in range(n_steps):
        i.grow_fodder()
        i.feed_animals()
        i.procreation()
        i.death()
        i.aging()
        for cell in i.cell_list:
            num_herbs_every_year.append(cell.get_num_herb_animals())
            num_carns_every_year.append(cell.get_num_carn_animals())
        # data.append(np.random.random())
        ax.plot(num_herbs_every_year, 'b-')
        ax.plot(num_carns_every_year, 'r-')
        plt.pause(1e-6)


def update(n_steps):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlim(0, n_steps)
    ax.set_ylim(0, 180)

    line1 = ax.plot(np.arange(n_steps),
                   np.full(n_steps, np.nan), 'b-')[0]
    line2 = ax.plot(np.arange(n_steps),
                   np.full(n_steps, np.nan), 'r-')[0]


    num_herbs_every_year = []
    num_carns_every_year = []
    for n in range(n_steps):
        i.grow_fodder()
        i.feed_animals()
        i.procreation()
        i.death()
        i.aging()
        for cell in i.cell_list:
            num_herbs_every_year.append(cell.get_num_herb_animals())
            num_carns_every_year.append(cell.get_num_carn_animals())

        ydata1 = line1.get_ydata()
        ydata2 = line2.get_ydata()
        ydata1[n] = num_herbs_every_year[n]
        ydata2[n] = num_carns_every_year[n]
        line1.set_ydata(ydata1)
        line2.set_ydata(ydata2)
        plt.pause(1e-6)


if __name__ == '__main__':
    #replot(100)
    update(200)
    plt.show()
