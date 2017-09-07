rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [s+t for s in a for t in b]

def useDiagonals(use):
    # global unitlist

    if use:
        unitlist.append(diagonal_units)
    else:
        if diagonal_units in unitlist:
            unitlist.remove(diagonal_units)

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