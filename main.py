from copy import deepcopy
from sudokus import sudokus

sudoku = sudokus[3]
NUMS = {1, 2, 3, 4, 5, 6, 7, 8, 9}

def sudoku_solver() -> None:
    sudoku_solving = []
    tries = 0
    cols_nums: dict = get_cols_nums()
    rows_nums: dict = get_rows_nums()
    boxes_nums: dict = get_boxes_nums()
    while tries < 3:
        for row in range(9):
            not_row_nums: dict = rows_nums[row]["notinit"]
            for col in range(9):
                if sudoku[row][col] == 0:
                    cell = f"{row}{col}"
                    row_nums: set = rows_nums[row]["init"]
                    col_nums: set = cols_nums[col]["init"]
                    box: str = get_cell_box(cell, boxes_nums)
                    box_nums: set = boxes_nums[box]
                    used_nums: set = row_nums | col_nums | box_nums
                    cell_nums: list = list(NUMS - used_nums)
                    if len(cell_nums) == 1:
                        num = cell_nums[0]
                        add_num_to_sudoku(num, row, col, box, rows_nums, cols_nums, boxes_nums)
                    else:
                        for num in cell_nums:
                            if cell not in cols_nums[col]["notinit"][num]:
                                cols_nums[col]["notinit"][num].append(cell)
                            if cell not in not_row_nums[num]:
                                not_row_nums[num].append(cell)
            
            add_inidividual_numbers(not_row_nums, rows_nums, cols_nums, boxes_nums)

        for i in range(9):
            not_cols_nums: dict = cols_nums[i]["notinit"]
            add_inidividual_numbers(not_cols_nums, rows_nums, cols_nums, boxes_nums)

        if sudoku == sudoku_solving:
            tries += 1
        else:
            tries = 0
        empty_nums_notinit(rows_nums, cols_nums)
        sudoku_solving = deepcopy(sudoku)
    
    print(rows_nums)
    print(cols_nums)
    for r in sudoku:
        print(r)

def get_rows_nums() -> dict:
    row_nums: dict = dict()
    for row in range(9):
        nums_in_row: set = set()
        for num in sudoku[row]:
            if num != 0:
                nums_in_row.add(num)
        not_in_row = NUMS - nums_in_row
        nums_not_in_row: dict = {num:[] for num in not_in_row}
        
        row_nums[row] = {"init":nums_in_row, "notinit":nums_not_in_row}
    return row_nums

def get_cols_nums() -> dict:
    col_nums = dict()
    for col in range(9):
        nums_in_col: set = set()
        for  row in range(9):
            num: int = sudoku[row][col]
            if num != 0:
                nums_in_col.add(num)
        not_in_col = NUMS - nums_in_col
        nums_not_in_col: dict = {num:[] for num in not_in_col}

        col_nums[col] = {"init":nums_in_col, "notinit":nums_not_in_col}
    return col_nums

def get_boxes_nums() -> dict:
    boxes_nums = dict()
    row: int = 0
    col: int = 0

    while row < 9:
        for _ in range(3):
            box: str = str()
            box_nums: set = set()
            for r in range(row, row+3):
                for c in range(col, col+3):
                    num: int = sudoku[r][c]
                    if num != 0:
                        box_nums.add(num)
                    box += f"{r}{c}-"
            col += 3
            boxes_nums[box] = box_nums
        row += 3  
        col = 0
    return boxes_nums

def get_cell_box(cell: str, boxes_nums: dict) -> str:
    box: str = "none"
    for key in boxes_nums.keys():
        if cell in key:
            box = key
            break
    return box

def add_num_to_sudoku(num: int, row: int, col: int, box: str, rows_nums: dict, cols_nums: dict, boxes_nums: dict) -> None:
    sudoku[row][col] = num
    rows_nums[row]["init"].add(num)
    cols_nums[col]["init"].add(num)
    boxes_nums[box].add(num)
    del rows_nums[row]["notinit"][num]
    del cols_nums[col]["notinit"][num]
    cell = f"{row}{col}"

def add_inidividual_numbers(notinit_dict: dict, rows_nums, cols_nums, boxes_nums) -> None:
    notinit_dict_copy: dict = deepcopy(notinit_dict)
    for key_num in notinit_dict_copy.keys():
        if len(notinit_dict_copy[key_num]) == 1:
            cell: str = list(notinit_dict_copy[key_num])[0]
            num: int = key_num
            row: int = int(cell[0])
            col: int = int(cell[1])
            box = get_cell_box(cell, boxes_nums)
            add_num_to_sudoku(num, row, col, box, rows_nums, cols_nums, boxes_nums)

def empty_nums_notinit(rows_nums, cols_nums) -> None:
    for i in range(9):
        for key_r in rows_nums[i]["notinit"].keys():
            rows_nums[i]["notinit"][key_r] = []
        for key_c in cols_nums[i]["notinit"].keys():
            cols_nums[i]["notinit"][key_c] = []

if __name__ == "__main__":
    sudoku_solver()