from utils import *


def grid_values(input):
    all_digits = '123456789'

    if (len(input) == 81):
        values = []
        for letter in input:
            if (letter == '.'):
                values.append(all_digits)
            else:
                values.append(letter)
        assert (len(values) == 81)
        zippedOutput = zip(boxes, values)
        output = dict(zippedOutput)

        return output


def eliminate(values):
    for key, value in values.items():
        # If value is only 1 char long, then it's filled, so we can remove it
        # from its peers
        if (len(value) == 1):
            peers_of_value = peers[key]

            for peer in peers_of_value:
                values[peer] = values[peer].replace(value, '')

    return values


def only_choice(values):
    all_digits = '123456789'

    for unit in unitlist:
        for digit in all_digits:
            boxes_containing_digit = []
            for box in unit:
                if digit in values[box]:
                    boxes_containing_digit.append(box)
            if len(boxes_containing_digit) == 1:
                values[boxes_containing_digit[0]] = digit
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes already have a set value
        stored_values_before = len(
            [box for box in values.keys() if len(values[box]) == 1])

        # Use Eliminate
        values = eliminate(values)

        # Use Only Choice
        values = only_choice(values)

        # Check how many boxes have a determined value (to compare to original)
        stored_values_after = len(
            [box for box in values.keys() if len(values[box]) == 1])

        # If no new values added; stop
        stalled = stored_values_before == stored_values_after

        # Check if it's even possible: check for boxes with 0 available values
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values


def search(values):
    # First reduce the puzzle using Elimination and Only Choice:
    values = reduce_puzzle(values)

    if values is False:
        return False

     # Solved!
    if all(len(values[box]) == 1 for box in values.keys()):
        return values

    # Find an incomplete square with the fewest options
    incomplete_boxes = [box for box in values.keys() if len(values[box]) > 1]

    chosen_box = ''
    num_of_options = 9

    for box in incomplete_boxes:
        if len(values[box]) < num_of_options:
            num_of_options = len(values[box])
            chosen_box = box
        # Stop searching if len = 2 because it can't get any lower
        if len(values[box]) == 2:
            break

    # Recursively solve each of the resulting puzzle sand it one returns a
    # value, we use it!
    for possible_value in values[chosen_box]:
        altered_values = values.copy()
        altered_values[chosen_box] = possible_value

        attempt = search(altered_values)

        if attempt:
            return attempt

    return False


input1 = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
input2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

input_dict = grid_values(input2)
# print("Grid values: ", grid_values(input))

search_values = search(input_dict)
print('Searched puzzle: ', search_values)
