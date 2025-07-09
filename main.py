from copy import deepcopy
from sudokus import sudokus

NUMS: set = {1, 2, 3, 4, 5, 6, 7, 8, 9}

def main() -> None:
    for s in range(len(sudokus)):
        print(f"sudoku #{s}")
        sudoku = sudokus[s]
        sudoku_solved = sudoku_solver(sudoku)
        for row in sudoku_solved:
            print(row)


def sudoku_solver(sudoku) -> list[list[int]]:
    #sudoku houses
    def get_rows_givens() -> dict:
        row_nums: dict = dict()
        for row in range(9):
            nums_in_row: set = set()
            for num in sudoku[row]:
                if num != 0:
                    nums_in_row.add(num)

            not_in_row = NUMS - nums_in_row
            nums_not_in_row: dict = {num:[] for num in not_in_row}
            
            possible_values["rows"][row] = nums_not_in_row
            row_nums[row] = nums_in_row
        return row_nums

    def get_cols_givens() -> dict:
        col_nums = dict()
        for col in range(9):
            nums_in_col: set = set()
            for  row in range(9):
                num: int = sudoku[row][col]
                if num != 0:
                    nums_in_col.add(num)

            not_in_col = NUMS - nums_in_col
            nums_not_in_col: dict = {num:[] for num in not_in_col}

            possible_values["columns"][col] = nums_not_in_col
            col_nums[col] = nums_in_col
        return col_nums

    def get_boxes_givens() -> dict:
        boxes_givens = dict()
        row: int = 0
        col: int = 0

        while row < 9:
            for _ in range(3):
                box: str = str()
                nums_in_box: set = set()
                for r in range(row, row+3):
                    for c in range(col, col+3):
                        num: int = sudoku[r][c]
                        if num != 0:
                            nums_in_box.add(num)
                        box += f"{r}{c}-"
                col += 3
                not_in_box = NUMS - nums_in_box
                nums_not_in_box: dict = {num:[] for num in not_in_box}
            
                possible_values["boxes"][box] = nums_not_in_box
                boxes_givens[box] = nums_in_box
            row += 3  
            col = 0
        return boxes_givens
    

    #functions
    def get_cell_box(cell: str) -> str:
            box: str = "none"
            for key in boxes_givens.keys():
                if cell in key:
                    box = key
                    break
            return box
    
    def add_value_to_sudoku(value: int, row: int, col: int, box: str) -> None:
            sudoku[row][col] = value
            rows_givens[row].add(value)
            cols_givens[col].add(value)
            boxes_givens[box].add(value)

    def delete_value_from_possible_values(value: int, row: int, col: int, box: str) -> None:
        del possible_values["rows"][row][value]
        del possible_values["columns"][col][value]
        del possible_values["boxes"][box][value]
        cell = f"{row}{col}"
        if cell in possible_values["cells"]:
            del possible_values["cells"][f"{row}{col}"]

    def remove_value_from_sudoku(value: int, row: int, col: int, box: str) -> None:
        sudoku[row][col] = 0
        rows_givens[row].remove(value)
        cols_givens[col].remove(value)
        boxes_givens[box].remove(value)


    #solving techniques
    def solve_singles() -> None:
        #functions
        def add_single_numbers(dict_possible_values: dict) -> None:
            dict_possible_values_copy: dict = deepcopy(dict_possible_values)
            for key_num in dict_possible_values_copy.keys():
                if len(dict_possible_values_copy[key_num]) == 1:
                    cell: str = list(dict_possible_values_copy[key_num])[0]
                    num: int = key_num
                    row: int = int(cell[0])
                    col: int = int(cell[1])
                    box = get_cell_box(cell)
                    add_value_to_sudoku(num, row, col, box)
                    delete_value_from_possible_values(num, row, col, box)

        def empty_nums_notgiven() -> None:
            for key in ("rows", "columns"):
                for i in range(9):
                    for value in possible_values[key][i].keys():
                        possible_values[key][i][value] = []
            for box_key in possible_values["boxes"].keys():
                for box_value in possible_values["boxes"][box_key]:
                    possible_values["boxes"][box_key][box_value] = []


        sudoku_solving_singles: list = []
        tries: int = 0

        while tries < 3:
            for row in range(9):
                not_row_nums: dict = possible_values["rows"][row]
                for col in range(9):
                    if sudoku[row][col] == 0:
                        cell = f"{row}{col}"

                        row_nums: set = rows_givens[row]
                        col_nums: set = cols_givens[col]
                        box: str = get_cell_box(cell)
                        box_nums: set = boxes_givens[box]
                        used_nums: set = row_nums | col_nums | box_nums
                        cell_nums: list = list(NUMS - used_nums)

                        if len(cell_nums) == 1:
                            num = cell_nums[0]
                            add_value_to_sudoku(num, row, col, box)
                            delete_value_from_possible_values(num, row, col, box)
                        else:
                            possible_values["cells"][cell] = cell_nums

                            not_col_nums = possible_values["columns"][col]
                            not_box_nums = possible_values["boxes"][box]
                            for num in cell_nums:
                                if cell not in not_col_nums[num]:
                                    not_col_nums[num].append(cell)
                                if cell not in not_row_nums[num]:
                                    not_row_nums[num].append(cell)
                                if cell not in not_box_nums[num]:
                                    not_box_nums[num].append(cell)
                
                #rows indvidual numbers
                add_single_numbers(not_row_nums)

            #columns single numbers
            for i in range(9):
                not_col_nums = possible_values["columns"][i]
                add_single_numbers(not_col_nums)

            not_box_nums = possible_values["boxes"]
            for key in not_box_nums:
                add_single_numbers(not_box_nums[key])


            if sudoku == sudoku_solving_singles:
                tries += 1
            else:
                tries = 0
            empty_nums_notgiven()
            sudoku_solving_singles = deepcopy(sudoku)

    
    def backtracking_solves(index:int) -> bool:
        if index >= len(cells):
            return True
        
        cell: str = cells[index]
        cell_values: list = possible_cell_values[cell]
        
        row: int = int(cell[0])
        col: int = int(cell[1])
        box: str = get_cell_box(cell)
        for value in cell_values:
            if value not in rows_givens[row] and value not in cols_givens[col] and value not in boxes_givens[box]:
                add_value_to_sudoku(value, row, col, box)
                
                if backtracking_solves(index+1):
                    return True

                remove_value_from_sudoku(value, row, col, box)
        return False


    possible_values: dict = {"rows":{}, "columns":{}, "boxes":{}, "cells":{}}
    cols_givens: dict = get_cols_givens()
    rows_givens: dict = get_rows_givens()
    boxes_givens: dict = get_boxes_givens()

    solve_singles()

    possible_cell_values = possible_values["cells"]
    if len(possible_cell_values) > 0:
        cells = list(possible_cell_values.keys())
        backtracking_solves(0)
    return sudoku


if __name__ == "__main__":
    main()