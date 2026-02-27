import pygame
import sys

# --------------------------------------------------------------------------
# Configuration of constants
WIDTH = 800     # Windows width in pixels
HEIGHT = 800    # Windows height in pixels
ROWS = 8
COLS = 8
SQUARE_SIZE = WIDTH // COLS # Size of each square in pixels

# Define square colours in RGB format
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
RED = (255, 0, 0)

# Draw the chess board
def draw_board(window):
    window.fill(WHITE) # fill background with white
    for row in range(ROWS):
        for col in range(COLS):
            if (row + col) % 2 != 0:
                pygame.draw.rect(window, BROWN, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
# --------------------------------------------------------------------------
# Class to represent a chess piece, with its position and color
class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

        # Calculate the exact pixel-position of the piece on the board
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        # calculate chess-coordinates (0-7) to pixel-coordinates, goal is to center the piece in the square
        self.x = self.col * SQUARE_SIZE + SQUARE_SIZE // 2
        self.y = self.row * SQUARE_SIZE + SQUARE_SIZE // 2

    def draw(self, window):
        # Draw the piece as a circele, smaller than the square
        radius = SQUARE_SIZE // 2 - 15
        pygame.draw.circle(window, self.color, (self.x, self.y), radius)
# --------------------------------------------------------------------------
# Main function to run the game loop
def main():
    # Initialize Pygame
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Board")

    run = True

    first_piece = Piece(1, 2, RED) # Create a red piece at row 1, column 2

    # Game loop
    while run:
        # Handle events
        for events in pygame.event.get():
            if events.type == pygame.QUIT:  # If the user clicks the close button
                run = False

        # Draw the chess board
        draw_board(window)
        first_piece.draw(window)  # Draw the first piece
        pygame.display.update()

    # Quit Pygame when loop ends
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()