import random
import math
import time

def initialize_board():
    # Create an empty board
    board = [[' ' for _ in range(16)] for _ in range(16)]
    
    # Place player 1's pieces
    # for i in range(5):
    #     for j in range(5):
    #         board[i][j] = 'x'
    # board[2][4] = ' '
    # board[3][3] = ' '
    # board[3][4] = ' '
    # board[4][2] = ' '
    # board[4][3] = ' '
    # board[4][4] = ' '
    
    # Place player 2's pieces
    # for i in range(11, 16):
    #     for j in range(11, 16):
    #         board[i][j] = 'o'

    # board[11][11] = ' '
    # board[11][12] = ' '
    # board[11][13] = ' '
    # board[12][11] = ' '
    # board[12][12] = ' '
    # board[13][11] = ' '

    o_starting = [(14, 11), (15, 11), (13, 12), (14, 12), (15, 12), (12, 13), (13, 13), (14, 13), (15, 13), (11, 14), (12, 14), (13, 14), (14, 14), (15, 14), (11, 15), (12, 15), (13, 15), (14, 15), (15, 15)]
    for i, j in o_starting:
        board[i][j] = 'o'
    
    x_starting = o_winning = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (0, 2), (1, 2), (2, 2), (3, 2), (0, 3), (1, 3), (2, 3), (0, 4), (1, 4)]
    for i, j in x_starting:
        board[i][j] = 'x'
    
    return board

def initialize_board_from_file(filename):
    # The file should have the following format:
    # 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0
    # 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0
    # 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0
    # 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0
    # 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    # 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    # 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    # 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    # 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    # 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    # 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    # 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1
    # 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1
    # 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1
    # 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1
    # 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1

    board = []
    with open(filename, 'r') as f:
        for line in f:
            # change 2 to 'x' and 1 to 'o'
            row = line.strip().split(' ')
            row = ['x' if x == '2' else 'o' if x == '1' else ' ' for x in row]
            board.append(row)
    return board

def display_board(board):
    print("    0 1 2 3 4 5 6 7 8 9 A B C D E F")
    print("    --------------------------------")
    for i in range(16):
        print(hex(i)[2:].upper(), '|', end=' ')
        for j in range(16):
            print(board[i][j], end=' ')
        print('|')
    print("    --------------------------------")

def legal_moves(board, player):
    # player is either 'x' or 'o'
    moves = []
    for i in range(16):
        for j in range(16):
            if board[i][j] == player:
                # Check all basic moves
                # up
                if i > 0 and board[i-1][j] == ' ':
                    moves.append([(i, j, i-1, j)])
                # down
                if i < 15 and board[i+1][j] == ' ':
                    moves.append([(i, j, i+1, j)])
                # left
                if j > 0 and board[i][j-1] == ' ':
                    moves.append([(i, j, i, j-1)])
                # right
                if j < 15 and board[i][j+1] == ' ':
                    moves.append([(i, j, i, j+1)])
                # up-left
                if i > 0 and j > 0 and board[i-1][j-1] == ' ':
                    moves.append([(i, j, i-1, j-1)])
                # up-right
                if i > 0 and j < 15 and board[i-1][j+1] == ' ':
                    moves.append([(i, j, i-1, j+1)])
                # down-left
                if i < 15 and j > 0 and board[i+1][j-1] == ' ':
                    moves.append([(i, j, i+1, j-1)])
                # down-right
                if i < 15 and j < 15 and board[i+1][j+1] == ' ':
                    moves.append([(i, j, i+1, j+1)])

                # now check all jump moves
                jumps = possible_jumps(board, player, i, j, [], [])
                for jump in jumps:
                    moves.append(jump)
    # cut moves 
    # return moves
    finished_moves = []
    for i in range(len(moves)):
        finished_moves.append(moves[i][0][0:2] + moves[i][-1][2:])
    return finished_moves

def possible_jumps(board, player, i, j, jump_prefix, used_positions = []):
    # player is either 'x' or 'o'
    # used positions is a list of (i, j) tuples which cant be used again in this turn
    jumps = []
    # Check all basic moves
    # up
    if i > 1 and board[i-1][j] != ' ' and board[i-2][j] == ' ' and (i-1, j) not in used_positions:
        jumps.append(jump_prefix + [(i, j, i-2, j)])
        further_jumps = possible_jumps(board, player, i-2, j, jump_prefix + [(i, j, i-2, j)], used_positions + [(i-1, j)])
        if further_jumps:
            jumps = jumps + further_jumps
    # down
    if i < 14 and board[i+1][j] != ' ' and board[i+2][j] == ' ' and (i+1, j) not in used_positions:
        jumps.append(jump_prefix + [(i, j, i+2, j)])
        further_jumps = possible_jumps(board, player, i+2, j, jump_prefix + [(i, j, i+2, j)], used_positions + [(i+1, j)])
        if further_jumps:
            jumps = jumps + further_jumps
    # left
    if j > 1 and board[i][j-1] != ' ' and board[i][j-2] == ' ' and (i, j-1) not in used_positions:
        jumps.append(jump_prefix + [(i, j, i, j-2)])
        further_jumps = possible_jumps(board, player, i, j-2, jump_prefix + [(i, j, i, j-2)], used_positions + [(i, j-1)])
        if further_jumps:
            jumps = jumps + further_jumps
    # right
    if j < 14 and board[i][j+1] != ' ' and board[i][j+2] == ' ' and (i, j+1) not in used_positions:
        jumps.append(jump_prefix + [(i, j, i, j+2)])
        further_jumps = possible_jumps(board, player, i, j+2, jump_prefix + [(i, j, i, j+2)], used_positions + [(i, j+1)])
        if further_jumps:
            jumps = jumps + further_jumps
    # up-left
    if i > 1 and j > 1 and board[i-1][j-1] != ' ' and board[i-2][j-2] == ' ' and (i-1, j-1) not in used_positions:
        jumps.append(jump_prefix + [(i, j, i-2, j-2)])
        further_jumps = possible_jumps(board, player, i-2, j-2, jump_prefix + [(i, j, i-2, j-2)], used_positions + [(i-1, j-1)])
        if further_jumps:
            jumps = jumps + further_jumps
    # up-right
    if i > 1 and j < 14 and board[i-1][j+1] != ' ' and board[i-2][j+2] == ' ' and (i-1, j+1) not in used_positions:
        jumps.append(jump_prefix + [(i, j, i-2, j+2)])
        further_jumps = possible_jumps(board, player, i-2, j+2, jump_prefix + [(i, j, i-2, j+2)], used_positions + [(i-1, j+1)])
        if further_jumps:
            jumps = jumps + further_jumps
    # down-left
    if i < 14 and j > 1 and board[i+1][j-1] != ' ' and board[i+2][j-2] == ' ' and (i+1, j-1) not in used_positions:
        jumps.append(jump_prefix + [(i, j, i+2, j-2)])
        further_jumps = possible_jumps(board, player, i+2, j-2, jump_prefix + [(i, j, i+2, j-2)], used_positions + [(i+1, j-1)])
        if further_jumps:
            jumps = jumps + further_jumps
    # down-right
    if i < 14 and j < 14 and board[i+1][j+1] != ' ' and board[i+2][j+2] == ' ' and (i+1, j+1) not in used_positions:
        jumps.append(jump_prefix + [(i, j, i+2, j+2)])
        further_jumps = possible_jumps(board, player, i+2, j+2, jump_prefix + [(i, j, i+2, j+2)], used_positions + [(i+1, j+1)])
        if further_jumps:
            jumps = jumps + further_jumps
    return jumps
    
def move(board, move):
    # move is a tuple of (i1, j1, i2, j2)
    i1, j1, i2, j2 = move
    new_board = [row.copy() for row in board]
    new_board[i2][j2] = new_board[i1][j1]
    new_board[i1][j1] = ' '
    return new_board

def is_blocked(board, i, j):
    blocking_piece = 'x'
    if board[i][j] == 'x':
        blocking_piece = 'o'
    
    # up
    if i > 0 and board[i-1][j] != blocking_piece:
        return False
    if i > 1 and board[i-2][j] != blocking_piece:
        return False
    # down
    if i < 15 and board[i+1][j] != blocking_piece:
        return False
    if i < 14 and board[i+2][j] != blocking_piece:
        return False
    # left
    if j > 0 and board[i][j-1] != blocking_piece:
        return False
    if j > 1 and board[i][j-2] != blocking_piece:
        return False
    # right
    if j < 15 and board[i][j+1] != blocking_piece:
        return False
    if j < 14 and board[i][j+2] != blocking_piece:
        return False
    # up-left
    if i > 0 and j > 0 and board[i-1][j-1] != blocking_piece:
        return False
    if i > 1 and j > 1 and board[i-2][j-2] != blocking_piece:
        return False
    # up-right
    if i > 0 and j < 15 and board[i-1][j+1] != blocking_piece:
        return False
    if i > 1 and j < 14 and board[i-2][j+2] != blocking_piece:
        return False
    # down-left
    if i < 15 and j > 0 and board[i+1][j-1] != blocking_piece:
        return False
    if i < 14 and j > 1 and board[i+2][j-2] != blocking_piece:
        return False
    # down-right
    if i < 15 and j < 15 and board[i+1][j+1] != blocking_piece:
        return False
    if i < 14 and j < 14 and board[i+2][j+2] != blocking_piece:
        return False
    return True

def is_winning(board, player):
    for i in range(16):
        for j in range(16):
            if board[i][j] != player and board[i][j] != ' ' and is_blocked(board, i, j) == True:
                return True
    
    x_winning = [(14, 11), (15, 11), (13, 12), (14, 12), (15, 12), (12, 13), (13, 13), (14, 13), (15, 13), (11, 14), (12, 14), (13, 14), (14, 14), (15, 14), (11, 15), (12, 15), (13, 15), (14, 15), (15, 15)]
    for i, j in x_winning:
        if board[i][j] != 'x' and player == 'x':
            return False

    o_winning = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (0, 2), (1, 2), (2, 2), (3, 2), (0, 3), (1, 3), (2, 3), (0, 4), (1, 4)]
    for i, j in o_winning:
        if board[i][j] != 'o' and player == 'o':
            return False
        
    return True

def heuristic_random(board):
    return random.randint(-100, 100)

def heuristic_euklides(board):
    # player is either 'x' or 'o'
    cornerx = (0, 0)
    cornero = (15, 15)
    distance = 0
    for i in range(16):
        for j in range(16):
            if board[i][j] == 'x':
                distance += (i - cornerx[0])**2 + (j - cornerx[1])**2
            elif board[i][j] == 'o':
                distance -= (i - cornero[0])**2 + (j - cornero[1])**2
    return distance

def heuristic_manhattan(board):
    cornerx = (0, 0)
    cornero = (15, 15)
    distance = 0
    for i in range(16):
        for j in range(16):
            if board[i][j] == 'x':
                distance += abs(i - cornerx[0]) + abs(j - cornerx[1])
            elif board[i][j] == 'o':
                distance -= abs(i - cornero[0]) + abs(j - cornero[1])
    return distance
    corner = (15, 15)
    distance = 0
    for i in range(16):
        for j in range(16):
            if board[i][j] == 'o':
                distance -= abs(i - corner[0]) + abs(j - corner[1])
    return distance

def heuristic_euklides_with_center(board):
    cornerx = (0, 0)
    cornero = (15, 15)
    center = (7, 7)
    distance = 0
    for i in range(16):
        for j in range(16):
            if board[i][j] == 'x':
                distance += ((i - cornerx[0])**2 + (j - cornerx[1])**2) - 0.1 * ((i - center[0])**2 + (j - center[1])**2)
            elif board[i][j] == 'o':
                distance -= ((i - cornero[0])**2 + (j - cornero[1])**2) - - 0.1 * ((i - center[0])**2 + (j - center[1])**2)
    return distance

def heuristic_manhattan_with_center(board):
    cornerx = (0, 0)
    cornero = (15, 15)
    center = (7.5, 7.5)
    distance = 0
    for i in range(16):
        for j in range(16):
            if board[i][j] == 'x':
                distance += (abs(i - cornerx[0]) + abs(j - cornerx[1])) - 0.1 * (abs(i - center[0]) + abs(j - center[1]))
            elif board[i][j] == 'o':
                distance -= (abs(i - cornero[0]) + abs(j - cornero[1])) - 0.1 * (abs(i - center[0]) + abs(j - center[1]))
    return distance

def heuristic_euklides_with_groupping(board):
    cornerx = (0, 0)
    cornero = (15, 15)
    distance = 0
    x_pieces = []
    o_pieces = []
    for i in range(16):
        for j in range(16):
            if board[i][j] == 'x':
                distance += (i - cornerx[0])**2 + (j - cornerx[1])**2
                x_pieces.append((i, j))
            elif board[i][j] == 'o':
                distance -= (i - cornero[0])**2 + (j - cornero[1])**2
                o_pieces.append((i, j))
    
    for x1 in x_pieces:
        for x2 in x_pieces:
            distance -= 0.01 * ((x1[0] - x2[0])**2 + (x1[1] - x2[1])**2)
    for o1 in o_pieces:
        for o2 in o_pieces:
            distance += 0.01 * ((o1[0] - o2[0])**2 + (o1[1] - o2[1])**2)
    return distance

def heuristic_manhattan_with_groupping(board):
    cornerx = (0, 0)
    cornero = (15, 15)
    distance = 0
    x_pieces = []
    o_pieces = []
    for i in range(16):
        for j in range(16):
            if board[i][j] == 'x':
                distance += abs(i - cornerx[0]) + abs(j - cornerx[1])
                x_pieces.append((i, j))
            elif board[i][j] == 'o':
                distance -= abs(i - cornero[0]) + abs(j - cornero[1])
                o_pieces.append((i, j))
    
    for x1 in x_pieces:
        for x2 in x_pieces:
            distance -= 0.01 * (abs(x1[0] - x2[0]) + abs(x1[1] - x2[1]))
    for o1 in o_pieces:
        for o2 in o_pieces:
            distance += 0.01 * (abs(o1[0] - o2[0]) + abs(o1[1] - o2[1]))
    return distance

def heuristic_finish_places(board):
    x_winning = [(14, 11), (15, 11), (13, 12), (14, 12), (15, 12), (12, 13), (13, 13), (14, 13), (15, 13), (11, 14), (12, 14), (13, 14), (14, 14), (15, 14), (11, 15), (12, 15), (13, 15), (14, 15), (15, 15)]
    o_winning = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (0, 2), (1, 2), (2, 2), (3, 2), (0, 3), (1, 3), (2, 3), (0, 4), (1, 4)]
    
    # check how many pieces are in the winning places
    x_counter = 0
    x_sad_pieces = []
    o_counter = 0
    o_sad_pieces = []
    for i in range(16):
        for j in range(16):
            if board[i][j] == 'x' and (i, j) in x_winning:
                x_counter += 1
                x_winning.remove((i, j))
            else:
                x_sad_pieces.append((i, j))

            if board[i][j] == 'o' and (i, j) in o_winning:
                o_counter += 1
                o_winning.remove((i, j))
            else:
                o_sad_pieces.append((i, j))
    return x_counter - o_counter
    val =  x_counter - o_counter 
    for x in x_sad_pieces:
        # substract the distance the closest free winning place
        min_distance = 100
        for w in x_winning:
            distance = (x[0] - w[0])**2 + (x[1] - w[1])**2
            if distance < min_distance:
                min_distance = distance
        val -= min_distance
    for o in o_sad_pieces:
        # substract the distance the closest free winning place
        min_distance = 100
        for w in o_winning:
            distance = (o[0] - w[0])**2 + (o[1] - w[1])**2
            if distance < min_distance:
                min_distance = distance
        val += min_distance
    return val

def heuristic_adaptive(board):
    # if all pieces are in the 'final region' of the board, use the euklides heuristic
    # otherwise use the eukides with center heuristic
    okx = True
    oko = True
    val = 5
    for i in range(16):
        for j in range(16):
            if board[i][j] == 'x' and i < val and j < val:
                okx = False
            if board[i][j] == 'o' and i > 15 - val and j > 15 - val:
                oko = False
            # if board[i][j] == 'x' and 15 - i + 15 - j > val:
            #     okx = False
            # if board[i][j] == 'o' and i + j > val:
            #     oko = False
    if okx or oko:
        # print("Using finish heuristic")
        return heuristic_finish_places(board)
    
    # print("Using euklides heuristic")
    return heuristic_manhattan(board)

def minimax(board, curDepth = 0, maxTurn = True, heuristicx = heuristic_manhattan, heuristico = heuristic_random, targetDepth = 2):
    if curDepth == targetDepth:
        if maxTurn:
            return heuristicx(board), None
        else:
            return heuristico(board), None
    
    if maxTurn:
        possibilities = legal_moves(board, 'x')
        best_val = -math.inf
        best_move = None
        for amove in possibilities:
            if amove == None:
                continue
            new_board = move(board, amove)
            (new_val, _) = minimax(new_board, curDepth + 1, False, heuristicx, heuristico, targetDepth)
            if new_val == None or best_val == None:
                continue
            if new_val > best_val:
                best_val = new_val
                best_move = amove
        return (best_val, best_move)
    else:
        possibilities = legal_moves(board, 'o')
        best_val = math.inf
        best_move = None
        for amove in possibilities:
            if amove == None:
                continue
            new_board = move(board, amove)
            (new_val, _) = minimax(new_board, curDepth + 1, True, heuristicx, heuristico, targetDepth)
            if new_val == None or best_val == None:
                continue
            if new_val < best_val:
                best_val = new_val
                best_move = amove
        return (best_val, best_move)
    
board = initialize_board_from_file('board.txt')
# board = initialize_board()

# Display the board
# display_board(board)

# Get all legal moves for player 1
# moves = legal_moves(board, 'o')
# print(len(moves))   
# for move in moves:
#     print(move)

# let two players play against each other
def play_game_minimax(board, heura_x, heura_o, depth_x, depth_o):
    while (is_winning(board, 'x') == False and is_winning(board, 'o') == False):
        # player 1
        (_, best_move) = minimax(board, 0, True, heura_x, heura_o, depth_x)
        board = move(board, best_move)
        display_board(board)
        if is_winning(board, 'x'):
            print("Player 1 wins!")
            break
        # player 2
        (_, best_move) = minimax(board, 0, False, heura_x, heura_o, depth_o)
        board = move(board, best_move)
        display_board(board)
        if is_winning(board, 'o'):
            print("Player 2 wins!")
            break
# TASK 3
# play_game_minimax(board, heuristic_adaptive, heuristic_random, 1, 1)

MAX, MIN = 10000000, -10000000
def minimaxAB(board, alfa, beta, curDepth = 0, maxTurn = True, heuristicx = heuristic_manhattan, heuristico = heuristic_random, targetDepth = 3):
    if curDepth == targetDepth:
        if maxTurn:
            return heuristicx(board), None
        else:
            return heuristico(board), None
        
    if maxTurn:
        possibilities = legal_moves(board, 'x')
        best_val = -MAX
        best_move = None
        for amove in possibilities:
            new_board = move(board, amove)
            (new_val, _) = minimaxAB(new_board, alfa, beta, curDepth + 1, False, heuristicx, heuristico, targetDepth)
            if new_val > best_val:
                best_val = new_val
                best_move = amove
            alfa = max(alfa, best_val)
            if beta <= alfa:
                break
        return (best_val, best_move)
    
    else:
        possibilities = legal_moves(board, 'o')
        best_val = MAX
        best_move = None
        for amove in possibilities:
            new_board = move(board, amove)
            (new_val, _) = minimaxAB(new_board, alfa, beta, curDepth + 1, True, heuristicx, heuristico, targetDepth)
            if new_val < best_val:
                best_val = new_val
                best_move = amove
            beta = min(beta, best_val)
            if beta <= alfa:
                break
        return (best_val, best_move)
    
def play_game_minimaxAB(board, heura_x, heura_o, depth_x, depth_o):
    while (is_winning(board, 'x') == False and is_winning(board, 'o') == False):
        # player 1
        (_, best_move) = minimaxAB(board, MIN, MAX, 0, True, heura_x, heura_o, depth_x)
        board = move(board, best_move)
        display_board(board)
        if is_winning(board, 'x'):
            print("Player 1 wins!")
            break
        # player 2
        (_, best_move) = minimaxAB(board, MIN, MAX, 0, False, heura_o, heura_x, depth_o)
        board = move(board, best_move)
        display_board(board)
        if is_winning(board, 'o'):
            print("Player 2 wins!")
            break

# TASK 4
# play_game_minimaxAB(board, heuristic_adaptive, heuristic_random, 2, 1)

def play_game_minimaxAB_vs_user(board, heura_x, depth_x):
    while (is_winning(board, 'x') == False and is_winning(board, 'o') == False):
        # player 1
        MAX, MIN = 10000000, -10000000
        (_, best_move) = minimaxAB(board, -MAX, MAX, 0, True, heura_x, heuristic_random, depth_x)
        board = move(board, best_move)
        display_board(board)
        if is_winning(board, 'x'):
            print("Player 1 wins!")
            break
        # player 2
        a1 = input("Enter a1: ")
        b1 = input("Enter b1: ")
        a2 = input("Enter a2: ")
        b2 = input("Enter b2: ")
        usermove = (int(a1), int(b1), int(a2), int(b2))
        print("Moving... " + str(usermove))
        board = move(board, usermove)
        display_board(board)
        if is_winning(board, 'o'):
            print("Player 2 wins!")
            break

play_game_minimaxAB_vs_user(board, heuristic_adaptive, 2)

# board2 = initialize_board_from_file('board.txt')
# display_board(board2)
# lmoves = legal_moves(board2, 'o')
# for move in lmoves:
#     print(move)

# play each strat aganist each other other 3 times (minimax depth 1, if position is repeated then break) and store the results
# also measure time
def play():
    heuristics = [heuristic_manhattan, heuristic_manhattan_with_center, heuristic_manhattan_with_groupping, heuristic_adaptive]
    results = [["" for _ in range(len(heuristics))] for _ in range(len(heuristics))]
    for i in range(len(heuristics)):
        for j in range(len(heuristics)):
            if i == j:
                continue
            results[i][j] = str(i) + " vs " + str(j) + " "
            start_time = time.time()
            total_time1 = 0
            total_time2 = 0
        
            board = initialize_board()
            positions = []
            move_count = 0
            while(True):
                move_count += 1
                if time.time() - start_time > 600:
                    results[i][j] += 'T'
                    break
                # player 1
                last_time_1 = time.time()
                (_, best_move) = minimax(board, 0, True, heuristics[i], heuristics[j], 1)
                total_time1 += time.time() - last_time_1
                if best_move == None:
                    results[i][j] += 'W'
                    break
                board = move(board, best_move)
                if board in positions:
                    results[i][j] += 'D'
                    break
                positions.append(board)
                if is_winning(board, 'x'):
                    results[i][j] += 'L'
                    break
                # player 2
                last_time_2 = time.time()
                (_, best_move) = minimax(board, 0, False, heuristics[i], heuristics[j], 2)
                total_time2 += time.time() - last_time_2
                if best_move == None:
                    results[i][j] += 'L'
                    break
                board = move(board, best_move)
                if board in positions:
                    results[i][j] += 'D'
                    break
                positions.append(board)
                if is_winning(board, 'o'):
                    results[i][j] += 'W'
                    break
            # add time per move but only two decimal places
            results[i][j] = results[i][j] + " " + str(round(total_time1 / move_count, 2)) + " " + str(round(total_time2 / move_count, 2))
            display_board(board)
            print(results[i][j])

    return results

# results = play()
# for row in results:
#     print('\n')
#     for res in row:
#         print(res)


def playAB():
    heuristics = [heuristic_manhattan, heuristic_manhattan_with_center, heuristic_manhattan_with_groupping, heuristic_adaptive]
    results = [["" for _ in range(len(heuristics))] for _ in range(len(heuristics))]
    for i in range(len(heuristics)):
        for j in range(len(heuristics)):
            if i == j:
                continue
            results[i][j] = str(i) + " vs " + str(j) + " "
            start_time = time.time()
            total_time1 = 0
            total_time2 = 0
        
            board = initialize_board()
            positions = []
            move_count = 0
            while(True):
                move_count += 1
                if time.time() - start_time > 600:
                    results[i][j] += 'T'
                    break
                # player 1
                last_time_1 = time.time()
                (_, best_move) = minimaxAB(board, MIN, MAX, 0, True, heuristics[i], heuristics[j], 2)
                total_time1 += time.time() - last_time_1
                if best_move == None:
                    results[i][j] += 'W'
                    break
                board = move(board, best_move)
                if board in positions:
                    results[i][j] += 'D'
                    break
                positions.append(board)
                if is_winning(board, 'x'):
                    results[i][j] += 'L'
                    break
                # player 2
                last_time_2 = time.time()
                (_, best_move) = minimaxAB(board, MIN, MAX, 0, False, heuristics[j], heuristics[j], 1)
                total_time2 += time.time() - last_time_2
                if best_move == None:
                    results[i][j] += 'L'
                    break
                board = move(board, best_move)
                if board in positions:
                    results[i][j] += 'D'
                    break
                positions.append(board)
                if is_winning(board, 'o'):
                    results[i][j] += 'W'
                    break
            # add time per move but only two decimal places
            results[i][j] = results[i][j] + " " + str(round(total_time1 / move_count, 2)) + " " + str(round(total_time2 / move_count, 2))
            display_board(board)
            print(results[i][j])

    return results

# results = playAB()
# for row in results:
#     print('\n')
#     for res in row:
#         print(res)