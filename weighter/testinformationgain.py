import numpy
from decimal import *
import unittest
from time import time
from informationgain import InformationGain

class TestInformationGain(unittest.TestCase):

    def setUp(self):
        self.feature_dict = {
            'a': {'cf': {'c1': 2, 'c2': 0}, 'df': 2},
            'b': {'cf': {'c1': 1, 'c2': 0}, 'df': 1},
            'c': {'cf': {'c1': 1, 'c2': 1}, 'df': 2},
            'd': {'cf': {'c1': 1, 'c2': 2}, 'df': 3}}
        self.cate_dict = {'c1': 2, 'c2': 2}
        self.weighter = InformationGain(self.feature_dict, self.cate_dict)

    def test_get_weight(self):
        self.assertEquals(self.weighter.get_weight('a'), 1.)
        self.assertEquals(
            self.weighter.get_weight('b'), float('0.31127812445913283'))
        self.assertEquals(self.weighter.get_weight('c'), 0.)
        self.assertEquals(
            self.weighter.get_weight('d'), float('0.31127812445913283'))

    def test_performance(self):
        start = time()
        for x in xrange(100000):
            self.weighter.get_weight('a')
        print 'costs: %0.2f secs' % (time() - start)


if __name__ == '__main__':
    unittest.main()
