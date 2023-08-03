import sys, platform, random, time, tkinter as tk

def add_mines_numbers(board, mines):
    # Add mines
    for _ in range(mines):
        not_ready = True
        while not_ready == True:
            space1 = random.randint(0,len(board) - 1)
            space2 = random.randint(0,len(board) - 1)
            if board[space1][space2] == " ":
                board[space1][space2] = "✶"
                not_ready = False
    # Add numbers for mines
    i_row = -1
    for row in board:
        i_row += 1
        i_item = -1
        for item in row:
            mines_count = 0
            i_item += 1
            if item == " ":# This item - board[i_row][i_item]
                if i_row - 1 >= 0:
                    if i_item - 1 >= 0:
                        if board[i_row - 1][i_item - 1] == "✶":# Up left
                            mines_count += 1
                    if board[i_row - 1][i_item] == "✶":# Up
                        mines_count += 1
                    try:
                        if board[i_row - 1][i_item + 1] == "✶":# Up right
                            mines_count += 1
                    except:pass
                if i_item - 1 >= 0:
                    if board[i_row][i_item - 1] == "✶":# Left
                        mines_count += 1
                try:
                    if board[i_row][i_item + 1] == "✶":# Right
                        mines_count += 1
                except:pass
                try:
                    if i_item - 1 >= 0:
                        if board[i_row + 1][i_item - 1] == "✶":# Down left
                            mines_count += 1
                    if board[i_row + 1][i_item] == "✶":# Down
                        mines_count += 1
                    if board[i_row + 1][i_item + 1] == "✶":# Down right
                        mines_count += 1
                except:pass
                # Add number
                if mines_count > 0:
                    board[i_row][i_item] = str(mines_count)
    return board

def scan_empty_around_marks(board_2):
    # If around marks found open empty spaces - open this mark
    i_row = -1
    for row in board_2:
        i_row += 1
        i_item = -1
        for item in row:
            i_item += 1
            if item == "►":
                empty_around_marks = 0
                if i_row - 1 >= 0:
                    if i_item - 1 >= 0:
                        if board_2[i_row - 1][i_item - 1] == " ":# Up left
                            empty_around_marks += 1
                    if board_2[i_row - 1][i_item] == " ":# Up
                        empty_around_marks += 1
                    try:
                        if board_2[i_row - 1][i_item + 1] == " ":# Up right
                            empty_around_marks += 1
                    except:pass
                if i_item - 1 >= 0:
                    if board_2[i_row][i_item - 1] == " ":# left
                        empty_around_marks += 1
                try:
                    if board_2[i_row][i_item + 1] == " ":# right
                        empty_around_marks += 1
                except:pass
                if i_row + 1 <= len(board_2) - 1:
                    if i_item - 1 >= 0:
                        if board_2[i_row + 1][i_item - 1] == " ":# Down left
                            empty_around_marks += 1
                    if board_2[i_row + 1][i_item] == " ":# Down
                        empty_around_marks += 1
                    try:
                        if board_2[i_row + 1][i_item + 1] == " ":# Down right
                            empty_around_marks += 1
                    except:pass
                # Open empty space
                if empty_around_marks >= 1:
                    board_2[i_row][i_item] = " "  
    return board_2

def scan_space(board, board_2, item_y, item_x):
    directions = []
    # Open empty spaces
    if board[item_y][item_x] == " ":
        board_2[item_y][item_x] = " "
        # Scan empty spaces on directions
        if item_y - 1 >= 0:
            if board[item_y - 1][item_x] == " " and (board_2[item_y - 1][item_x] == "-" or board_2[item_y - 1][item_x] == "►"):# Up
                directions.append([item_y - 1, item_x])
        if item_x - 1 >= 0:
            if board[item_y][item_x - 1] == " " and (board_2[item_y][item_x - 1] == "-" or board_2[item_y][item_x - 1] == "►"):# Left
                directions.append([item_y, item_x - 1])
        try:
            if board[item_y][item_x + 1] == " " and (board_2[item_y][item_x + 1] == "-" or board_2[item_y][item_x + 1] == "►"):# Right
                directions.append([item_y, item_x + 1])
        except:pass
        if item_y + 1 <= len(board) - 1:
            if board[item_y + 1][item_x] == " " and (board_2[item_y + 1][item_x] == "-" or board_2[item_y + 1][item_x] == "►"):# Down
                directions.append([item_y + 1, item_x])
        # Looks into next empty spaces
        ready = False
        counter1 = 0
        while ready == False:
            try:
                board_2 = scan_space(board, board_2, directions[counter1][0], directions[counter1][1])
                counter1 += 1
            except:
                ready = True
        # Opening numbers near by empty"s
        if item_y - 1 >= 0:
            if board[item_y - 1][item_x] != " ":
                board_2[item_y - 1][item_x] = board[item_y - 1][item_x]# Up
            if item_x - 1 >= 0:
                if board[item_y - 1][item_x - 1] != " ":
                    board_2[item_y - 1][item_x - 1] = board[item_y - 1][item_x - 1]# Up left
            try:
                if board[item_y - 1][item_x + 1] != " ":
                    board_2[item_y - 1][item_x + 1] = board[item_y - 1][item_x + 1]# Up right
            except:pass
        if item_x - 1 >= 0:
            if board[item_y][item_x - 1] != " ":
                board_2[item_y][item_x - 1] = board[item_y][item_x - 1]# Left
        try:
            if board[item_y][item_x + 1] != " ":
                board_2[item_y][item_x + 1] = board[item_y][item_x + 1]# Right
        except:pass
        if item_y + 1 <= len(board) - 1:
            if board[item_y + 1][item_x] != " ":
                board_2[item_y + 1][item_x] = board[item_y + 1][item_x]# Down
            if item_x - 1 >= 0:
                if board[item_y + 1][item_x - 1] != " ":
                    board_2[item_y + 1][item_x - 1] = board[item_y + 1][item_x - 1]# Down left
            try:
                if board[item_y + 1][item_x + 1] != " ":
                    board_2[item_y + 1][item_x + 1] = board[item_y + 1][item_x + 1]# Down right
            except:pass
    # Open number
    elif board[item_y][item_x] != " " and board[item_y][item_x] != "✶":
        board_2[item_y][item_x] = board[item_y][item_x]
    # Lose
    elif board[item_y][item_x] == "✶":
        # Count and show mines
        iter = -1
        for row in board:
            iter += 1
            index = -1
            for item in row:
                index += 1
                if item == "✶":
                    if board_2[iter][index] == "►":
                        board_2[iter][index] = "▷"
                    else:
                        board_2[iter][index] = "✶"
        board_2[item_y][item_x] = "X"
        return board_2
    return board_2

def mark_mine(board_2, item_y, item_x):
    if board_2[item_y][item_x] == "-":
        board_2[item_y][item_x] = "►"
    elif board_2[item_y][item_x] == "►":
        board_2[item_y][item_x] = "-"
    return board_2

def check_win(board_2):
    mine = False
    hidden_spaces = 0
    for row in board_2:
        for item in row:
            if item == "X":
                mine = True
            if item == "-":
                hidden_spaces += 1
    if mine == True:
        return "lose"
    if hidden_spaces == 0:
        return "win"
    else:
        return None

def print_board(board):
    """Print board on the command line"""
    y = 0
    print("")
    # Upper row
    list_x = []
    for i in range(len(board)):
        if len(str(i + 1)) == 2:
            list_x.append(str(i + 1))
        else:
            list_x.append(str(i + 1) + " ")
    print("  " + "   " + "  ".join(list_x))
    print("--" + "---" + "---".join(["-" for i in range(len(board))]) + "--")
    for i in board:
        # Left column
        y += 1
        y1 = f"{y} "
        if len(str(y)) == 2:
            y1 = f"{y}"
        # Board row
        print(y1 + " | " + " | ".join(i) + " |")
    print("")

def player_input(board, board_2):
    """Player input on the command line"""
    while True:
        player_input = input("Write 'Y X' or 'Y X m' for mark mine (eg: '2 1', '2 1 m'): ")
        input_item = player_input.split() # ["2", "1"]
        if len(input_item) == 2 or len(input_item) == 3:
            try:
                input_item[0] = int(input_item[0]) - 1
                input_item[1] = int(input_item[1]) - 1
                if board[input_item[0]][input_item[1]]:
                    if board_2[input_item[0]][input_item[1]] == "-" or board_2[input_item[0]][input_item[1]] == "►":
                        return input_item
                    else:
                        print("Space already open")
            except IndexError:
                print("Incorrect space")
            except ValueError:
                print("Incorrect value")
        else:
            print("Incorrect value")

def play_command_line(board_size=10, mines=13):
    """Play Minesweeper on the command line
    Board size: width and height of the board (rec ≈ 20)
    Mines: number of mines"""
    board = [[" " for _ in range(board_size)] for _ in range(board_size)]
    board = add_mines_numbers(board, mines)
    board_2 = [["-" for _ in range(board_size)] for _ in range(board_size)]
    result = None
    start = time.time()
    while result == None:
        board_2 = scan_empty_around_marks(board_2)
        print_board(board_2)
        input_item = player_input(board, board_2)
        if len(input_item) == 3:
            board_2 = mark_mine(board_2, input_item[0], input_item[1])
        elif len(input_item) == 2 and board_2[input_item[0]][input_item[1]] != "►":
            board_2 = scan_space(board, board_2, input_item[0], input_item[1])
        result = check_win(board_2)
    if result == "lose":
        end = time.time()
        print_board(board_2)
        print(f"BOOM !!! Game over in {int(end - start)} seconds\n")
    if result == "win":
        end = time.time()
        print_board(board_2)
        print(f"You won in {int(end - start)} seconds\n")

def play_interface(board_size=10, mines=13):
    """Play Minesweeper with the interface
    Board size: width and height of the board (rec ≈ 20)
    Mines: number of mines"""
    def game(board_size, mines):
        def new_game():
            result[0] = "lose"
            button_state[0] = "disabled"
            label_count["text"] = counter
            label_mines["text"] = mines
            button_new_game.destroy()
            for b in buttons_for_destroying: # Destroy old buttons
                b.destroy()
            buttons_for_destroying.clear()
            game(board_size, mines)
        def game_counter():
            if result[0] == None:
                counter[0] += 1
                label_count["text"] = str(counter[0])
                label_count.after(1000, game_counter)
        def reload_board(board_2):
            # Count mark mines and show it on label
            mines_mark = 0
            for row in board_2:
                for item in row:
                    if item == "►":
                        mines_mark += 1
            label_mines["text"] = mines - mines_mark
            # Create buttons
            item_y = -1
            for row in board_2:
                item_y += 1
                item_x = -1
                for item in row:
                    item_x += 1
                    b = tk.Button(frame_down, text=item, width=3, height=1, font=("Helvetica", 14), state=button_state[0], relief="ridge", disabledforeground='black')
                    b.grid(row=item_y,column=item_x)
                    b["command"] = lambda y=item_y, x=item_x: click_on_board(board_2, y, x)
                    if item != "-":
                        b["bg"] = "white"
                        b["state"] = "disabled"
                    if item == "X":
                        b["bg"] = "red"
                        b["text"] = "✶"
                    elif item == "►":
                        b["state"] = "disabled"
                        b["disabledforeground"] = "red"
                    elif item == "▷":
                        b["text"] = "►"
                        b["state"] = "disabled"                        
                    elif item == "-":
                        b["text"] = " "
                    elif item == "1":
                        b["disabledforeground"] = "blue"
                    elif item == "2":
                        b["disabledforeground"] = "green"
                    elif item == "3":
                        b["disabledforeground"] = "red"
                    elif item == "4":
                        b["disabledforeground"] = "blue4"
                    elif item == "5":
                        b["disabledforeground"] = "brown"
                    elif item == "6":
                        b["disabledforeground"] = "brown4"
                    elif item == "7":
                        b["disabledforeground"] = "orange"
                    b.bind('<Button-3>',  lambda event, y=item_y, x=item_x:right_click_on_board(board_2, y, x))
                    buttons_for_destroying.append(b)
            return board_2
        def click_on_board(board_2, y, x):
            if board_2[y][x] != "►":
                board_2 = scan_space(board, board_2, y, x)
                result[0] = check_win(board_2)
                if result[0] == "lose":
                    button_state[0] = "disabled"
                    label_count["text"] = counter
                    label_mines["text"] = mines
                    button_new_game["text"] = "☠"
                if result[0] == "win":
                    button_state[0] = "disabled"
                    label_count["text"] = counter
                    label_mines["text"] = mines
                    button_new_game["text"] = "👍"
                board_2 = scan_empty_around_marks(board_2)
                for b in buttons_for_destroying: # Destroy old buttons
                    b.destroy()
                buttons_for_destroying.clear()
                board_2 = reload_board(board_2)
        def right_click_on_board(board_2, y, x):
            if result[0] == None:
                board_2 = mark_mine(board_2, y, x)
                for b in buttons_for_destroying: # Destroy old buttons
                    b.destroy()
                buttons_for_destroying.clear()
                board_2 = reload_board(board_2)
            result[0] = check_win(board_2)
            if result[0] == "win":
                button_state[0] = "disabled"
                label_count["text"] = counter
                label_mines["text"] = mines
                button_new_game["text"] = "👍"
        # Start new game
        button_new_game = tk.Button(frame_up, width=6, height=1, font=("Helvetica", 14), relief="ridge", foreground="black")
        button_new_game.pack(side="left")
        button_new_game["command"] = lambda: new_game()
        button_new_game["text"] = "😁"
        result = [None]
        counter = [0]
        game_counter()
        board = [[" " for _ in range(board_size)] for _ in range(board_size)]
        board = add_mines_numbers(board, mines)
        board_2 = [["-" for _ in range(board_size)] for _ in range(board_size)]
        button_state = ["normal"]
        board_2 = scan_empty_around_marks(board_2)
        buttons_for_destroying = []
        board_2 = reload_board(board_2)
    # Fix graphic on Win 10
    if sys.platform == "win32" and platform.release() == "10":
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    # Windows settings
    window = tk.Tk()
    window.resizable(False, False)
    window.title("Minesweeper")
    window.iconphoto(False, tk.PhotoImage(file="data/minesweeper.png"))
    frame_up = tk.Frame(window, border=3)
    frame_up.pack()
    frame_down = tk.Frame(window, border=3)
    frame_down.pack()
    label_mines = tk.Button(frame_up, text=mines, width=6, height=1, font=("Helvetica", 14), relief="ridge", state="disabled", disabledforeground='red', bg="black")
    label_mines.pack(side="left", padx=40)
    label_count = tk.Button(frame_up, width=6, height=1, font=("Helvetica", 14), relief="ridge", state="disabled", disabledforeground='red', bg="black")
    label_count.pack(side="right", padx=40)
    game(board_size, mines)
    window.mainloop()

if __name__ == "__main__":
    # Game options: play_command_line(board_size, mines), play_interface(board_size, mines)
    play_interface()