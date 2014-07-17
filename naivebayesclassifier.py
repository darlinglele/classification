# encoding=utf-8
import numpy
import pickle
import jieba
import os
from decimal import *
from time import time
from collections import Counter
import re
from math import log
from weighter.informationgain import InformationGain


class NaiveBayesClassifier():

    def __init__(self, cutter=None, stop_words=None):
        self.cutter = cutter
        self.stop_words = stop_words
        self.feature_dict = {}
        self.selected_feature_dict = {}
        self.cate_dict = {}
        self.cache = {'feature_prob': {}, 'feature_lst': {}}

    def train(self, data, encoding='utf-8'):
        for root, dirs, files in os.walk(data, True):
            for name in files:
                print root, name, '.....'
                cate_id = root.split('/')[-1]
                doc_text = open(os.path.join(root,name)).read().decode(encoding)
                features = self._split(doc_text)
                for key, count in features:
                    self.feature_dict.setdefault(key, {})
                    self.feature_dict[key].setdefault('tf', 0)
                    self.feature_dict[key]['tf'] += count
                    self.feature_dict[key].setdefault('df', 0)
                    self.feature_dict[key]['df'] += 1
                    self.feature_dict[key].setdefault('cf', {})
                    self.feature_dict[key]['cf'].setdefault(cate_id, 0)
                    self.feature_dict[key]['cf'][cate_id] += 1
                self.cate_dict.setdefault(cate_id, 0)
                self.cate_dict[cate_id] += 1

    def reduce(self, max_size=10000, weighter=InformationGain):
        print 'reducing the feature dimessions, weighted by', type(weighter).__name__
        start = time()
        weighter = weighter(self.feature_dict, self.cate_dict)
        for f in self.feature_dict:
            self.feature_dict[f]['weight'] = weighter.get_weight(f)
        reduced_features = sorted(
            [x for x in self.feature_dict.items()], key=lambda x: x[1]['weight'], reverse=True)[0:max_size]
        self.reduced_feature_dict = {x[0]: x[1] for x in reduced_features}
        print 'reducing completed, costs %0.2f secs' % (time() - start)

    def dump(self, file):
        print 'dumping the raw features to file ', file
        start = time()
        data = {'feature_dict': self.feature_dict, 'cate_dict': self.cate_dict}
        output = open(file, 'wb')
        pickle.dump(data, output)
        output.close()
        print 'dumping completed costs %0.2f secs' % (time() - start)

    def load(self, file):
        print 'loading raw features from', file, '...'
        start = time()
        input = open(file, 'rb')
        data = pickle.load(input)
        input.close()
        self.feature_dict = data['feature_dict']
        self.cate_dict = data['cate_dict']
        print 'loading raw features completed, costs %0.2f secs' % (time() - start)

    def _split(self, doc_text):
        self.stop_words = self.stop_words or set(
            unicode(x.strip(), 'utf-8') for x in open('stopwords.dic', 'r'))
        try:
            seg_list = self.cutter.cut(doc_text, cut_all=False)
            zh_vocabulaly = re.compile(ur"([\u4E00-\u9FA5]+$)")
            feature_lst = [x.strip()
                           for x in seg_list if zh_vocabulaly.match(x) and x not in self.stop_words]
        except Exception, e:
            return []
        else:
            counter = Counter(feature_lst)
            return [(x, counter[x]) for x in counter]

    def predict(self, doc_path, encoding='utf-8'):
        return sorted([(x, self._prob(x, encoding,doc_path=doc_path)) for x in self.cate_dict], key=lambda x: x[1], reverse=True)[0][0]

    def predict_text(self, doc_text, encoding='utf-8'):
        return sorted([(x, self._prob(x,encoding,doc_text=doc_text)) for x in self.cate_dict], key=lambda x: x[1], reverse=True)[0][0]

    def test(self, test_data):
        start = time()
        total = 0.0
        errors = 0.0
        for root, dirs, files in os.walk(test_data, topdown=True):
            for name in files:
                cate_id = root.split('/')[-1]
                print cate_id, name
                label = self.predict(os.path.join(root, name))
                total += 1
                if cate_id != label:
                    errors += 1
                    print 'predict: %s, actual: %s, errors percentage: %0.2f' % (label, cate_id, 100 * errors / total)
        print 'testing completed, total: %d, errors: %d, error rate:%0.2f, costs: %0.2f' % (total, errors, 100 * errors / total, time() - start)
        return errors / total

    def _prob(self, cate_id, encoding, doc_path=None, doc_text=None):
        if (doc_path or doc_text) == None:
            raise Exception('doc_path and doc_text should not both None')
        doc_path = doc_path or hash(doc_text)
        if doc_path in self.cache['feature_lst']:
            feature_lst = self.cache['feature_lst'][doc_path]
        else:
            doc_text = doc_text or open(doc_path).read().decode(encoding)
            feature_lst = [x[0] for x in self._split(doc_text)]
            self.cache['feature_lst'] = {doc_path: feature_lst}

        return self._doc_prob(feature_lst, cate_id) * self._cate_prob(cate_id)

    def _cate_prob(self, cate_id):
        return Decimal(self.cate_dict.get(cate_id, 0)) / sum(self.cate_dict.itervalues())

    def _doc_prob(self, feature_lst, cate_id):
        doc_prob = Decimal(1.0)
        for feature in feature_lst:
            if feature in self.reduced_feature_dict:
                doc_prob *= Decimal(self._feature_prob(feature, cate_id))
        return doc_prob

    def _feature_prob(self, feature, cate_id, weight=1, alpha=0.5):
        if feature + cate_id in self.cache['feature_prob']:
            return self.cache['feature_prob'][feature + cate_id]
        basic_feature_prob = 0.0
        cf_dict = self.reduced_feature_dict[feature]['cf']
        cf_sum = sum(cf_dict.itervalues())
        if cate_id in cf_dict:
            basic_feature_prob = float(
                cf_dict[cate_id]) / self.cate_dict[cate_id]
        feature_prob = (
            weight * alpha + cf_sum * basic_feature_prob) / (weight + cf_sum)
        self.cache['feature_prob'][feature + cate_id] = feature_prob
        return feature_prob

if __name__ == '__main__':
    classifier = NaiveBayesClassifier(cutter=jieba)
    # classifier.train('data_train/')
    # classifier.dump('raw_features.dat')
    classifier.load('raw_features.dat')
    classifier.reduce(max_size=450, weighter=InformationGain)
    for x in classifier.reduced_feature_dict.keys():
        print x.encode('utf-8')
