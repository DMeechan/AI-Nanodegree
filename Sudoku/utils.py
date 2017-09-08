rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [s+t for s in a for t in b]

def useDiagonals(use):
    global unitlist

    if use:
        # unitlist.append(diagonal_units)
        # for unit in diagonal_units:
        unitlist += diagonal_units

    else:
        # diagonal_units is an array of units, so need to check if
        # one of those units can be found in unitlist
        # if so, it needs to add the diagonal_units individually
        # adding the array at once causes a crash

        if diagonal_units[0] in unitlist:
            for unit in diagonal_units:
                unitlist.remove(unit)
        else:
            print('Error: can\'t find diagonal_units in unitlist')

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
diagonal_units = crossDiagonal(rows)

unitlist = row_units + column_units + square_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

dict_row_units = dict((s, [u for u in row_units if s in u]) for s in boxes)
row_peers = dict((s, set(sum(dict_row_units[s], [])) - set([s])) for s in boxes)

dict_column_units = dict((s, [u for u in column_units if s in u]) for s in boxes)
column_peers = dict((s, set(sum(dict_column_units[s], [])) - set([s])) for s in boxes)

dict_square_units = dict((s, [u for u in square_units if s in u]) for s in boxes)
square_peers = dict((s, set(sum(dict_square_units[s], [])) - set([s])) for s in boxes)