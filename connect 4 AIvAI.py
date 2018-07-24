import time
from random import randrange as rr
start = time.time() #times cpu moves
board = [[0]*6]*7 #initial board state
###### colors: red, p1, 1 ; yellow, p2, 2

def move(board_init,i,c): #function to calculate board state after color [c] is droped in column [i]
    board = [[j for j in i] for i in board_init]
    try:
        board[i][board[i].index(0)] = c
    except:
        for j in range(7):
            try:
                 board[j][board[j].index(0)] = c
                 return board
            except:
                0
    return board #returns new board state, and whether a free turn is generated

def won(board): #tells whether the current board state is a completed game
    winners = {1:False, 2:False}
    for i in range(7):#vertical
        for j in range(3):
            if board[i][j] != 0 and all(board[i][j + k] == board[i][j + k + 1] for k in range(3)):
                winners[board[i][j]] = True
    for i in range(4):#horizonal
        for j in range(6):
            if board[i][j] != 0 and all(board[i + k][j] == board[i + k + 1][j] for k in range(3)):
                winners[board[i][j]] = True
    for i in range(4):#diagonal
        for j in range(3):
            if board[i][j] != 0 and all(board[i + k][j + k] == board[i + k + 1][j + k + 1] for k in range(3)):
                return board[i][j]
            if board[i][j + 3] != 0 and all(board[i + k][j + 3 - k] == board[i + k + 1][j + 2 - k] for k in range(3)):
                winners[board[i][j + 3]] = True
    return winners[1]*1 + winners[2]*2

def threes(board): #tells whether the current board state is a completed game
    amount = {1:0, 2:0}
    for i in range(7):#vertical
        for j in range(4):
            if board[i][j] != 0 and all(board[i][j + k] == board[i][j + k + 1] for k in range(2)):
                amount[board[i][j]] += 1
    for i in range(5):#horizonal
        for j in range(6):
            if board[i][j] != 0 and all(board[i + k][j] == board[i + k + 1][j] for k in range(2)):
                amount[board[i][j]] += 1
    for i in range(5):#diagonal
        for j in range(4):
            if board[i][j] != 0 and all(board[i + k][j + k] == board[i + k + 1][j + k + 1] for k in range(2)):
                amount[board[i][j]] += 1
            if board[i][j + 2] != 0 and all(board[i + k][j + 2 - k] == board[i + k + 1][j + 1 - k] for k in range(2)):
                amount[board[i][j + 2]] += 1
    return amount

def twos(board): #tells whether the current board state is a completed game
    amount = {1:0, 2:0}
    for i in range(7):#vertical
        for j in range(5):
            if board[i][j] != 0 and board[i][j] == board[i][j + 1]:
                amount[board[i][j]] += 1
    for i in range(6):#horizonal
        for j in range(6):
            if board[i][j] != 0 and board[i][j] == board[i + 1][j]:
                amount[board[i][j]] += 1
    for i in range(6):#diagonal
        for j in range(5):
            if board[i][j] != 0 and board[i][j] == board[i + 1][j + 1]:
                amount[board[i][j]] += 1
            if board[i][j + 1] != 0 and board[i][j + 1] == board[i + 1][j]:
                amount[board[i][j + 1]] += 1
    return amount

def new(board,side,override): #finds all possible states of board [board] after one turn for player [side] (0:cpu, 1:human).  [override] keeps track of the move sequence made.
    r = []
    if won(board):
        return [[board, -1]]
    for i in range(7):
        if 0 in board[i]:
            j = move(board,i,side)
            r += [[j,override + [i]]]
    return r #returns a list with the new boards, and their corresponding move sequences

def score(board,won_by,side): #calculates the approximate "goodness" of a board state - used for the minimax algorithm
    mult = 15
    if not won_by:
        won_by = won(board)
    if won_by: #if game is completed return highly extreme value
        return (120*(won_by == side) - 100*(won_by == 3 - side))*(won_by != 3)
    _3 = threes(board)
    _2 = twos(board)
    return (-(mult*(_3[1] - _3[2]) + (_2[1] - _2[2])))*({1:-1,2:1}[side]) #returns integer

def main(board_,side,depth,current,steps,won_by,side_init): #this function calls itself recursively to generate a list of all possible board scores and the moves taken to get them after [depth] turns
    r = []
    if depth == current:
        r += [steps]
    else:
        for i in new(board_,side,[]):
            won_by = won(i[0])
            if current + 1 == depth:
                r += main(i[0],3 - side,depth,current + 1,steps + [i[1],score(i[0],won_by,side_init)],won_by,side_init)
            else:
                r += main(i[0],3 - side,depth,current + 1,steps + [i[1]],won_by,side_init)
#            if won(board_):#########maybe minimal A/B pruning
#                break
    return r #returns the list used by minimax

'''the maximin and minimax functions - which I refer to collectively as minimax - are used to implement a minimax algorithm to estimate what the best move to take this turn is, assuming that the human always picks the best move'''
def maximin(q,depth):#chosen
    r = []
    try:
        t = q[0]
    except:
        valid = []
        for i in range(7):
            if 0 in board[i]:
                valid += [i]
#        valid = [i if 0 in board[i] for i in range(7)]
        t = [[valid[rr(len(valid))]]]
    c = 1
    for i in range(len(q)):
        if q[i][:depth] != t[:depth]:
            r += [t]
            t = q[i]
        if q[i][-1] > t[-1]:
            t = q[i]  
            c = 1
        elif q[i][-1] == t[-1]:
            c += 1
            if rr(c) == 0:
                t = q[i]
    return r + [t]#returns list containing ideal (supposedly) move sequence

def minimax(q,depth):#unknown
    r = []
    try:
        t = q[0]
    except:
        valid = []
        for i in range(7):
            if 0 in board[i]:
                valid += [i]
        t = [[valid[rr(len(valid))]]]
    c = 1
    for i in range(len(q)):
        if q[i][:depth] != t[:depth]:
            r += [t]
            t = q[i]
        if q[i][-1] < t[-1]:
            t = q[i]
            c = 1
        elif q[i][-1] == t[-1]:
            c += 1
            if rr(c) == 0:
                t = q[i]
    return r + [t]#returns list containing ideal (supposedly) move sequence
'''
def do_move(board,i): #applies the move generated by minimax to current board state
    r = [j for j in board]
    s = []
    while i:
        s = [i%100] + s
        i //= 100
    for i in s:
        r = move(r,i)[0]
    return r #returns board state and boolean for whether or a free turn was generated
'''
def get_f(iq): #generates a string to allow easier dynamic difficulty
    s = ""
    for i in range(iq):
        s += ["maximin(","minimax("][i%2]
    s += "j"
    for i in range(iq, 0, -1):
        s += "," + str(i - 1) + ")"
    return s #returns string that can have the eval() builtin applied to it

'''lines 129-153 are used to generate a human readable version of the board and move sequence'''

def human_readable(board): #makes human readable board
    s = "\n".join(" ".join("-OX"[board[j][5 - i]] for j in range(7)) for i in range(6)) + "\n" + "="*13 + "\n1 2 3 4 5 6 7"
    return s #returns string

'''
z = "0"
while not int(z) in range(1,8):
    z = input("Enter CPU1 difficulty from 1 to 7: ")
    try:
        int(z)
    except:
        z = "0"
iq1 = int(z)
z = "0"
while not int(z) in range(1,8):
    z = input("Enter CPU2 difficulty from 1 to 7: ")
    try:
        int(z)
    except:
        z = "0"
iq2 = int(z)
'''
def new_instance():
    z = "0"
    while not int(z) in range(1,8):
        z = input("Enter CPU1 difficulty from 1 to 7: ")
        try:
            int(z)
        except:
            z = "0"
    iq1 = int(z)
    z = "0"
    while not int(z) in range(1,8):
        z = input("Enter CPU2 difficulty from 1 to 7: ")
        try:
            int(z)
        except:
            z = "0"
    iq2 = int(z)
    print(("DRAW","CPU1 won!","CPU2 won!","DRAW")[3 - new_game(iq1,iq2,True)])
    print("[difficulty {} vs {}]".format(iq1,iq2) + "\n"*5)


#print(["HUMAN plays first","CPU plays first"][cpu_go])
def new_game(iq1,iq2,print_):
    start = time.time()
    board = [[0]*6]*7 #initial board state
    while not won(board):#continues gameplay until complete
        t1 = time.time()#times cpu turn
        j = main(board, 2, iq1, 0, [],0,2)
        m = eval(get_f(iq1))#finds 'ideal' move
        j = []#reduce ram usage
        board = move(board,m[0][0][0],2)
        if print_: print("\nComputer move (" + str(time.time() - t1)[:5] + "s) : " + str(m[0][0][0] + 1) + "\n" + human_readable(board))
        if not any(0 in j for j in board):
            break
        if won(board):
            break
        t1 = time.time()#times cpu turn
        j = main(board, 1, iq2, 0, [],0,1)
        m = eval(get_f(iq2))#finds 'ideal' move
        j = []#reduce ram usage
        board = move(board,m[0][0][0],1)
        if print_: print("\nComputer move (" + str(time.time() - t1)[:5] + "s) : " + str(m[0][0][0] + 1) + "\n" + human_readable(board))
        if not any(0 in j for j in board):
            break
        if won(board):
            break
    print(str(time.time() - start)[:6] + " seconds elapsed.")
    return won(board)

for i in range(0):
    print(("DRAW","CPU1 won!","CPU2 won!","DRAW")[3 - new_game(2,2,True)])
    print("[difficulty {} vs {}]".format(2,2) + "\n"*5)


#wins = {0:0,1:0,2:0,3:0}
#for _ in range(100):
#    while True:
#        try:
#            wins[new_game(iq1,iq2,False)] += 1
#            break
#        except:
#            0
#    if _%10 == 9:
#        print(_//10 + 1)
#print("{} - CPU1, Diff. {}".format(str(wins[2]).zfill(2),iq2))
#print("{} - CPU2, Diff. {}".format(str(wins[1]).zfill(2),iq1))
#print("{} - DRAWS".format(wins[0]))
#print(str(time.time() - start)[:6] + "secs.")

#print(("DRAW","CPU1 won!","CPU2 won!","DRAW")[new_game(iq1,iq2,True)])
#print("[difficulty {} vs {}]".format(iq1,iq2))

'''    cpu_go = 1#randomize first player
    print(human_readable(board))
    if won(board):#checks completion
        break
    prompt = "column#: "
    z = "0"
    while not int(z) in range(1,8) or not (0 in board[int(z) - 1]): #gets valid player move
        z = input(prompt)
        try:
            int(z)
            if int(z) in range(1,8):
                if not (0 in board[int(z) - 1]):
                    prompt = "pick column that has space left: "
        except:
            z = "0"
            prompt = "Integer column# from 1 to 7: "
    z = int(z) - 1
    print("\n")
    board = move(board,z,1)
    print(human_readable(board))
    if won(board): #checks completion
        break
    if not any(0 in j for j in board):
        break'''
#if won(board) == 1:
#    print("CPU1 won!")
#elif won(board) == 2:
#    print("CPU2 won!")
#else:
#    print("no winner")
#print("[difficulty {} vs {}]".format(iq1,iq2))
while True:
    new_instance()
input("hit [enter] to finish")#if played by double clicking, won't close immediately after completion
