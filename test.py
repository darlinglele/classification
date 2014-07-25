from numpy import *
import unittest
import matplotlib.pylab as plt
from perceptron import *


class PerceptronTest(unittest.TestCase):

    def test_fit(self):
        X = mat(
            array([[2, 4.3], [1, 2.4], [1, 3.3], [2, 1.8], [3, 9.2], [4, 6.3], [5, 10.1], [2.3, 3.4], [3.2, 6]]))
        Y = array([1, 1, 1, -1, 1, -1, 1, -1, -1])
        icons = {1: 'ro', -1: 'bo'}
        # print X
        for x, y in zip(X, Y):
            plt.plot(x[0, 0], x[0, 1], icons[y])

        perceptron = Perceptron(alpha=0.1, n_iter=20)

        print perceptron.fit(X, Y)

        # points on the hyperplane
        p1 = [0, -perceptron.intercept / perceptron.W[1, 0]]

        p2 = [
            5, (-perceptron.intercept - 5 * perceptron.W[0, 0]) / perceptron.W[1, 0]]

        # print the hyperplane
        plt.plot([p1[0], p2[0]], [p1[1], p2[1]])

        plt.show()

if __name__ == '__main__':
    unittest.main()
