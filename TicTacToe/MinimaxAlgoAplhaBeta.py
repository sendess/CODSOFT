import random
import os

# the actual game board list
board = [' ' for _ in range(0, 9)]
sample_board = [i+1 for i in range(0,9)]

# to draw the game board and a sample board to let know position to place symbols
def draw_board():
    print("Positions on the board now are:\n")
    row_first = '| {} | {} | {} |'.format(board[0], board[1], board[2])
    row_second = '| {} | {} | {} |'.format(board[3], board[4], board[5])
    row_third = '| {} | {} | {} |'.format(board[6], board[7], board[8])
    row_first_sample = '| {} | {} | {} |'.format(sample_board[0], sample_board[1], sample_board[2])
    row_second_sample = '| {} | {} | {} |'.format(sample_board[3], sample_board[4], sample_board[5])
    row_third_sample = '| {} | {} | {} |'.format(sample_board[6], sample_board[7], sample_board[8])
    print()
    print(row_first+"\t\t"+row_first_sample)
    print(row_second+"\t\t"+row_second_sample)
    print(row_third+"\t\t"+row_third_sample)
    print()

# to handle player's moves
def player_move(symbol):
    run = True
    while run:
        move = input(f'Please select a position to place an \'{symbol}\' (1-9): ')
        try:
            move = int(move)
            if 1 <= move <= 9:
                if vacant_space(move):
                    insert_playing_symbol(symbol, move)
                    run = False
                else:
                    print('Not a legal move, Slot preoccupied')
            else:
                print('Please type a number within the range!')
        except ValueError:
            print('Please type a number')

#to handle AI moves using minmax inside of it.
def ai_move(ai_sym, first_run):
    if first_run == 1:
        best_step = random.randint(1, 9)
        while not vacant_space(best_step):
            best_step = random.randint(1, 9)
        insert_playing_symbol(ai_sym, best_step)
        return True
    else:
        best_scenario = float('-inf') if ai_sym == 'O' else float('inf')
        best_step = None
        for i in range(9):
            if board[i] == ' ':
                board[i] = ai_sym
                score = minimax(board, 0, ai_sym == 'X', float('-inf'), float('inf'))
                board[i] = ' '
                if (ai_sym == 'O' and score > best_scenario) or (ai_sym == 'X' and score < best_scenario):
                    best_scenario = score
                    best_step = i
        
        if best_step is not None:
            insert_playing_symbol(ai_sym, best_step + 1)
        else:
            print("No valid moves available for AI")


# to check if requested spot/ place by player is vacant or not
def vacant_space(pos):
    return board[pos - 1] == ' '

# to insert the player symbol into the board
def insert_playing_symbol(letter, pos):
    board[pos - 1] = letter
    sample_board[pos - 1] = ' '

# to check if the board is full for draw condition
def is_board_full():
    return ' ' not in board

# to check for the winning condition with all winning possible placements
def is_winner(letter):
    winning_placements = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for places in winning_placements:
        if board[places[0]] == board[places[1]] == board[places[2]] == letter:
            return True
    return False

# Recursive minimax function Alpha-Beta pruning implementation 
def minimax(board, depth, is_maximizing, alpha, beta):
    if is_winner('O'):
        return 10 - depth
    elif is_winner('X'):
        return depth - 10
    elif is_board_full():
        return 0

    if is_maximizing:
        best_scenario = float('-inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, depth + 1, False, alpha, beta)
                board[i] = ' '
                best_scenario = max(score, best_scenario)
                alpha = max(alpha, best_scenario)
                if beta <= alpha:
                    break
        return best_scenario
    else:
        best_scenario = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, depth + 1, True, alpha, beta)
                board[i] = ' '
                best_scenario = min(score, best_scenario)
                beta = min(beta, best_scenario)
                if beta <= alpha:
                    break
        return best_scenario

# Loop for main game to repeat until winning case of any player
def main():
    c = 0
    run = True
    os.system('cls')
    print('You are welcome to the unbeatable tic tac toe!!')
    print("Please choose your playing symbol")
    print("\n\t1. O\n\t2. X")
    choice = input()
    choice = choice.upper()
    if choice == "1" or choice == "O":
        sym = "O"
    elif choice == "2" or choice == "X":
        sym = "X"
    else:
        print("Invalid choice! Retry")
        main()
        return
    
    print(f"Your symbol is {sym}")
    ai_sym = "X" if sym == "O" else "O"

    while run:
        if sym == "X":
            draw_board()
            player_move(sym)
            if is_winner('X'):
                draw_board()
                print('You Win')
                break
            elif is_board_full():
                draw_board()
                print('Draw')
                break
            ai_move(ai_sym,0)
            if is_winner('O'):
                draw_board()
                print('You Lose')
                break
        else:
            if c == 0:
                c+=1
                ai_move(ai_sym,1)
            else:
                ai_move(ai_sym,0)
            draw_board()
            if is_winner('X'):
                draw_board()
                print('You Lose')
                break
            elif is_board_full():
                draw_board()
                print('Draw')
                break
            player_move(sym)
            if is_winner('O'):
                draw_board()
                print('You Win')
                break

if __name__ == '__main__':
    main()
