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
WHITE = (250, 230, 180)
GREEN = (20, 70, 40)
RED = (255, 0, 0)
BLUE = (0, 128, 255)

# Load chess pieces PNGs
IMAGES = {}

def load_images():
    IMAGES['pawn_white'] = pygame.image.load('assets/standard/pawn_white.png')
    IMAGES['pawn_white'] = pygame.transform.scale(IMAGES['pawn_white'], (SQUARE_SIZE, SQUARE_SIZE))

    IMAGES['pawn_black'] = pygame.image.load('assets/standard/pawn_black.png')
    IMAGES['pawn_black'] = pygame.transform.scale(IMAGES['pawn_black'], (SQUARE_SIZE, SQUARE_SIZE))

    
# --------------------------------------------------------------------------
# Class to represent a chess piece, with its position and color
class Piece:
    def __init__(self, row, col, color, image):
        self.row = row
        self.col = col
        self.color = color
        self.image = image

        # Calculate the exact pixel-position of the piece on the board
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        # calculate chess-coordinates (0-7) to pixel-coordinates, goal is to center the piece in the square
        self.x = self.col * SQUARE_SIZE + SQUARE_SIZE // 2
        self.y = self.row * SQUARE_SIZE + SQUARE_SIZE // 2

    def draw(self, window):
        # To draw the piece, we need to calculate the top-left corner of the image, since blit uses that as reference
        top_left_x = self.x - self.image.get_width() // 2
        top_left_y = self.y - self.image.get_height() // 2
        
        window.blit(self.image, (top_left_x, top_left_y))

    def move(self, row, col):
        # Update location of the piece and recalculate pixel position
        self.row = row
        self.col = col
        self.calc_pos()
# --------------------------------------------------------------------------
# Class for pawn
class Pawn(Piece):
    def __init__(self, row, col, color):
        # Decide image we need from dictionary based on color
        if color == "white":
            img = IMAGES['pawn_white']
        else:
            img = IMAGES['pawn_black']

        # Call parent class with super
        super().__init__(row, col, color, img)

    # Move method
    def get_valid_moves(self, board):
        # This method will return a list of valid moves for the pawn, based on its current position and the board state
        moves = []
        direction = -1 if self.color == "white" else 1 # White pawns move up (negative direction), black pawns move down (positive direction)

        # Saftey check to ensure we don't go out of bounds when checking moves
        next_row = self.row + direction
        if 0 <= next_row < ROWS:

            # Check one square forward
            if board.get_piece(self.row + direction, self.col) == None:
                moves.append((self.row + direction, self.col))
    
                # Check two squares forward from starting position
                if (self.row == 6 and self.color == "white") or (self.row == 1 and self.color == "black"):
                    if board.get_piece(self.row + 2 * direction, self.col) == None:
                        moves.append((self.row + 2 * direction, self.col))
    
            # Check captures diagonally
            for col_offset in [-1, 1]:
                new_col = self.col + col_offset
                if 0 <= new_col < COLS: # Ensure we don't go out of bounds
                    target_piece = board.get_piece(self.row + direction, new_col)
                    if target_piece != None and target_piece.color != self.color:
                        moves.append((self.row + direction, new_col))

        return moves
# --------------------------------------------------------------------------
# Class for chess board, to handle remembering pieces
class Board:
    def __init__(self):
        self.board = [] # 2D list to hold pieces
        self.create_board() # Initialize the board with pieces

    def create_board(self):
        for row in range(ROWS):
            self.board.append([]) #Add a new row to the board
            for col in range(COLS):
                # row 1 black pawns
                if row == 1:
                    self.board[row].append(Pawn(row, col, "black"))
                # row 6 white pawns
                elif row == 6:
                    self.board[row].append(Pawn(row, col, "white"))
                # other rows are empty
                else:
                    self.board[row].append(None)
    
    def draw(self, window, selected_piece=None):
        window.fill(WHITE)

        # Draw the chess board squares
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 != 0:
                    pygame.draw.rect(window, GREEN, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        
        # Draw a blue border around the selected piece (if any)
        if selected_piece != None:
            s_row, s_col = selected_piece.row, selected_piece.col
            pygame.draw.rect(window, BLUE, (s_col * SQUARE_SIZE, s_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

        # Draw pieces from the matrix
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != None:
                    piece.draw(window)
    
    def get_piece(self, row, col):
        # returns the piece at the given row and column, or None if there is no piece
        return self.board[row][col]
    
    def move_piece(self, piece, row, col):
        # Move the piece in the board matrix and update its position
        self.board[piece.row][piece.col] = None # Remove piece from old location
        self.board[row][col] = piece # Place piece in new location
        piece.move(row, col) # Update the piece's internal position
# --------------------------------------------------------------------------
# Function to convert mouse position (in pixels) to board coordinates (row, col)
def get_row_col_from_mouse(pos):
    x, y = pos

    # we need // divisions to get the integer row and column indices
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE

    return row, col
# --------------------------------------------------------------------------
# Main function to run the game loop
def main():
    # Initialize Pygame
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Board")

    load_images() # Load piece images before starting the game loop

    selected_piece = None
    clock = pygame.time.Clock()
    run = True

    #first_piece = Piece(6, 2, RED) # Create a red piece at row 6, column 2
    board = Board() # Create the chess board with pieces

    # Game loop
    while run:
        clock.tick(60) # Limit the frame rate to 60 FPS

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the user clicks the close button
                run = False

            # Handle mouse clicks to move the piece
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()  # Get the mouse position in pixels
                row, col = get_row_col_from_mouse(pos)  # Convert to board coordinates
                
                # Case 1: A piece is already selected
                if selected_piece != None:
                    # Check if the clicked square is a valid move for the selected piece
                    valid_moves = selected_piece.get_valid_moves(board)
                    # If it is, move the piece to the new location
                    if (row, col) in valid_moves:
                        board.move_piece(selected_piece, row, col)
                    selected_piece = None # Deselect the piece after moving

                # Case 2: No piece is selected, try to select a piece at the clicked location
                else:
                    clicked_piece = board.get_piece(row, col)
                    if clicked_piece != None:
                        selected_piece = clicked_piece # Select the piece that was clicked

        # Draw the chess board
        board.draw(window, selected_piece)
        pygame.display.update()

        

    # Quit Pygame when loop ends
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()