from solver_and_generator import sudoku_generator, sudoku_solver
import pygame # type: ignore
from sys import exit

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Sudoku")
screen.fill("White")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Comfortaa", 35)

grid = pygame.Surface((454, 454))
grid.fill("White")
sudoku = sudoku_generator("evil")
print(sudoku)

def main() -> None:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)

        screen.blit(grid, (73,100))

        draw_grid(sudoku)
        pygame.display.update()
        clock.tick(30)

def draw_grid(sudoku) -> None:
    size: int = 50
    final_pos: int = 452
    for i in range(10):
        pos: int = (i*size) +1
        line_tickness = 1
        if i%3 == 0:
            line_tickness = 3
        pygame.draw.line(grid, "Black",(pos, 0), (pos,final_pos), line_tickness)
        pygame.draw.line(grid, "Black",(0, pos), (final_pos, pos), line_tickness) 

        pos += 16
        for j in range(9):
            if i == 9:
                break
            
            num: str = str(sudoku[j][i])
            if num != "0":
                pos_2 = j*size + 9
                number = pygame.font.Font.render(font, num, True, "Black") 
                grid.blit(number, (pos, pos_2))

if __name__ == "__main__":
    main()