from math import log


class InformationGain():

    def __init__(self, features, categories):
        self.features = features
        self.categories = categories
        self.total = sum([x for x in self.categories.itervalues()])
        self.h = self.h()

    def h(self):
        cate_prob_lst = [
            float(x) / self.total for x in self.categories.itervalues()]
        return -sum([x * log(x, 2) for x in cate_prob_lst])

    def get_weight(self, f):
        return self.h - self.hf(f)

    def hf(self, f):
        f_df = sum(self.features[f].itervalues())
        _f_df = self.total - f_df
        pf = float(f_df) / self.total
        p_f = 1 - pf
        f_cf = self.features[f]
        # p(c|f)
        pfc = [float(x) / f_df for x in f_cf.itervalues()]
        _f_cf = []

        for category, count in self.categories.items():
            c = f_cf.get(category, 0)
            _f_cf.append(count - c)
        # p(Ci|_f)
        p_fc = [float(x) / _f_df for x in _f_cf]

        return -pf * sum([x * log(x, 2) for x in pfc if x != 0]) - p_f * sum([x * log(x, 2) for x in p_fc if x != 0])
