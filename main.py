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

sudoku_boxes = [
    ["00", "01", "02", "10", "11", "12", "20", "21", "22"],
    ["03", "04", "05", "13", "14", "15", "23", "24", "25"],
    ["06", "07", "08", "16", "17", "18", "26", "27", "28"],
    ["30", "31", "32", "40", "41", "42", "50", "51", "52"],
    ["33", "34", "35", "43", "44", "45", "53", "54", "55"],
    ["36", "37", "38", "46", "47", "48", "56", "57", "58"],
    ["60", "61", "62", "70", "71", "72", "80", "81", "82"],
    ["63", "64", "65", "73", "74", "75", "83", "84", "85"],
    ["66", "67", "68", "76", "77", "78", "86", "87", "88"]
]

def sudoku_solver() -> None:
    cols_nums: dict = get_cols_nums()
    rows_nums: dict = get_rows_nums()
    boxes_nums: dict = get_boxes_nums()

    possible_nums = dict()
    for row in range(9):
        for col in range(9):
            if sudoku[row][col] == 0:
                ubication = f"{row}{col}"
                row_nums: set = rows_nums[row]
                col_nums: set = cols_nums[col]
                box: str = "none"
                for key in boxes_nums.keys():
                    if ubication in key:
                        box = key
                        break
                box_nums: set = boxes_nums[box]
                used_nums: set = row_nums | col_nums | box_nums
                cell_nums: list = list(NUMS - used_nums)
                if len(cell_nums) == 1:
                    sudoku[row][col] = cell_nums[0]
                else:
                    possible_nums[ubication] = cell_nums

                
    print(possible_nums)
    print(sudoku)

def get_rows_nums() -> dict:
    row_nums = dict()
    for row in range(9):
        nums: set = set()
        for num in sudoku[row]:
            if num != 0:
                nums |= {num}
        row_nums[row] = nums
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

if __name__ == "__main__":
    sudoku_solver()