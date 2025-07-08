from copy import deepcopy

sudoku = [
    [0,6,0,0,9,0,0,8,7],
    [8,3,0,2,6,0,5,0,0],
    [9,2,0,8,0,7,0,4,3],
    [0,0,0,0,0,0,0,0,6],
    [6,8,0,7,5,0,0,0,2],
    [5,0,0,0,0,3,0,0,0],
    [2,5,0,4,0,0,7,6,9],
    [3,1,9,0,0,0,8,2,4],
    [0,4,0,0,8,2,0,0,0]
]

NUMS = {1, 2, 3, 4, 5, 6, 7, 8, 9}

def sudoku_solver() -> None:
    sudoku_solving = []
    cols_nums: dict = get_cols_nums()
    rows_nums: dict = get_rows_nums()
    boxes_nums: dict = get_boxes_nums()
    possible_nums = dict()
    while sudoku != sudoku_solving:
        for row in range(9):
            not_row_nums: dict = rows_nums[row]["notinit"]
            for col in range(9):
                if sudoku[row][col] == 0:
                    ubication = f"{row}{col}"
                    row_nums: set = rows_nums[row]["init"]
                    col_nums: set = cols_nums[col]
                    box: str = get_cell_box(ubication, boxes_nums)
                    box_nums: set = boxes_nums[box]
                    used_nums: set = row_nums | col_nums | box_nums
                    cell_nums: list = list(NUMS - used_nums)
                    if len(cell_nums) == 1:
                        num = cell_nums[0]
                        add_num_to_sudoku(num, row, col, box, rows_nums, cols_nums, boxes_nums)
                    else:
                        possible_nums[ubication] = cell_nums
                        for num in cell_nums:
                            not_row_nums[num].append(ubication)

            not_row_nums_copy: dict = deepcopy(not_row_nums)
            for key_num in not_row_nums_copy.keys():
                if len(not_row_nums_copy[key_num]) == 1:
                    cell: str = not_row_nums_copy[key_num][0]
                    num: int = key_num
                    row: int = int(cell[0])
                    col: int = int(cell[1])
                    box = get_cell_box(cell, boxes_nums)
                    add_num_to_sudoku(num, row, col, box, rows_nums, cols_nums, boxes_nums)
                    
        sudoku_solving = sudoku[:]
        
    print(rows_nums)
    print(possible_nums)
    for r in sudoku:
        print(r)

def get_rows_nums() -> dict:
    row_nums: dict = dict()
    for row in range(9):
        nums_in_row: set = set()
        for num in sudoku[row]:
            if num != 0:
                nums_in_row |= {num}

        not_in_row = NUMS - nums_in_row
        nums_not_in_row: dict = {num:[] for num in not_in_row}
        
        row_nums[row] = {"init":nums_in_row, "notinit":nums_not_in_row}
    return row_nums

def get_cols_nums() -> dict:
    col_nums = dict()
    for col in range(9):
        nums: set = set()
        for  row in range(9):
            num: int = sudoku[row][col]
            if num != 0:
                nums |= {num}
        col_nums[col] = nums
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
                        box_nums |= {num}
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
    rows_nums[row]["init"] |= {num}
    cols_nums[col] |= {num}
    boxes_nums[box] |= {num}
    del rows_nums[row]["notinit"][num]

if __name__ == "__main__":
    sudoku_solver()