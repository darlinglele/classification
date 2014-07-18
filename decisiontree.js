var build_tree = function(dataset, features) {
	var labels = [];

	for (var x = 0; x < dataset.length; x++) {
		labels.push(dataset[x][dataset[x].length - 1]);
	}

	var label_dict = dict(labels);

	if (Object.keys(label_dict).length == 1) {
		return {
			'label': labels[0]
		};
	}

	if (features.length == 0) {
		return {
			'label': majority_label(labels)
		}
	}

	var best_feature = select_feature(dataset, features);
	var best_feature_values = [];

	for (var x = 0; x < dataset.length; x++) {
		best_feature_values.push(dataset[x][best_feature]);
	}

	best_feature_values = set(best_feature_values);
	var tree = {
		'feature': best_feature,
		'children': {}
	};

	for (var x = 0; x < best_feature_values.length; x++) {
		var sub_features = features.slice(0);
		sub_features.splice(features.indexOf(best_feature), 1);
		var val = best_feature_values[x];
		var sub_dataset = dataset.filter(function(vector) {
			return val == vector[best_feature];
		});

		if (sub_dataset.length == 0) {
			tree['children'][val] = {
				'label': majority_label(labels)
			}
		} else {
			tree['children'][val] = build_tree(sub_dataset, sub_features);
		}
	}
	return tree;
}

var predict = function(tree, sample_vector) {
	if (tree.hasOwnProperty('label')) {
		return tree.label;
	} else {
		return predict(tree.children[sample_vector[tree.feature]], sample_vector);
	}
}

// 一些辅助的函数
var set = function(list) {
	var set = []
	
	for (var x = 0; x < list.length; x++) {
		if (set.indexOf(list[x]) == -1) {
			set.push(list[x])
		}
	}

	return set
}

var dict = function(list) {
	var dict = {};

	for (var x = 0; x < list.length; x++) {
		if (!dict.hasOwnProperty(list[x])) {
			dict[list[x]] = 1;
		} else {
			dict[list[x]] += 1;
		}
	}

	return dict;
}

var log = function(base, x) {
	return Math.log(x) / Math.log(base);
}

var entropy = function(dataset) {
	var labels = [];

	for (x in dataset) {
		labels.push(dataset[x][dataset[x].length - 1]);
	}

	var label_dict = dict(labels);
	var sum = dataset.length;
	var h = 0.0;
	
	for (x in label_dict) {
		h -= label_dict[x] / sum * log(2, label_dict[x] / sum);
	}

	return h;
}

var majority_label = function(labels) {
	var label_dict = dict(labels);
	var max = 0;
	var label = 1;

	for (x in label_dict) {
		if (label_dict[x] > max) {
			max = label_dict[x];
			label = x;
		}
	}

	return label;
}

var select_feature = function(dataset, features) {
	var max = 0;
	var label;

	for (var x = 0; x < features.length; x++) {
		var val = info_gain(dataset, features[x]);
		if (val > max) {
			max = val;
			label = features[x];
		}
	}

	return label;
}

var info_gain = function(dataset, feature) {
	var feature_values = [];

	for (x in dataset) {
		feature_values.push(dataset[x][feature]);
	}

	feature_values = set(feature_values);
	sum = dataset.length;
	var sub_entropy = 0.0;

	for (x = 0; x < feature_values.length; x++) {
		var val = feature_values[x];
		var sub_dataset = dataset.filter(function(vector) {
			return vector[feature] == val
		});
		sub_entropy += sub_dataset.length / sum * entropy(sub_dataset);
	}

	return entropy(dataset) - sub_entropy;
}

// testing code

var dataset = [
	[1, 1, 1, 1, 3],
	[1, 1, 1, 2, 2],
	[1, 1, 2, 1, 3],
	[1, 1, 2, 2, 1],
	[1, 2, 1, 1, 3],
	[1, 2, 1, 2, 2],
	[1, 2, 2, 1, 3],
	[1, 2, 2, 2, 1],
	[2, 1, 1, 1, 3],
	[2, 1, 1, 2, 2],
	[2, 1, 2, 1, 3],
	[2, 1, 2, 2, 1],
	[2, 2, 1, 1, 3],
	[2, 2, 1, 2, 2],
	[2, 2, 2, 1, 3],
	[2, 2, 2, 2, 3],
	[3, 1, 1, 1, 3],
	[3, 1, 1, 2, 3],
	[3, 1, 2, 1, 3],
	[3, 1, 2, 2, 1],
	[3, 2, 1, 1, 3],
	[3, 2, 1, 2, 2],
	[3, 2, 2, 1, 3],
	[3, 2, 2, 2, 3]
]

var features = [0, 1, 2, 3];

var tree = build_tree(dataset, features);

for (var x = 0; x < dataset.length; x++) {
	if (dataset[x][4] != predict(tree, dataset[x])) {
		console.log(dataset[x][4].toString() + predict(tree, dataset[x]));
	}
}