import tkinter as tk
import numpy as np

# Create the main window
root = tk.Tk()
root.title("Tic-Tac-Toe AI")

# Global variables
board = np.full((3, 3), "")
player_turn = "X"
ai_turn = "O"
game_over = False

# Create buttons for the game board
buttons = [[None, None, None], [None, None, None], [None, None, None]]

# Check for a winner
def check_winner(b):
    # Check rows, columns, and diagonals for a winner
    for row in range(3):
        if b[row, 0] == b[row, 1] == b[row, 2] and b[row, 0] != "":
            return b[row, 0]
    for col in range(3):
        if b[0, col] == b[1, col] == b[2, col] and b[0, col] != "":
            return b[0, col]
    if b[0, 0] == b[1, 1] == b[2, 2] and b[0, 0] != "":
        return b[0, 0]
    if b[0, 2] == b[1, 1] == b[2, 0] and b[0, 2] != "":
        return b[0, 2]
    if "" not in b:
        return "Draw"
    return None

# Minimax algorithm for AI
def minimax(b, is_maximizing):
    winner = check_winner(b)
    if winner == player_turn:
        return -1
    elif winner == ai_turn:
        return 1
    elif winner == "Draw":
        return 0

    if is_maximizing:
        best_score = -np.inf
        for i in range(3):
            for j in range(3):
                if b[i, j] == "":
                    b[i, j] = ai_turn
                    score = minimax(b, False)
                    b[i, j] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = np.inf
        for i in range(3):
            for j in range(3):
                if b[i, j] == "":
                    b[i, j] = player_turn
                    score = minimax(b, True)
                    b[i, j] = ""
                    best_score = min(score, best_score)
        return best_score

# AI move
def ai_move():
    best_score = -np.inf
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i, j] == "":
                board[i, j] = ai_turn
                score = minimax(board, False)
                board[i, j] = ""
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    if best_move:
        make_move(best_move[0], best_move[1], ai_turn)

# Handle player's move
def make_move(row, col, player):
    global game_over
    if not game_over and board[row, col] == "":
        board[row, col] = player
        buttons[row][col].config(text=player)

        winner = check_winner(board)
        if winner:
            end_game(winner)
        elif player == player_turn:
            ai_move()

# End game
def end_game(winner):
    global game_over
    game_over = True
    if winner == "Draw":
        result_label.config(text="It's a Draw!")
    else:
        result_label.config(text=f"{winner} Wins!")

# Reset game
def reset_game():
    global board, player_turn, game_over
    board = np.full((3, 3), "")
    player_turn = "X"
    game_over = False
    result_label.config(text="")
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text="")

# Create buttons and labels
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text="", font="Helvetica 20", height=3, width=6,
                                  command=lambda i=i, j=j: make_move(i, j, player_turn))
        buttons[i][j].grid(row=i, column=j)

# Result label
result_label = tk.Label(root, text="", font="Helvetica 15")
result_label.grid(row=3, column=0, columnspan=3)

# Reset button
reset_button = tk.Button(root, text="Reset Game", font="Helvetica 12", command=reset_game)
reset_button.grid(row=4, column=0, columnspan=3)

# Run the GUI loop
root.mainloop()
