import random
class Heuristic():

    def __init__(self, my_chara, oppo_chara):
        self.ME = my_chara
        self.OPPO = oppo_chara
        self.D = False
        self.W1 = 10000
        self.W2 = 1000
        self.W3 = 100
        self.W4 = 10
        self.W5 = 1
        self.W6 = 0

    def setParameter(self, w1,w2,w3,w4,w5,w6):
        self.W1 = w1
        self.W2 = w2
        self.W3 = w3
        self.W4 = w4
        self.W5 = w5
        self.W6 = w6

    def choiceByHeuristic(self, board, possible_columns):
        # calculate heuristic value for all possible columns.
        # and choice best move.
        col_num = len(possible_columns)
        heuristic_moves = []
        critical_moves = []
        best_height = 100
        best_heuristic_val = -1


        for i in range(col_num):
            col = possible_columns[i]
            row = board.position[col]

            # check winning line to calculate heuristic score.
            klm,kclm,kcn,kot,ket,kill_height,flg_win \
                    = self.checkWinningLine(board, self.OPPO, row, col)
            clm,cclm,ccn,cot,cet,create_height, flg_lose \
                    = self.checkWinningLine(board, self.ME, row, col)

            temp_val = self.calcHeuristicValue(klm,kclm,kcn,kot,ket,clm,cclm,ccn,cot,cet)
            temp_height = min(create_height, kill_height)
            if self.D:print 'column:'+str(col)+' - '+str(temp_val)+'( height='+str(temp_height)+' )'
            # if you put a move here then you win.(or otherwise you will lose in next turn)
            if flg_win or flg_lose: return [col]
            '''
            if temp_height < best_height:
                critical_moves = [(temp_val,col)]
                best_height = temp_height
            elif temp_height == best_height and temp_height != 100:
                critical_moves.append((temp_val,col))
            '''
            if temp_val > best_heuristic_val:
                heuristic_moves = [col]
                best_heuristic_val = temp_val
            elif temp_val == best_heuristic_val:
                heuristic_moves.append(col)

        if self.D : print 'critical move (row='+str(best_height)+'):'+str(critical_moves)
        if len(critical_moves) != 0:
            best_critical = max(critical_moves)
            return [best_critical[1]]
        return heuristic_moves

    def choiceByStrongHeuristic(self, board, possible_columns):
        # calculate heuristic value for all possible columns.
        # and choice best move.
        col_num = len(possible_columns)
        heuristic_moves = []
        critical_moves = []
        best_height = 100
        scores = [0 for i in range(col_num)] # tuple of (critical_height, heuristic_score, column)
        best_heuristic_val = -3

        for i in range(col_num):
            col = possible_columns[i]
            row = board.position[col]


            # check winning line to calculate heuristic score.
            klm,kclm,kcn,kot,ket,kill_height,flg_win \
                    = self.checkWinningLine(board, self.OPPO, row, col)
            clm,cclm,ccn,cot,cet,create_height, flg_lose \
                    = self.checkWinningLine(board, self.ME, row, col)

            temp_val = self.calcHeuristicValue(klm,kclm,kcn,kot,ket,clm,cclm,ccn,cot,cet)
            temp_height = min(create_height, kill_height)
            scores[i] = (temp_height, -temp_val, col)
            if self.D:print 'column:'+str(col)+' - '+str(temp_val)+'( height='+str(temp_height)+' )'

            # if you put a move here then you win.(or otherwise you will lose in next turn)
            if flg_win or flg_lose: 
                if self.D: print 'you must put here.'
                return [col]

            # check if this move's above square is opponent threat,
            # if so, avoid this move as possible as I can.
            if row+1!=board.HEIGHT and board.checkIfWin(self.OPPO, row+1, col):
                if self.D:print 'lose if put a move on square('+str(row)+','+str(col)+')'
                if best_heuristic_val <= -2:
                    best_heuristic_val = -2
                    scores[i] = (100, 50, col)
                    heuristic_moves.append(col)
                continue
            if row+1!=board.HEIGHT and board.checkIfWin(self.ME, row+1, col):
                if self.D:print 'lose my threat if put a move on square('+str(row)+','+str(col)+')'
                scores[i] = (100, 100, col)
                if best_heuristic_val < -1:
                    heuristic_moves = [col]
                elif best_heuristic_val == -1:
                    heuristic_moves.append(col)
                best_heuristic_val = -1
                continue

            if temp_height < best_height:
                critical_moves = [(temp_val,col)]
                best_height = temp_height
            elif temp_height == best_height and temp_height != 100:
                critical_moves.append((temp_val,col))

            if temp_val > best_heuristic_val:
                heuristic_moves = [col]
                best_heuristic_val = temp_val
            elif temp_val == best_heuristic_val:
                heuristic_moves.append(col)

        # search STMH solver(moves which create/kill STMH).
        # if found then choose best move from STMH solver by heuristic function.
        STMHsolver = self.solveSTMH(board)
        if STMHsolver!=-1:
            # first priority is height, and second is heuristic score.
            # To sort in this priority order we negated heuristic score above.
            if self.D: print 'solved STMH !!!'
            scores.sort()
            for h,v,col in scores:
                if col in STMHsolver: return [col]

        # if critical moves found then return them,
        # else return moves which get high heuristic score.
        if self.D : print 'critical move (row='+str(best_height)+'):'+str(critical_moves)
        if len(critical_moves) != 0:
            best_critical = max(critical_moves)
            return [best_critical[1]]
        return heuristic_moves

    '''
    if find STMH(Succesive Three Moves in Horizontal) then return columns of moves
    which create or solve this STMH.
    (if found my STMH then create, otherwise kill it)
    if not found then return -1 as flag.
    EX.)
        [move 'X' on column 2 or 5 solve STMH and 'O' on 5 create STMH]
                    - - - - -     - - - - -
                    - - O O -  => - O O O -
                    1 2 3 4 5     1 2 3 4 5
        [move 'X' on column 1,3,5 solve STMH and 'O' on 3 create STMH]
                    - - - - -     - - - - -
                    - O - O -  => - O O O -
                    1 2 3 4 5     1 2 3 4 5
    '''
    def solveSTMH(self, board):
        p = board.position
        ans = -1

        for i in range(board.WIDTH-5+1):
            # STMH test 1 (check if 5 horizontal square contain 3 brank square which is available.)
            h = p[i]
            if h==board.HEIGHT: continue
            tb = board.table[h]
            if tb[i] == tb[i+4] == 0 and p[i] == p[i+4]:
                brank_num = 0
                for j in range(1,4):
                    if tb[i+j] == '-':
                        if p[i+j] == h:
                            brank_num += 1
                        else:
                            brank_num = 2
                            break
                if brank_num != 1:
                    continue
            else:
                continue
            # STMH test 2 (check if it's STMH in detail)
            temp = 0
            # find pattern 1
            if tb[i+2] != 0:
                player = tb[i+2]
                if tb[i+1]==tb[i+2]:
                    if player == self.ME: temp=[i+3]
                    else: temp=[i,i+3,i+4]
                elif tb[i+2] == tb[i+3]:
                    if player == self.ME: temp=[i+1]
                    else: temp=[i,i+1,i+4]
            # find pattern 2
            elif p[i+2] == 0 and p[i+1] != 0 and p[i+1] == p[i+3]:
                player = p[i+1]
                if player == self.ME: temp=[p[i+2]]
                else: temp=[p[i],p[i+2],p[i+4]]

            if temp!=0: # find STMH !!
                if ans == -1:
                    ans = temp
                else:
                    # take intersection of two list(ans & temp)
                    # temp = set(temp)
                    # ans = set(ans)
                    # ans = list(temp.intersection(ans))
                    ans = [col for col in ans if col in temp]
        # if STMH not found
        return ans

    def calcHeuristicValue(self, klm,kclm,kcn,kot,ket,clm,cclm,ccn,cot,cet):
        # calculate heuristic value for the given move and return heuristic value.
        # parameters are, 
        # 1. the number of critical loosing line which this move kills.
        # 2. the number of loosing line which this move kills.
        # 3. the number of winning line which this move creates.
        # 4. the max number of opponent moves in loosing line which this move kills.
        killed_line_num = klm
        killed_critical_line_num = kclm
        kill_component_num = kcn
        killed_odd_threat_num = kot
        killed_even_threat_num = ket
        create_line_num = clm
        create_critical_line_num = cclm
        create_component_num = ccn
        create_odd_threat_num = cot
        create_even_threat_num = cet

        # assume that odd threat is good for first-move player('O'),
        # and even threat is good for second-move player('X')
        killed_critical_line_num = killed_even_threat_num if self.ME == 1 else killed_odd_threat_num
        create_critical_line_num = create_odd_threat_num if self.ME == 1 else create_even_threat_num

        return killed_critical_line_num*self.W1+\
                killed_line_num*self.W2+\
                create_critical_line_num*self.W3+\
                create_line_num*self.W4 +\
                kill_component_num*self.W5 +\
                create_component_num*self.W6

    '''
    count the number of winning line this move make.
    if you want to count the number of losing line,
    then pass your opponent character in player variable.
    '''
    def checkWinningLine(self, board, player, row, col):
        # line_upper_right, line_horizontal, line_lower_right, line_bottom = 1,1,1,1
        line_nums = [1,1,1,1]
        line_component_nums = [1,1,1,1]
        threat_even_odd = [0,0,0,0] # flg-> 0:none, 1:odd, 2:even, 3:both
        di = [1,-1,0,0,-1,1,-1]
        dj = [1,-1,1,-1,1,-1,0]

        winning_line_num = 0
        winning_critical_line_num = 0
        best_component_num = 0
        odd_threat_num, even_threat_num = 0, 0
        is_successive = True
        is_finish_move = False
        # holds the row & column pair of critical threat
        critical_best_height = 100
        temp_height = -1
        opponent = self.OPPO if player==self.ME else self.ME

        for d in range(7):
            ni, nj = row, col
            is_successive = True
            for k in range(board.CONNECT_K-1):
                ni += di[d]
                nj += dj[d]
                # if opponent is already interrupting this winning line
                if not(0<=ni<board.HEIGHT) or not(0<=nj<board.WIDTH) or board.table[ni][nj] == opponent:
                    break
                # if this winning line already has my pieces,
                # then you should fill this winning line.
                if is_successive and board.table[ni][nj] == player:
                    line_component_nums[d/2] += 1
                else:
                    is_successive = False
                # if the square below the threat is not empty, then we do not count this winning line.
                # because opponent can immediately interrupt this threat.
                if ni==0 or (board.table[ni][nj] == 0 and board.table[ni-1][nj] != 0):
                    continue
                # if this square is threat, then check its even-odd and remember it.
                if board.table[ni][nj] == 0:
                    temp_height = max(temp_height, ni)
                    if ni%2==0: #this threat is odd-threat
                        threat_even_odd[d/2] |= 1
                    else: # this threat is even-threat
                        threat_even_odd[d/2] |= 2
                line_nums[d/2] += 1
            if d%2==1 or d==6:
                if line_component_nums[d/2] >= board.CONNECT_K:
                    #print 'final move'
                    #raw_input()
                    is_finish_move = True
                if line_nums[d/2] >= board.CONNECT_K:
                    winning_line_num += 1
                    best_component_num = max(best_component_num, line_component_nums[d/2])
                    if threat_even_odd[d/2] == 1:
                        odd_threat_num += 1
                    elif threat_even_odd[d/2] == 2:
                        even_threat_num += 1
                    if (player == 1 and threat_even_odd[d/2] == 1) or\
                             (player == 2 and threat_even_odd[d/2] == 2):
                        critical_best_height = min(critical_best_height, temp_height)
                temp_height = -1

        return winning_line_num, winning_critical_line_num,\
                best_component_num, odd_threat_num, even_threat_num, critical_best_height, False#TODOis_finish_move
