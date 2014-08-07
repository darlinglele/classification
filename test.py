from numpy import *
import unittest
import matplotlib.pylab as plt
from perceptron import *
from knnclassifier import *
from time import time

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

        # plt.show()


class KNNClassifierTest(unittest.TestCase):

    """docstring for KNNClassifierTest"""

    def test_knn(self):
        X = array([[2, 3], [5, 4], [9, 6], [4, 7], [8, 1], [7, 2]])
        Y = array([1, 1, 1, 1, 1, 1])
        classifier = KNNClassifier()
        classifier.fit(X, Y)
        kd_tree = classifier.kd_tree
        # print kd_tree

    def test_kd_tree_2_dimenssion(self):
        X = array([[2, 3], [5, 4], [9, 6], [4, 7], [8, 1], [7, 2]])
        test_points = [[3, 5],[2,9],[5,9],[3,8],[9,6],[7,3]]
        tree = KdTree(X, dist=euclid)
        for point in test_points:
            neartest = sorted([(euclid(point, x), str(x)) for x in X])[0][0] 
            if neartest !=  tree.find_nearest(point)[0]:
                print '*****error*****'


    def test_kd_tree_3_dimenssion(self):
        X = np.array(
            [[0, 1, 1], [100, 100, 100], [9, 8, 11], [9, 7, 1], [5, 9, 1], [2, 3, 9], [4, 3, 19], [2, 9, 93], [92, 32, 1], [23, 98, 67],
             [6, 8, 26], [23, 22, 0], [2, 9, 12], [0,0,0],[0,0,1],[0,0,4],[8, 4, 1], [6, 3, 9], [2, 3, 4], [4, 5, 7], [2, 9, 10], [0, 9, 20], [9, 8, 1], [9, 1, 1]])
        test_points = [[1, 1, 9], [4, 9, 1], [3, 2, 3], [3, 0, 2], [0, 8, 6], [8, 4, 8], [20, 1, 10], [9, 11, 11], [100, 299, 28], [
            8, 9, 12], [1, 8, 1], [6, 5, 9], [2, 4, 4], [3, 2, 9], [0, 8, 6], [9, 2, 3], [9, 8, 2], [7, 9, 3], [0, 2, 1], [2, 3, 5]]

        tree =KdTree(X, dist=euclid)
        for point in test_points:
            neartest = sorted([(euclid(point, x), str(x)) for x in X])[0][0] 
            if neartest !=  tree.find_nearest(point)[0]:
                print '*****error*****'
    def test_perfomance(self):
        X = np.array(
            [[0, 1, 1], [100, 100, 100], [9, 8, 11], [9, 7, 1], [5, 9, 1], [2, 3, 9], [4, 3, 19], [2, 9, 93], [92, 32, 1], [23, 98, 67],
             [6, 8, 26], [23, 22, 0], [2, 9, 12], [0,0,0],[0,0,1],[0,0,4],[8, 4, 1], [6, 3, 9], [2, 3, 4], [4, 5, 7], [2, 9, 10], [0, 9, 20], [9, 8, 1], [9, 1, 1]])
        test_points = [[1, 1, 9], [4, 9, 1], [3, 2, 3], [3, 0, 2], [0, 8, 6], [8, 4, 8], [20, 1, 10], [9, 11, 11], [100, 299, 28], [
            8, 9, 12], [1, 8, 1], [6, 5, 9], [2, 4, 4], [3, 2, 9], [0, 8, 6], [9, 2, 3], [9, 8, 2], [7, 9, 3], [0, 2, 1], [2, 3, 5]]

        tree =KdTree(X, dist=euclid)
        start = time()
        n =100        
        start = time()                
        for x in xrange(n):
            for point in test_points:                
                tree.find_nearest(point)    
        print 'KdTree search:', time() - start                

if __name__ == '__main__':
    unittest.main()
