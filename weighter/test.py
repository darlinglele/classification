import unittest
from time import time

from informationgain import InformationGain


class TestInformationGain(unittest.TestCase):

    def setUp(self):
        self.feature_dict = {
            'a': {'c1': 2, 'c2': 0},
            'b': {'c1': 1, 'c2': 0},
            'c': {'c1': 1, 'c2': 1},
            'd': {'c1': 1, 'c2': 2}}
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
