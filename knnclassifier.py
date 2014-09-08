# encoding=utf8
import numpy as np
import sys


def euclid(a, b):
    return np.sqrt(sum(np.power(a - b, 2)))


class Node(object):

    def __init__(self, val=None, dimension=None, left=None, right=None):
        self.val = val
        self.dimension = dimension
        self.left = left
        self.right = right

    def is_parent(self):
        return (self.left or self.right) != None

    def compare(self, x):
        return self.val[self.dimension] - x[self.dimension]

    def __repr__(self):
        return self.val.__str__()


class KdTree(object):

    def __init__(self, X, dist=euclid):
        self.root = self.build(X)
        self.dist = dist

    def build(self, X, depth=0):
        if len(X) == 0:
            return None
        depth = depth % len(X[0])
        if len(X) == 1:
            return Node(val=X[0], dimension=depth)
        indices = np.argsort(X[:, depth], axis=0)
        median_index = len(indices) / 2
        median = indices[median_index]
        left_indices = indices[:median_index]
        right_indices = indices[median_index + 1:]
        root = Node(val=X[median], dimension=depth)
        root.left = self.build(X[left_indices], depth + 1)
        root.right = self.build(X[right_indices], depth + 1)
        return root

    def find_nearest(self, x):
        return self._find_nearest(x, self.root)

    def _find_nearest(self, x, node):
        if node == None:
            return
        search_paths = []
        
        while node:
            search_paths.append(node)
            node = node.left or node.right if node.compare(
                x) > 0 else node.right or node.left
        
        child_node = closest_node = search_paths.pop()

        min_dist = self.dist(x, closest_node.val)
        while len(search_paths) > 0:
            parent_node = search_paths.pop()
            d = self.dist(x, parent_node.val)
            if d < min_dist:
                min_dist = d
                child_node = closest_node
                closest_node = parent_node

            if np.abs(parent_node.compare(x)) < min_dist:
                sibling = parent_node.right if parent_node.compare(
                    child_node.val) > 0 else parent_node.left
                if sibling != None:
                    s_dist, s_node = self._find_nearest(x, sibling)
                    if s_dist < min_dist:
                        min_dist = s_dist
                        child_node = closest_node
                        closest_node = s_node
        return min_dist, closest_node

    def draw(self, node, depth=0):
        if node is None:
            return ''
        print ' ' * 5 * depth, node.val
        if node.left != None:
            print ' ' * 5 * depth, 'left', self.draw(node.left, depth + 1)
        if node.right != None:
            print ' ' * 5 * depth, 'right', self.draw(node.right, depth + 1)
        return ''


class KNNClassifier():

    def __init__(self, k=1, dist=euclid):
        self.k = k
        self.dist = dist
        self.kd_tree = None

    def fit(self, X, Y):
        self.kd_tree = KdTree(X)

    def predict(self, x):
        self.kd_tree

if __name__ == '__main__':

    X = np.array([[2, 3], [5, 4], [9, 6], [4, 7], [8, 1], [7, 2]])
    
    dist = euclid
    target = [2, 0]

    # print get_nearest(tree, target)
    targets = [[1, 2], [2, 3], [3, 4], [5, 6], [7, 8],
              [9, 10], [1, 1], [9, 8], [8, 6], [7, 4], [6, 3], [11, 0], [4, 2], [5, 1], [3, 8], [12, 1], [15, -1]]

    X2 = np.array(
        [[0, 1, 1], [100, 100, 100], [9, 8, 11], [9, 7, 1], [5, 9, 1], [2, 3, 9], [4, 3, 19], [2, 9, 93], [92, 32, 1], [23, 98, 67], [6, 8, 26], [23, 22, 0], [2, 9, 12], [8, 4, 1], [6, 3, 9], [2, 3, 4], [4, 5, 7], [2, 9, 10], [0, 9, 20], [9, 8, 1], [9, 1, 1]])

    targets2 = [
        [1, 1, 9], [4, 9, 1], [3, 2, 3], [3, 0, 2], [0, 8, 6], [
            8, 4, 8], [20, 1, 10], [9, 11, 11], [100, 299, 28],
        [8, 9, 12], [1, 8, 1], [6, 5, 9], [2, 4, 4], [3, 2, 9], [0, 8, 6], [9, 2, 3], [9, 8, 2], [7, 9, 3], [0, 2, 1], [2, 3, 5]]
    tree = KdTree(X2)
    print tree.draw(tree.root)

    print tree.find_nearest([9, 2, 3])
