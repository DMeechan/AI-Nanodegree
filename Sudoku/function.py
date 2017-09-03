# BOARD CREATION:
rows = 'ABCDEFGHI'
cols = '123456789'


def cross(a, b):
    return [s + t for s in a for t in b]

boxes = cross(rows, cols)
# print("Boxes:", boxes)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI')
                for cs in ('123', '456', '789')]
unitlist = row_units + column_units + square_units
# print("Row units:", row_units)
# print("Column units:", column_units)
# print("Square units:", square_units)
# print("Unit list: ", unitlist)

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)
# print("Units: ", units)
# print("Peers: ", peers)


def original_grid_values(input):
    all_digits = '123456789'
    # Check for valid input
    if (len(input) == 81):
        dict = {}
        counter = 0
        # Associate each letter in input with a grid value
        for letter in input:
            if (letter == "."):
                dict.update({boxes[counter]: all_digits})
            else:
                dict.update({boxes[counter]: letter})
            counter += 1

    return dict

# SOLUTION:


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

# Desired output of only_choice():
#   4     8     3   |  9     2     1   |  6     5     7   
#   9     6     7   |  3     4     5   |  8     2     1   
#   2     5     1   |  8     7     6   |  4     9     3   
# ------------------+------------------+------------------
#   5    345    8   |  1    3456   2   |  9     7     6   
#   7     2     9   |  5   34569   4   |  1   13456   8   
#   1   13459   6   |  7    3459   8   |  2    1345   5   
# ------------------+------------------+------------------
#   3     7     2   |  6     8     9   |  5     1     4   
#   8     1     4   |  2     5     3   |  7     6     9   
#   6     9     5   |  4     1     7   |  3     8     2   


def original_only_choice(values):
    all_digits = '123456789'
    for unit_boxes in unitlist:
        remaining_digits = all_digits

        for digit in remaining_digits:
            found = False
            num_possible_boxes = 0
            last_box_digit_found_in = ''

            for box in unit_boxes:
                # Check if the digit has already been solved
                if values[box] == digit:
                    remaining_digits = remaining_digits.replace(digit, '')
                    found = True
                    break

                else:
                    # for list_of_peers_of_box in units[box]:
                        # print('List: ', list_of_peers_of_box)
                    for peers_of_box in units[box]:
                        for peer_of_box in peers_of_box:
                            if digit in values[peer_of_box]:
                                num_possible_boxes += 1
                                last_box_digit_found_in = peer_of_box
            if found == True:
                break

            if num_possible_boxes == 1:
                values[last_box_digit_found_in] = digit
    return values

def only_choice(values):
    all_digits = '123456789'

    for unit in unitlist:
        for digit in all_digits:

            # Based off this condensed code:
            # dplaces = [box for box in unit if digit in values[box]]
            # if len(dplaces) == 1:
                # values[dplaces[0]] = digit

            boxes_containing_digit = []
            for box in unit:
                if digit in values[box]:
                    boxes_containing_digit.append(box)
            if len(boxes_containing_digit) == 1:
                values[boxes_containing_digit[0]] = digit


    return values


input = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'

grid_values = grid_values(input)
# print("Grid values: ", grid_values(input))

eliminated_values = eliminate(grid_values)
# print('Eliminated values', eliminated_values)

only_choice_values = only_choice(eliminated_values)
# print('Only choice values', only_choice_values)

# USER INTERFACE:


def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    return
