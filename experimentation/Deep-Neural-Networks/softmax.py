import numpy as np

# Write a function that takes as input a list of numbers, and returns
# the list of values given by the softmax function.

# SOFTMAX = e^(item) / e^(item 1) + e^(item 2) ... + e^(item n)
def softmax(list):
    exp_list = [np.exp(item) for item in list]
    exp_list_sum = np.sum(exp_list)
    values_list = [exp_item / exp_list_sum for exp_item in exp_list]
    return values_list
