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
            
            row_nums[row] = {"given":nums_in_row, "notgiven":nums_not_in_row}
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

            col_nums[col] = {"given":nums_in_col, "notgiven":nums_not_in_col}
        return col_nums

    def get_boxes_givens() -> dict:
        boxes_givens = dict()
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
                boxes_givens[box] = box_nums
            row += 3  
            col = 0
        return boxes_givens

    #solving techniques
    def solve_singles(sudoku: list[list[int]]) -> list[list[int]]:
        #functions
        def get_cell_box(cell: str) -> str:
            box: str = "none"
            for key in boxes_givens.keys():
                if cell in key:
                    box = key
                    break
            return box

        def add_value_to_sudoku(num: int, row: int, col: int, box: str) -> None:
            sudoku[row][col] = num
            rows_givens[row]["given"].add(num)
            cols_givens[col]["given"].add(num)
            boxes_givens[box].add(num)
            del rows_givens[row]["notgiven"][num]
            del cols_givens[col]["notgiven"][num]
            cell = f"{row}{col}"

        def add_single_numbers(notgiven_dict: dict) -> None:
            notgiven_dict_copy: dict = deepcopy(notgiven_dict)
            for key_num in notgiven_dict_copy.keys():
                if len(notgiven_dict_copy[key_num]) == 1:
                    cell: str = list(notgiven_dict_copy[key_num])[0]
                    num: int = key_num
                    row: int = int(cell[0])
                    col: int = int(cell[1])
                    box = get_cell_box(cell)
                    add_value_to_sudoku(num, row, col, box)

        def empty_nums_notgiven() -> None:
            for i in range(9):
                for key_r in rows_givens[i]["notgiven"].keys():
                    rows_givens[i]["notgiven"][key_r] = []
                for key_c in cols_givens[i]["notgiven"].keys():
                    cols_givens[i]["notgiven"][key_c] = []


        sudoku_solving_singles: list = []
        tries: int = 0

        while tries < 3:
            for row in range(9):
                not_row_nums: dict = rows_givens[row]["notgiven"]
                for col in range(9):
                    if sudoku[row][col] == 0:
                        cell = f"{row}{col}"

                        row_nums: set = rows_givens[row]["given"]
                        col_nums: set = cols_givens[col]["given"]
                        box: str = get_cell_box(cell)
                        box_nums: set = boxes_givens[box]
                        used_nums: set = row_nums | col_nums | box_nums
                        cell_nums: list = list(NUMS - used_nums)

                        if len(cell_nums) == 1:
                            num = cell_nums[0]
                            add_value_to_sudoku(num, row, col, box)
                        else:
                            not_col_nums = cols_givens[col]["notgiven"]
                            for num in cell_nums:
                                if cell not in not_col_nums[num]:
                                    not_col_nums[num].append(cell)
                                if cell not in not_row_nums[num]:
                                    not_row_nums[num].append(cell)
                
                #rows indvidual numbers
                add_single_numbers(not_row_nums)

            #columns single numbers
            for i in range(9):
                not_cols_givens: dict = cols_givens[i]["notgiven"]
                add_single_numbers(not_cols_givens)

            if sudoku == sudoku_solving_singles:
                tries += 1
            else:
                tries = 0
            empty_nums_notgiven()
            sudoku_solving_singles = deepcopy(sudoku)
        
        return sudoku


    cols_givens: dict = get_cols_givens()
    rows_givens: dict = get_rows_givens()
    boxes_givens: dict = get_boxes_givens()

    sudoku = solve_singles(sudoku)
    return sudoku


if __name__ == "__main__":
    main()