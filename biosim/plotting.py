import matplotlib.pyplot as plt
import numpy as np
from biosim.island import Island

list_of_fauna = [{'species': 'Herbivore', 'age': 0, 'weight': 20} for _ in range(50)]

i = Island()
i.create_new_cell()


for cell in i.cell_list:
    cell.place_animals(list_of_fauna)


def replot(n_steps):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlim(0, n_steps)
    ax.set_ylim(0, 250)

    num_animals_every_year = []
    for _ in range(n_steps):
        i.grow_fodder()
        i.feed_animals()
        i.procreation()
        i.death()
        i.aging()
        for cell in i.cell_list:
            num_animals_every_year.append(cell.get_num_animals())
        # data.append(np.random.random())
        ax.plot(num_animals_every_year, 'b-')
        plt.pause(1e-6)


def update(n_steps):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlim(0, n_steps)
    ax.set_ylim(0, 250)

    line = ax.plot(np.arange(n_steps),
                   np.full(n_steps, np.nan), 'b-')[0]

    num_animals_every_year = []
    for n in range(n_steps):
        i.grow_fodder()
        i.feed_animals()
        i.procreation()
        i.death()
        i.aging()
        for cell in i.cell_list:
            num_animals_every_year.append(cell.get_num_animals())

        ydata = line.get_ydata()
        ydata[n] = num_animals_every_year[n]
        line.set_ydata(ydata)
        plt.pause(1e-6)


if __name__ == '__main__':
    #replot(200)
    update(200)
    plt.show()
