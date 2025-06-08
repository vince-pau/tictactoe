from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Game state
board = [['' for _ in range(3)] for _ in range(3)]
current_player = 'X'
winner = None
draw = False
human_player = 'X' # Human is always X
computer_player = 'O' # Computer is always O

def check_winner():
    global winner
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != '':
            winner = row[0]
            return True
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != '':
            winner = board[0][col]
            return True
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '':
        winner = board[0][0]
        return True
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '':
        winner = board[0][2]
        return True
    return False

def check_draw():
    global draw
    if not winner and all(all(cell != '' for cell in row) for row in board):
        draw = True
        return True
    return False

def reset_game():
    global board, current_player, winner, draw
    board = [['' for _ in range(3)] for _ in range(3)]
    current_player = human_player # Human starts
    winner = None
    draw = False

def check_move_eval(temp_board, player):
    """Checks if a given player can win with this temporary board configuration."""
    # Check rows
    for r in range(3):
        if temp_board[r][0] == temp_board[r][1] == temp_board[r][2] == player:
            return True
    # Check columns
    for c in range(3):
        if temp_board[0][c] == temp_board[1][c] == temp_board[2][c] == player:
            return True
    # Check diagonals
    if temp_board[0][0] == temp_board[1][1] == temp_board[2][2] == player:
        return True
    if temp_board[0][2] == temp_board[1][1] == temp_board[2][0] == player:
        return True
    return False

def get_computer_move():
    global board, human_player, computer_player
    empty_cells = []
    for r_idx, row_val in enumerate(board):
        for c_idx, cell_val in enumerate(row_val):
            if cell_val == '':
                empty_cells.append((r_idx, c_idx))

    if not empty_cells:
        return None

    # 1. Check if computer ('O') can win
    for r, c in empty_cells:
        temp_board_state = [row[:] for row in board] # Create a deep copy
        temp_board_state[r][c] = computer_player
        if check_move_eval(temp_board_state, computer_player):
            return (r, c)

    # 2. Check if human ('X') needs to be blocked
    for r, c in empty_cells:
        temp_board_state = [row[:] for row in board]
        temp_board_state[r][c] = human_player
        if check_move_eval(temp_board_state, human_player):
            return (r, c) # Block this move

    # 3. Take Center if available
    if board[1][1] == '':
        return (1, 1)

    # 4. Take an empty corner
    corners = [(0,0), (0,2), (2,0), (2,2)]
    available_corners = []
    for r_corn, c_corn in corners:
        if board[r_corn][c_corn] == '':
            available_corners.append((r_corn, c_corn))
    if available_corners:
        return random.choice(available_corners)

    # 5. Take an empty side
    sides = [(0,1), (1,0), (1,2), (2,1)]
    available_sides = []
    for r_side, c_side in sides:
        if board[r_side][c_side] == '':
            available_sides.append((r_side, c_side))
    if available_sides:
        return random.choice(available_sides)
    
    # 6. Random (Fallback - should ideally not be reached if logic above is complete for available moves)
    if empty_cells: # Should always be true if we reached here and game not over
        return random.choice(empty_cells)
        
    return None # Should not happen if game is not over and there are moves

@app.route('/')
def index():
    reset_game() # Reset game on initial load or refresh
    return render_template('index.html', board=board, current_player=current_player)

@app.route('/move', methods=['POST'])
def move():
    global current_player, board, winner, draw
    data = request.json
    row, col = data['row'], data['col']

    # Human player's move (always 'X')
    if current_player != human_player:
        return jsonify({'status': 'error', 'message': 'Not your turn.'}), 400
    
    if winner or draw:
        return jsonify({'status': 'error', 'message': 'Game is over. Please reset.'}), 400

    if board[row][col] == '':
        board[row][col] = human_player
        
        if check_winner():
            # Human wins
            return jsonify({
                'status': 'win', 
                'message': f'Player {winner} wins!', 
                'board': board, 
                'currentPlayer': human_player, # currentPlayer was human
                'winner': winner,
                'draw': draw
            })
        
        if check_draw():
            # Draw after human's move
            return jsonify({
                'status': 'draw', 
                'message': "It's a draw!", 
                'board': board, 
                'currentPlayer': human_player, # currentPlayer was human
                'winner': winner,
                'draw': draw
            })

        # Computer's turn ('O')
        current_player = computer_player
        computer_move_coords = get_computer_move()

        if computer_move_coords:
            comp_row, comp_col = computer_move_coords
            board[comp_row][comp_col] = computer_player
            
            if check_winner():
                # Computer wins
                return jsonify({
                    'status': 'win', 
                    'message': f'Player {winner} wins!', 
                    'board': board, 
                    'currentPlayer': computer_player, # currentPlayer is computer
                    'winner': winner,
                    'draw': draw
                })

            if check_draw():
                # Draw after computer's move
                return jsonify({
                    'status': 'draw', 
                    'message': "It's a draw!", 
                    'board': board, 
                    'currentPlayer': computer_player, # currentPlayer is computer
                    'winner': winner,
                    'draw': draw
                })
        else: # No valid moves for computer means it's a draw if not already caught
            if not draw: # If check_draw() didn't already set it
                draw = True # Set global draw directly
                return jsonify({
                    'status': 'draw',
                    'message': "It's a draw! No moves left.",
                    'board': board,
                    'currentPlayer': computer_player, 
                    'winner': None,
                    'draw': True
                })

        # If game continues, it's human's turn again
        current_player = human_player
        return jsonify({
            'status': 'success', 
            'message': f'Player {current_player}\'s turn', 
            'board': board, 
            'currentPlayer': current_player,
            'winner': winner,
            'draw': draw
        })
    else:
        return jsonify({'status': 'error', 'message': 'Cell already taken.'}), 400

@app.route('/reset', methods=['POST'])
def reset():
    reset_game()
    return jsonify({
        'status': 'success', 
        'message': f'Game reset. Player {current_player}\'s turn.', 
        'board': board, 
        'currentPlayer': current_player
    })

if __name__ == '__main__':
    app.run(debug=True)