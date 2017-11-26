# from utils import *

assignments = []
all_digits = '123456789'
performing_tree_search = False

rows = 'ABCDEFGHI'
cols = '123456789'

debug = False
usingDiagonals = True

def cross(a, b):
    return [s+t for s in a for t in b]

def useDiagonals(shouldUseDiagonals):
    global unitlist, units, peers, usingDiagonals

    usingDiagonals = shouldUseDiagonals

    unitlist = row_units + column_units + square_units

    if shouldUseDiagonals:
         unitlist += diagonal_units

    units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
    peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def crossDiagonal(rows):
    output = []

    leftToRightCol = 1
    leftToRight = []

    rightToLeftCol = 9
    rightToLeft = []

    for r in rows:
        leftToRight.append(r + str(leftToRightCol))
        rightToLeft.append(r + str(rightToLeftCol))

        leftToRightCol += 1
        rightToLeftCol -= 1

    output.append(leftToRight)
    output.append(rightToLeft)

    return output

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# diagonal_units = [[r+c for r,c in zip(rows,cols)], [r+c for r,c in zip(rows,cols[::-1])]]
diagonal_units = crossDiagonal(rows)

unitlist = []

units = []
peers = []

dict_row_units = dict((s, [u for u in row_units if s in u]) for s in boxes)
row_peers = dict((s, set(sum(dict_row_units[s], [])) - set([s])) for s in boxes)

dict_column_units = dict((s, [u for u in column_units if s in u]) for s in boxes)
column_peers = dict((s, set(sum(dict_column_units[s], [])) - set([s])) for s in boxes)

dict_square_units = dict((s, [u for u in square_units if s in u]) for s in boxes)
square_peers = dict((s, set(sum(dict_square_units[s], [])) - set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def display(values):
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    return

def grid_values(grid):
    if (len(grid) == 81):
        values = []
        for letter in grid:
            if letter == '.':
                values.append(all_digits)
            elif letter == 'X':
                values.append('2379')
            elif letter == 'Y':
                values.append('379')
            elif letter == 'Z':
                values.append('23')
            else:
                values.append(letter)

        assert (len(values) == 81)
        zippedOutput = zip(boxes, values)
        grid = dict(zippedOutput)

    return grid

def eliminate(values):
    for key, value in values.items():
        # If value is only 1 char long, then it's filled, so we can remove it
        # from its peers
        if len(value) == 1:
            peers_of_value = peers[key]

            for peer in peers_of_value:
                newValue = values[peer].replace(value, '')
                assign_value(values, peer, newValue)
    if debug:
        print('After elimination')
        display(values)
    return values

def only_choice(values):
    # Iterate through every possible unit (rows, cols, )
    for unit in unitlist:
        for digit in all_digits:
            boxes_containing_digit = []
            for box in unit:
                if digit in values[box]:
                    boxes_containing_digit.append(box)
            if len(boxes_containing_digit) == 1:
                assign_value(values, boxes_containing_digit[0], digit)
                # values[boxes_containing_digit[0]] = digit
    if debug:
        print('After only choice')
        display(values)
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes already have a set value
        stored_values_before = len(
            [box for box in values.keys() if len(values[box]) == 1])

        # Run through eliminate, only choice, and naked twins
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        # Check how many boxes have a determined value (to compare to original)
        stored_values_after = len(
            [box for box in values.keys() if len(values[box]) == 1])

        # If no new values added; stop
        stalled = stored_values_before == stored_values_after

        # Check if it's even possible: check for boxes with 0 available values
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    if debug:
        print('After reduction')
        display(values)
    return values

def naked_twins(values):
    # If a value is 2 chars long, look for a matching pair
    # So that pair can be removed from their unit's peers

    possible_pairs = [box for box in values.keys() if len(values[box]) == 2]

    # Go through every box containing 2 values
    for pair in possible_pairs:

        # Go through unitTypes 0, 1, 2 to check units for: rows, columns, and squares
        for unitType in range(3):
            pair_value = values[pair]

            # Check that the box's corresponding pair hasn't already been processed; since their peers are the same (efficiency)
            # if pair_value not in seen:

            # Check that only 2 boxes in the same unit share the same values
            if len([box for box in getUnitPeersOfBox(unitType, pair) if values[box] == pair_value]) == 1:

                # Get all eligible peers of the pair
                pair_unit_peers = [peer for peer in getUnitPeersOfBox(unitType, pair) if len(values[peer]) >= 2]

                # Iterate through all peers and remove the digits found in the pair
                for peer in pair_unit_peers:
                    peer_value = values[peer]
                    # print('Peer ' + peer + ' value before: ' + peer_value + ' for pair ' + pair_value)

                    # Prevent it from deleting the pair's corresponding pair
                    if peer_value != pair_value:
                        for char in pair_value:
                            peer_value = peer_value.replace(char, '')

                        # Check if the value has changed before appending
                        if peer_value != values[peer]:
                            assign_value(values, peer, peer_value)   

                    # print('Peer ' + peer + ' value after: ' + peer_value)
    if debug:
        print('After naked twins')
        display(values)
    return values

def getUnitPeersOfBox(unitType, box):
    if unitType == 0:
        # Use row unit
        return row_peers[box]

    elif unitType == 1:
        # Use column unit
        return column_peers[box]

    elif unitType == 2:
        # use square unit
        return square_peers[box]

    else:
        # Invalid input
        print("Error: unitType: " + unitType +
              " is invalid. Please use value between 0 and 2.")
        return []


def search(values):
    global performing_tree_search

    original_values = values.copy()
    # First reduce the puzzle using Elimination and Only Choice:
    values = reduce_puzzle(values)

    if values is False:

        # Don't attempt to mess with diagonals if in the middle of a tree search
        # To avoid spamming print() with error messages
        if performing_tree_search:
            return False

        # It may be returning false because the puzzle can't be solved with diagonal units
        # Attempt to solve without diagonal units
        print('Puzzle not solvable using diagonal units. Attempting to solve without diagonal units...')
        useDiagonals(False)

        values = reduce_puzzle(original_values)

        if values is False:
            print('Puzzle not solvable.')
            return False

    if all(len(values[box]) == 1 for box in values.keys()):
        # Solved!
        return values

    if debug:
        print('Attempting search')

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
    performing_tree_search = True
    for possible_value in values[chosen_box]:
        altered_values = values.copy()
        altered_values[chosen_box] = possible_value

        attempt = search(altered_values)

        if attempt:
            return attempt

    performing_tree_search = False

    return False


def solve(grid, alreadyInGridFormat=False):
    useDiagonals(True)
    
    if not alreadyInGridFormat:
        values = grid_values(grid)

    values = search(values)

    return values

def run():
    input1 = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    input2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    input3 = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    input4 = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    # Input which has a twins in it
    input5 = '1.4.9..68956.18.34..84.695151X....868.Y6...1264Z.8..97781923645495.6.823.6Z854179'

    input6 = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'

    input_grid = eval("{\"G7\": \"2345678\", \"G6\": \"1236789\", \"G5\": \"23456789\", \"G4\": \"345678\", \"G3\": \"1234569\", \"G2\": \"12345678\", \"G1\": \"23456789\", \"G9\": \"24578\", \"G8\": \"345678\", \"C9\": \"124578\", \"C8\": \"3456789\", \"C3\": \"1234569\", \"C2\": \"1234568\", \"C1\": \"2345689\", \"C7\": \"2345678\", \"C6\": \"236789\", \"C5\": \"23456789\", \"C4\": \"345678\", \"E5\": \"678\", \"E4\": \"2\", \"F1\": \"1\", \"F2\": \"24\", \"F3\": \"24\", \"F4\": \"9\", \"F5\": \"37\", \"F6\": \"37\", \"F7\": \"58\", \"F8\": \"58\", \"F9\": \"6\", \"B4\": \"345678\", \"B5\": \"23456789\", \"B6\": \"236789\", \"B7\": \"2345678\", \"B1\": \"2345689\", \"B2\": \"1234568\", \"B3\": \"1234569\", \"B8\": \"3456789\", \"B9\": \"124578\", \"I9\": \"9\", \"I8\": \"345678\", \"I1\": \"2345678\", \"I3\": \"23456\", \"I2\": \"2345678\", \"I5\": \"2345678\", \"I4\": \"345678\", \"I7\": \"1\", \"I6\": \"23678\", \"A1\": \"2345689\", \"A3\": \"7\", \"A2\": \"234568\", \"E9\": \"3\", \"A4\": \"34568\", \"A7\": \"234568\", \"A6\": \"23689\", \"A9\": \"2458\", \"A8\": \"345689\", \"E7\": \"9\", \"E6\": \"4\", \"E1\": \"567\", \"E3\": \"56\", \"E2\": \"567\", \"E8\": \"1\", \"A5\": \"1\", \"H8\": \"345678\", \"H9\": \"24578\", \"H2\": \"12345678\", \"H3\": \"1234569\", \"H1\": \"23456789\", \"H6\": \"1236789\", \"H7\": \"2345678\", \"H4\": \"345678\", \"H5\": \"23456789\", \"D8\": \"2\", \"D9\": \"47\", \"D6\": \"5\", \"D7\": \"47\", \"D4\": \"1\", \"D5\": \"36\", \"D2\": \"9\", \"D3\": \"8\", \"D1\": \"36\"}")

    input_value = input6

    solved = solve(input_value)
    if solved:
        display(solved)
    else:
        print(solved)

def runTests():
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

if __name__ == '__main__':
    # runTests()
    run()
