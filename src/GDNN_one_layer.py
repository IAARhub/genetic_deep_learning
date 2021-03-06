import numpy as np
from NN1 import NN1
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from nn_utils import mate, Type, sort_by_fittest
import os


class gdnn:
    def __init__(self, nlayers):
        self.nlayers = 1

    @classmethod
    def read_dataset(self, dbpath, size):
        path = os.path.dirname(os.path.abspath(__file__))
        dataset = np.loadtxt(
            path +
            dbpath,
            delimiter=",",
            skiprows=1,
            usecols=range(
                1,
                180))[
            0:size]
        neurons = dataset.shape[1] - 1
        X = dataset[:, 0:neurons]
        Y = dataset[:, neurons].reshape(X.__len__(), 1)
        Y[Y > 1] = 0
        maxn = 100  # np.matrix(X).maxn()
        # Improving gradient descent through feature scaling
        X = 2 * X / float(maxn) - 1
        return shuffle(X, Y, random_state=1)

    @classmethod
    def process(self, X, Y):
        train_x, test_x, train_y, test_y = train_test_split(
            X, Y, test_size=0.2, random_state=1)

        epochs = 600
        best_n_children = 4
        population_size = 10
        gen = {}
        generations = 10

        # Generate a poblation of neural networks each trained from a random starting weigth
        # ordered by the best performers (low error)
        init_pob = [NN1(train_x, train_y, test_x, test_y, epochs)
                    for i in range(population_size)]
        init_pob = sort_by_fittest([(nn.get_error(), nn)
                                    for nn in init_pob], Type.error)
        print("600,{}".format(init_pob[0][1].get_error()))
        gen[0] = init_pob

        result = []

        for x in range(1, generations):
            population = []
            for i in range(population_size):
                parent1 = gen[x -
                              1][np.random.randint(best_n_children)][1].get_weight()
                parent2 = gen[x -
                              1][np.random.randint(best_n_children)][1].get_weight()
                w_child = mate(parent1, parent2)
                aux = NN1(train_x, train_y, test_x, test_y, epochs, w_child)
                population += [tuple((aux.get_error(), aux))]
            gen[x] = sort_by_fittest(population, Type.error)
            net = gen[x][0][1]
            result.append(
                "{},{},{}".format(
                    (x + 1) * epochs,
                    net.get_error(),
                    net.calc_accuracy(
                        test_x,
                        test_y)))

            del population

        return(result)
