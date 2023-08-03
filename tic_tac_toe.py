import random, math, time

def count_spaces(board):
    free_spaces = 0
    for i in board:
        if i == " ":
            free_spaces += 1
    return free_spaces

def count_possible_moves(board, free_spaces):
    possible_moves = []
    while free_spaces != len(possible_moves):
        index = random.randint(1,9)
        if index - 1 not in possible_moves:
            if board[index - 1] == " ":
                possible_moves.append(index - 1)
    return possible_moves

def check_winner_variants(board, player):
    if (
    (board[0] == player and board[1] == player and board[2] == player) or (board[3] == player and board[4] == player and board[5] == player) or (board[6] == player and board[7] == player and board[8] == player) or
    (board[0] == player and board[3] == player and board[6] == player) or (board[1] == player and board[4] == player and board[7] == player) or (board[2] == player and board[5] == player and board[8] == player) or
    (board[0] == player and board[4] == player and board[8] == player) or (board[2] == player and board[4] == player and board[6] == player)):
        return True

def check_winner(board, free_spaces):
    if check_winner_variants(board, "X") == True:
        winner = "X"
    elif check_winner_variants(board, "O") == True:
        winner = "O"
    elif free_spaces <= 0:
        winner = "tie"
    else:
        winner = ""
    return winner

def random_machine_player(board, player, free_spaces):
    """Easy AI player"""
    while True:
        index = random.randint(1,9)
        if board[index - 1] == " ":
            board[index - 1] = player
            return board

def smart_machine_player(board, player, free_spaces):
    """Unbeatable AI player"""
    possible_moves = count_possible_moves(board, free_spaces)
    if len(possible_moves) == 9:
        board[possible_moves[0]] = player
    else:
        best = minimax(board, player)['position']
        board[best] = player
    return board

def minimax(board, player):
    max_player = 'X'
    other_player = 'O' if player == 'X' else 'X'
    if check_winner_variants(board, other_player) == True:
        return {'position': None, 'score': 1 * (count_spaces(board) + 1) if other_player == max_player else -1 * (count_spaces(board) + 1)}
    elif count_spaces(board) <= 0:
        return {'position': None, 'score': 0}
    if player == max_player:
        best = {'position': None, 'score': -math.inf}
    else:
        best = {'position': None, 'score': math.inf}
    possible_moves = count_possible_moves(board, count_spaces(board))
    for possible_move in possible_moves:
        board[possible_move] = player
        simulat_score = minimax(board, other_player)
        board[possible_move] = ' '
        simulat_score['position'] = possible_move
        if player == max_player:
            if simulat_score['score'] > best['score']:
                best = simulat_score
        else:
            if simulat_score['score'] < best['score']:
                best = simulat_score
    return best

def human_player(board, player, free_spaces):
    """Player input on the command line"""
    time.sleep(0.5)
    print_board(board)
    while True:
        try:
            index = int(input(f"{player} turn. Write from 1 to 9: "))
            if board[index - 1] == " ":
                board[index - 1] = player
                return board
            else:
                print("This space taken")
        except IndexError:
            print("Incorrect space")
        except ValueError:
            print("Incorrect value")

def print_board(board):
    """Print board on the command line"""
    print("")
    print("| " + " | ".join(board[0:3]) + " |")
    print("| " + " | ".join(board[3:6]) + " |")
    print("| " + " | ".join(board[6:]) + " |")
    print("")

def play_once(x_player, o_player, print_result=True):
    """Play Tic-Tac-Toe once on the command line
    Players: human_player, smart_machine_player, random_machine_player"""
    board = [" " for _ in range(9)]
    free_spaces = count_spaces(board)
    winner = ""
    while free_spaces > 0 and winner == "":
        # X player
        board = x_player(board, "X", free_spaces)
        free_spaces = count_spaces(board)
        winner = check_winner(board, free_spaces)
        if winner == "":
            # O player
            board = o_player(board, "O", free_spaces)
            free_spaces = count_spaces(board)
        winner = check_winner(board, free_spaces)
    if print_result:
        print_board(board)
        if winner == "tie":
            print("It's a tie\n")
        else:
            print(f"Winner - {winner} player\n")
    return winner

def play_more_games(number_of_games, x_player, o_player):
    """Play Tic-Tac-Toe many (number_of_games) times (on command line)
    Players: human_player, smart_machine_player, random_machine_player"""
    win_x = 0
    win_o = 0
    tie = 0
    start = time.time()
    for i in range(number_of_games):
        winner = play_once(x_player, o_player, print_result=False)
        if winner == "tie":
            tie += 1
        elif winner == "X":
            win_x += 1
        elif winner == "O":
            win_o += 1
    end = time.time()
    print(f"\nIn {number_of_games} games in {int(end - start)} seconds: X player win - {win_x}; O player win - {win_o}; Tie - {tie}.\n")

def play_interface(opponent_player):
    """Play Tic-Tac-Toe with the interface
    Opponent: human_player, smart_machine_player, random_machine_player"""
    import tkinter as tk
    import sys, platform
    # Fix graphic on Win 10
    if sys.platform == "win32" and platform.release() == "10":
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    def game(x_player="human_player_tk", o_player="human_player_tk"):
        def human_player_tk(board, player=None):
            # Printing a board (creating buttons with the ability to click on them for move)
            item = -1
            for y in range(3):
                for x in range(3):
                    item += 1
                    b = tk.Button(frame_down, text=board[item], width=6, height=2, font=("Helvetica", 16), state=button_state[0], relief="ridge", disabledforeground='black')
                    b.grid(row=y,column=x)
                    if player != None: # If this a move, not a simple printing
                        b["command"] = lambda item=item: click_on_board(board, player, item)
                    buttons_for_destroying.append(b)
            return board
        def click_on_board(board, player, item):
            if board[item] == " ":
                board[item] = player
                for b in buttons_for_destroying: # Destroy old buttons
                    b.destroy()
                buttons_for_destroying.clear()
                board = human_player_tk(board)
                free_spaces = count_spaces(board)
                result = check_winner_tk(board, free_spaces)
                if result == "":
                    if player == "X":
                        board = o_player(board, "O", free_spaces)
                    elif player == "O":
                        board = x_player(board, "X", free_spaces)
                    free_spaces = count_spaces(board)
                    result = check_winner_tk(board, free_spaces)
            board = human_player_tk(board, player)
        def check_winner_tk(board, free_spaces):
            result = check_winner(board, free_spaces)
            if result == "X":
                button_state[0] = "disabled"
                label_count["text"] = "X win"
            elif result == "O":
                button_state[0] = "disabled"
                label_count["text"] = "O win"
            elif result == "tie":
                button_state[0] = "disabled"
                label_count["text"] = "Tie"
            return result
        # Start new game
        board = [" " for _ in range(9)]
        label_count["text"] = ""
        button_state = ["normal"]
        buttons_for_destroying = []
        if x_player == "human_player_tk":
            x_player = human_player_tk
            board = x_player(board, "X")
        elif o_player == "human_player_tk":
            o_player = human_player_tk
            free_spaces = count_spaces(board)
            board = x_player(board, "X", free_spaces)
            board = o_player(board, "O")
    # Windows settings
    window = tk.Tk()
    window.resizable(False, False)
    window.minsize(width=250, height=260)
    window.title("Tic-Tac-Toe")
    window.iconphoto(False, tk.PhotoImage(file="data/tic_tac_toe.png"))
    frame_up = tk.Frame(window, border=5)
    frame_up.pack()
    frame_down = tk.Frame(window, border=5)
    frame_down.pack()
    button_x = tk.Button(frame_up, text="X", width=6, height=1, font=("Helvetica", 16), relief="ridge")
    button_x.pack(side="left")
    button_x["command"] = lambda: game(o_player=opponent_player)
    label_count = tk.Button(frame_up, width=6, height=1, font=("Helvetica", 16), relief="ridge", state="disabled", disabledforeground='red', bg="black")
    label_count.pack(side="left")
    button_o = tk.Button(frame_up, text="O", width=6, height=1, font=("Helvetica", 16), relief="ridge")
    button_o.pack(side="right")
    button_o["command"] = lambda: game(x_player=opponent_player)
    window.mainloop()

if __name__ == '__main__':
    # Players: human_player, random_machine_player, smart_machine_player
    # Game options: play_once(x_player, o_player), play_more_games(number_of_games, x_player, o_player), play_interface(opponent_player)
    play_interface(random_machine_player)