assignments = []
all_digits = '123456789'

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

def cross(A, B):
    "Cross product of elements in A and elements in B."
    pass

def grid_values(grid):
    if (len(grid) == 81):
        values = []
        for letter in grid:
            if (letter == '.'):
                values.append(all_digits)
            else:
                values.append(letter)
        assert (len(values) == 81)
        zippedOutput = zip(boxes, values)
        output = dict(zippedOutput)

        return output

def display(values):
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    for key, value in values.items():
        # If value is only 1 char long, then it's filled, so we can remove it
        # from its peers
        if (len(value) == 1):
            peers_of_value = peers[key]

            for peer in peers_of_value:
                newValue = values[peer].replace(value, '')
                assign_value(values, peer, newValue)

    return values

def only_choice(values):
    for unit in unitlist:
        for digit in all_digits:
            boxes_containing_digit = []
            for box in unit:
                if digit in values[box]:
                    boxes_containing_digit.append(box)
            if len(boxes_containing_digit) == 1:
                assign_value(values, boxes_containing_digit[0], digit)
                # values[boxes_containing_digit[0]] = digit
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

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
