from math import log
from decimal import *


class InformationGain():

    def __init__(self, feature_dict, cate_dict):
        self.feature_dict = feature_dict
        self.cate_dict = cate_dict
        self.doc_total = sum([x for x in self.cate_dict.itervalues()])
        self.h = self.h()

    def h(self):
        cate_prob_lst = [
            float(x) / self.doc_total for x in self.cate_dict.itervalues()]
        return -sum([x * log(x, 2) for x in cate_prob_lst])

    def get_weight(self, f):
        return self.h - self.hf(f)

    def hf(self, f):
        f_df = self.feature_dict[f]['df']
        _f_df = self.doc_total - f_df
        pf = float(f_df) / self.doc_total
        p_f = 1 - pf
        f_cf = self.feature_dict[f]['cf']
        # p(c|f)
        pfc = [float(x) / f_df for x in f_cf.itervalues()]
        _f_cf = []
        for c, f in self.cate_dict.items():
            f_fc = f_cf.get(c, 0)
            _f_cf.append(f - f_fc)
        # p(Ci|_f)
        p_fc = [float(x) / _f_df for x in _f_cf]
        return -pf * sum([x * log(x, 2) for x in pfc if x != 0]) - p_f * sum([x * log(x, 2) for x in p_fc if x != 0])
