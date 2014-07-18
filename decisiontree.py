from math import log

def select_feature(dataset, features):
    info_gains = [(info_gain(dataset, x), x) for x in features]
    return max(info_gains)[1]


def info_gain(dataset, feature):
    feature_values = set([x[feature] for x in dataset])
    entropy_sub_dataset = 0.0
    for val in feature_values:
        sub_dataset = [x for x in dataset if x[feature] == val]
        entropy_sub_dataset += float(len(sub_dataset)) / len(
            dataset) * entropy(sub_dataset)
    return entropy(dataset) - entropy_sub_dataset


def entropy(dataset):
    labels = [x[-1] for x in dataset]
    label_dict = {x: 0.0 for x in set(labels)}
    for label in labels:
        label_dict[label] += 1
    h = 0.0
    for k, v in label_dict.iteritems():
        h -= v / len(labels) * log(v / len(labels), 2)
    return h


def majority_label(labels):
    label_dict = {x: 0 for x in set(labels)}
    for label in labels:
        label_dict[label] += 1
    return max(label_dict.items(), key=lambda x: x[1])[0]


def build_tree(dataset, features):
    labels = [x[-1] for x in dataset]
    if labels.count(labels[0]) == len(labels):
        return {'label': labels[0]}
    if len(features) == 0:
        return {'label': majority_label(labels)}
    best_feature = select_feature(dataset, features)
    tree = {'feature': best_feature, 'children': {}}
    best_feature_values = set([x[best_feature] for x in dataset])
    for val in best_feature_values:
        sub_dataset = filter(lambda x: x[best_feature] == val, dataset)
        if len(sub_dataset) == 0:
            tree['children'][val] = {
                'label': majority_label(labels)}
        else:
            tree['children'][val] = build_tree(
                sub_dataset, [x for x in features if x != best_feature])
    return tree


def predict(tree, sample_vector):
    if 'feature' in tree:
        return predict(tree['children'][sample_vector[tree['feature']]], sample_vector)
    else:
        return tree['label']


if __name__ == '__main__':

    dataset = [map(int, x.strip().split('  ')) for x in open('lenses.data')]
    features = [x for x in xrange(len(dataset[0]) - 1)]


    print info_gain(dataset,0)
    print entropy(dataset)
    # tree = build_tree(dataset, features)

    # for x in dataset:
    #     print x[-1], predict(tree, x)
