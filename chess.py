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
    for color in ['white', 'black']:
        IMAGES[f'pawn_{color}'] = pygame.transform.scale(pygame.image.load(f'assets/standard/pawn_{color}.png'), (SQUARE_SIZE, SQUARE_SIZE))
        IMAGES[f'rook_{color}'] = pygame.transform.scale(pygame.image.load(f'assets/standard/rook_{color}.png'), (SQUARE_SIZE, SQUARE_SIZE))
        IMAGES[f'bishop_{color}'] = pygame.transform.scale(pygame.image.load(f'assets/standard/bishop_{color}.png'), (SQUARE_SIZE, SQUARE_SIZE))
        IMAGES[f'knight_{color}'] = pygame.transform.scale(pygame.image.load(f'assets/standard/knight_{color}.png'), (SQUARE_SIZE, SQUARE_SIZE))
        IMAGES[f'queen_{color}'] = pygame.transform.scale(pygame.image.load(f'assets/standard/queen_{color}.png'), (SQUARE_SIZE, SQUARE_SIZE))
        IMAGES[f'king_{color}'] = pygame.transform.scale(pygame.image.load(f'assets/standard/king_{color}.png'), (SQUARE_SIZE, SQUARE_SIZE))

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

    def get_sliding_moves(self, board, directions):
        # This method returns a list of valid moves for sliding pieces (rooks, bishops, queens)
        
        moves = []
        for d_row, d_col in directions:
            current_row = self.row + d_row
            current_col = self.col + d_col

            while 0 <= current_row < ROWS and 0 <= current_col < COLS:
                target_piece = board.get_piece(current_row, current_col)

                if target_piece == None:
                    # field is empty, add to valid moves
                    moves.append((current_row, current_col))
                elif target_piece.color != self.color:
                    # field is occupied by opponent's piece, add to valid moves and stop in this direction
                    moves.append((current_row, current_col))
                    break
                else:
                    # field is occupied by own piece, stop in this direction
                    break

                # Go one step further in the current direction
                current_row += d_row
                current_col += d_col

        return moves

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
# Class for rook
class Rook(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color, IMAGES[f'rook_{color}'])

    def get_valid_moves(self, board):
        # Rooks can move horizontally and vertically, so we define the directions for sliding moves
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)] # Up, Down, Left, Right
        return self.get_sliding_moves(board, directions)  
# --------------------------------------------------------------------------
# Class for bishop
class Bishop(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color, IMAGES[f'bishop_{color}'])

    def get_valid_moves(self, board):
        # Bishops can move diagonally, so we define the directions for sliding moves
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)] # Diagonal directions
        return self.get_sliding_moves(board, directions)
# --------------------------------------------------------------------------
# Class for Queen
class Queen(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color, IMAGES[f'queen_{color}'])

    def get_valid_moves(self, board):
        # Queens can move both like rooks and bishops, so we combine their directions
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        return self.get_sliding_moves(board, directions)         
# --------------------------------------------------------------------------
# Class for Knight
class Knight(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color, IMAGES[f'knight_{color}'])

    def get_valid_moves(self, board):
        # Knights move in an "L" shape: two squares in one direction and one square perpendicular
        moves = []
        jump_offsets = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

        for d_row, d_col in jump_offsets:
            target_row = self.row + d_row
            target_col = self.col + d_col

            # Check if the target position is within the bounds of the board
            if 0 <= target_row < ROWS and 0 <= target_col < COLS:
                target_piece = board.get_piece(target_row, target_col)
                # If target field is empty or occupied by an opponent's piece, it's a valid move
                if target_piece == None or target_piece.color != self.color:
                    moves.append((target_row, target_col))

        return moves
# --------------------------------------------------------------------------
# Class for King
class King(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color, IMAGES[f'king_{color}'])

    def get_valid_moves(self, board):
        moves = []
        # King can move one square in any direction
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

        for d_row, d_col in directions:
            target_row = self.row + d_row
            target_col = self.col + d_col

            if 0 <= target_row < ROWS and 0 <= target_col < COLS:
                target_piece = board.get_piece(target_row, target_col)
                
                # Square is valid if it's empty or occupied by an opponent's piece
                if target_piece == None or target_piece.color != self.color:
                    moves.append((target_row, target_col))

        return moves
# --------------------------------------------------------------------------
# Class for chess board, to handle remembering pieces
class Board:
    def __init__(self):
        self.board = [] # 2D list to hold pieces
        self.create_board() # Initialize the board with pieces

    def create_board(self):
        # Defines the back rank pieces in order for both colors
        back_rank = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

        for row in range(ROWS):
            self.board.append([]) # Add a new row to the board
            for col in range(COLS):
                # Black back rank (row 0)
                if row == 0:
                    self.board[row].append(back_rank[col](row, col, "black"))
                # Black pawns (row 1)
                elif row == 1:
                    self.board[row].append(Pawn(row, col, "black"))
                # White pawns (row 6)
                elif row == 6:
                    self.board[row].append(Pawn(row, col, "white"))
                # White back rank (row 7)
                elif row == 7:
                    self.board[row].append(back_rank[col](row, col, "white"))
                # Remaining squares are empty
                else:
                    self.board[row].append(None)
    
    def draw(self, window, selected_piece=None, valid_moves=None):
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

        if valid_moves != None:
            for move in valid_moves:
                m_row, m_col = move
                # calculate the center of the square for the valid move
                center_x = m_col * SQUARE_SIZE + SQUARE_SIZE // 2
                center_y = m_row * SQUARE_SIZE + SQUARE_SIZE // 2
                # Draw a small circle at the center of the square to indicate a valid move
                pygame.draw.circle(window, RED, (center_x, center_y), 15)
    
    def get_piece(self, row, col):
        # returns the piece at the given row and column, or None if there is no piece
        return self.board[row][col]
    
    def move_piece(self, piece, row, col):
        # Move the piece in the board matrix and update its position
        self.board[piece.row][piece.col] = None # Remove piece from old location
        self.board[row][col] = piece # Place piece in new location
        piece.move(row, col) # Update the piece's internal position

        # Check for pawn promotion
        if isinstance(piece, Pawn):
            if (piece.color == "white" and piece.row == 0) or (piece.color == "black" and piece.row == 7):
                # Promote pawn to queen of same color
                self.board[row][col] = Queen(row, col, piece.color)
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
    valid_moves = [] # List to hold valid moves for the selected piece
    clock = pygame.time.Clock()
    run = True

    #first_piece = Piece(6, 2, RED) # Create a red piece at row 6, column 2

    turn = "white" # Start with white's turn
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
                    # If it is, move the piece to the new location
                    if (row, col) in valid_moves:
                        board.move_piece(selected_piece, row, col)
                        # Switch turns after a successful move
                        if turn == "white":
                            turn = "black"
                        else:
                            turn = "white"

                    selected_piece = None # Deselect the piece after moving
                    valid_moves = [] # Clear valid moves after moving

                # Case 2: No piece is selected, try to select a piece at the clicked location
                else:
                    clicked_piece = board.get_piece(row, col)
                    # Check if there is a piece at the clicked location and if it is the correct turn
                    if clicked_piece != None and clicked_piece.color == turn:
                        selected_piece = clicked_piece # Select the piece that was clicked
                        valid_moves = selected_piece.get_valid_moves(board) # Get valid moves for the selected piece

        # Draw the chess board
        board.draw(window, selected_piece, valid_moves)
        pygame.display.update()

        

    # Quit Pygame when loop ends
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()