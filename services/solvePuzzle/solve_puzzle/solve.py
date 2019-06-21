import json
from solve_puzzle import validate
from solve_puzzle import common


def solve_puzzle(puzzle):
    for loop in range(0, 5):
        # Method 2 - Row elimination
        for r in range(0, 9):
            puzzle = row_elimination(puzzle, r)

        # Method 1 - Cell Elimination
        for r in range(0, 9):
            for c in range(0, 9):
                cell_contains_value = common.cell_contains_number(puzzle, r, c)
                if not cell_contains_value:
                    result = eliminate_cell_values(puzzle, r, c)

                    if result['status']:
                        puzzle = update_cell(puzzle, r, c, result['values'][0])

        print("INFO: Loop (" + str(loop) + "), puzzle update: " + json.dumps(puzzle))

        if puzzle_complete(puzzle):
            return {'puzzle': puzzle, 'status': True}

    # Puzzle not solved
    return {'puzzle': puzzle, 'status': False}


def row_elimination(puzzle, row_num):
    row = common.get_row(puzzle, row_num)

    # Determine remaining values to solve in row.
    value_test_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    remaining_values = elimate_list_values(value_test_list, row)
    # print("DEBUG: Row (" + str(row_num) + ") has remaining values (" + str(remaining_values) + ")")

    for test_val in remaining_values:
        # print("DEBUG: Checking if all but one of the cells in row ({}) can be elimindated for value ({}).".format(row_num, test_val))

        # Tracking list, when this reaches a size of 1, for the test value, the cell is solved.
        unsolved_cell_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]

        for cell in range(0, 9):
            # Test if cell can be eliminated, as already contains value
            if row[cell] > 0:
                unsolved_cell_list.remove(cell)
                continue

            # Test if cell can be eliminated, due to a column match.
            col = common.get_column(puzzle, cell)
            if test_val in col:
                unsolved_cell_list.remove(cell)
                # print("DEBUG: Removed cell ({},{}) of Col ({}) contains val ({}).".format(row_num, cell, col, test_val))
                continue

            # Test if a cell can be eliminated, due to grid match.
            grid_num = common.get_grid_number(puzzle, row_num, cell)
            grid = common.get_grid(puzzle, grid_num)
            if test_val in grid:
                unsolved_cell_list.remove(cell)
                # print("DEBUG: Removed cell ({},{}) of Grid ({}) contains val ({}).".format(row_num, cell, grid, test_val))
                continue

        if len(unsolved_cell_list) == 1:
            print("INFO: Eliminated all cells in row {} ({}) for value ({}) to reference ({})".format(row_num, row, test_val, unsolved_cell_list))
            puzzle = update_cell(puzzle, row_num, unsolved_cell_list[0], test_val)
        # else:
        #     print("DEBUG: All cells in row {} ({}) could not be eliminated for value ({}). Remaining cell references ({})".format(
        #         row_num, row, test_val, unsolved_cell_list))

    return puzzle


def puzzle_complete(puzzle):
    if row_col_grid_complete(puzzle, "rows"):
        if row_col_grid_complete(puzzle, "cols"):
            if row_col_grid_complete(puzzle, "grids"):
                print("INFO: Puzzle complete")
                return True

    # print("DEBUG: Puzzle not complete")
    return False


def row_col_grid_complete(puzzle, type):
    test_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(0, 9):
        # TODO
        type_list = []
        if type == "rows":
            type_list = common.get_row(puzzle, i)
        elif type == "cols":
            type_list = common.get_column(puzzle, i)
        elif type == "grids":
            type_list = common.get_grid(puzzle, i)
        else:
            # if type not row, col or grid, throw exception.
            print("ERROR....")

        if not set(type_list) == set(test_list):
            # print("DEBUG: " + type + " (" + str(i) + ") with values (" + str(type_list) + ") is not complete.")
            return False

    return True


def eliminate_cell_values(puzzle, row_num, col_num):
    remaining_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    row = common.get_row(puzzle, row_num)
    remaining_values = elimate_list_values(remaining_values, row)

    col = common.get_column(puzzle, col_num)
    remaining_values = elimate_list_values(remaining_values, col)

    grid_num = common.get_grid_number(puzzle, row_num, col_num)
    grid = common.get_grid(puzzle, grid_num)
    remaining_values = elimate_list_values(remaining_values, grid)

    if len(remaining_values) == 1:
        return {'values': remaining_values, 'status': True}

    return {'values': remaining_values, 'status': False}


def update_cell(puzzle, row, col, value):
    puzzle[row][col] = value
    print("INFO: Updated row (" + str(row) + "), col (" + str(col) + ") with value (" + str(value) + ").")
    return puzzle


def elimate_list_values(possible_vals, number_list):
    for val in number_list:
        if possible_vals.count(val) > 0:
            possible_vals.remove(val)
            # print("DEBUG: Elimated value (" + str(val) + ").  List of cell possibilities now (" + str(possible_vals) + ")")

    return possible_vals
