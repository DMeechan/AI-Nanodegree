import math

import tensorflow as tf

def batches(batch_size, features, labels):
    """
    Create batches of features and labels
    :param batch_size: The batch size
    :param features: List of features
    :param labels: List of labels
    :return: Batches of (Features, Labels)
    """
    assert len(features) == len(labels)
    # DONE: Implement batching

    output = []
    for starting_i in range(0, len(features), batch_size):
        ending_i = starting_i + batch_size
        feature = features[starting_i:ending_i]
        label = labels[starting_i:ending_i]
        batch = [feature, label]
        output.append(batch)
    return output


# 4 Samples of features
example_features = [
    ['F11', 'F12', 'F13', 'F14'],
    ['F21', 'F22', 'F23', 'F24'],
    ['F31', 'F32', 'F33', 'F34'],
    ['F41', 'F42', 'F43', 'F44']]
# 4 Samples of labels
example_labels = [
    ['L11', 'L12'],
    ['L21', 'L22'],
    ['L31', 'L32'],
    ['L41', 'L42']]

print(batches(3, example_features, example_labels))
