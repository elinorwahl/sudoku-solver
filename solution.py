
from utils import *
import itertools


row_units = [cross(r, cols) for r in rows]
# row_units[0] = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
# This is the top-most row.
column_units = [cross(rows, c) for c in cols]
# column_units[0] = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']
# This is the left-most column.
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# square_units[0] = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']
# This is the top-left square.
diagonal_units = [[r + c for r, c in zip(rows, cols)], [r + c for r, c in zip(rows[::-1], cols)]]
# diagonal_units[0] = ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']
# This is the top-left-to-bottom-right diagonal unit.
unitlist = row_units + column_units + square_units + diagonal_units


# units = extract_units(unitlist, boxes)
# peers = extract_peers(units, boxes)
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    # Make a list of all the boxes with one assigned value as a solution
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        # Remove the solved boxes' digits from the possible values of their peers
        digit = values[box]
        for peer in peers[box]:
            # values[peer] = values[peer].replace(digit, '')
            values = assign_value(values, peer, values[peer].replace(digit, ''))
    return values


def only_choice(values):
    """Apply the only-choice strategy to a Sudoku puzzle

    The only-choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned
    """
    for unit in unitlist:
        for digit in '123456789':
            # Make a list of all the boxes in a unit that contain a specific digit
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                # Select the digit that is the only solution for a given box
                # values[dplaces[0]] = digit
                values = assign_value(values, dplaces[0], digit)
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    The naked twins strategy says that if you have two or more unallocated boxes
    in a unit and there are only two digits that can go in those two boxes, then
    those two digits can be eliminated from the possible assignments of all other
    boxes in the same unit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers
    """
    for unit in unitlist:
        # Make a list of all boxes with two possible values as solutions
        double_values = [box for box in unit if len(values[box]) == 2]
        # Make a list of all possible pairwise combinations
        possible_twins = [list(pair) for pair in itertools.combinations(double_values, 2)]
        for pair in possible_twins:
            box_a, box_b = pair[0], pair[1]
            # Locate the naked twin pairs
            if values[box_a] == values[box_b]:
                # Remove the naked twins' possible values from other boxes in the unit
                for box in unit:
                    if box != box_a and box != box_b:
                        for digit in values[box_a]:
                            # values[box] = values[box].replace(digit, '')
                            values = assign_value(values, box, values[box].replace(digit, ''))
    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the 'eliminate' strategy
        values = eliminate(values)
        # Use the 'only choice' strategy
        values = only_choice(values)
        # Use the 'naked twins' strategy
        values = naked_twins(values)
        # Compare to check how many boxes have a determined value
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # Stop the loop if no new values were added
        stalled = solved_values_before == solved_values_after
        # Return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False
    """
    # Reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False # Unsolved
    if all(len(values[s]) == 1 for s in boxes):
        return values # Solved
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Use a ‘for’ loop to solve each one of the resulting sudokus,
    # and if one returns a value (not False), return that answer
    for value in values[s]:
        new_sudoku = values.copy()
        # new_sudoku[s] = value
        assign_value(new_sudoku, s, value)
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
