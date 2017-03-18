from stack import Stack
import random
import concurrent.futures
#from tkinter import *
#You cannot use tkinter along with threads. It's not threat-safe
 

class Board:
    def __init__(self):         #Default Constructor
        #Initialize Board
        self.N = 5
        self.B = []
        self.Winner = ""
        for x in range(self.N*self.N):
            self.B.append(Stack())
        self.pieces(self.N)

        #Initialize Temp Variable
        self.Flag = False        #False for First Move, True from Second
        self.Buffer = Stack()    #For Movement
        self.Move = True         #True for Player 1, False for Player 2; Change Later
        self.HThreatLength = 0   #Temp Variables for Threat Evaluation
        self.VThreatLength = 0
       

    def pieces(self, N):        #Remaining Pieces
        if(N==5):
            F=21
        if(N==6):
            F=30
        if(N==7):
            F=40
        self.Flats = [F,F]
        self.Caps = [1,1]       #7x7 can have 1 or 2 caps depending on players. I've assumed C=1


    def fromParent(self, parent):       #Copy Constructor
        self.N = parent.N
        self.Winner = parent.Winner
        self.Flag = True        
        self.Buffer = Stack()    
        self.Move = parent.Move
        self.Flats = parent.Flats[:]        ###Problem Resolved by Splicing!
        self.Caps = parent.Caps[:]
        self.copyBoard(parent)
        return self
    

    def copyBoard(self, parent):            ###PROBLEMResolved^!!!!!!!!!!!!!
        self.B = []
        for x in range(self.N*self.N):
            self.B.append(Stack())
            self.B[x].copy(parent.B[x])
    

    def move(self, Player, Str):    
        F = 'F'                 #Caps for White and lower case for black
        S = 'S'                 #A better representation might be +ve for White, -ve for black 
        C = 'C'                 #F = 1, S = 2, C = 3. This should be done as Python string manip is complex
        if(self.Flag):          #From Second Move
            if(Str[0]>='0' and Str[0]<='5'):
                self.movePly(Player, Str)   #Move Ply
            else:
                self.placePly(Player, Str)  #Place Ply
        else:                   #For First Move
            if(int(Player) != 2):
                F='f'
                S='s'
                C='c'
            else:
                self.Flag = True
            T = self.strToNum(Str)
            if(Str[0]>='a' and Str[0]<=chr(ord('a')+self.N)): 
                self.B[T].push(F)
            if(Str[0]=='C'): 
                self.B[T].push(C)
            if(Str[0]=='S'):
                self.B[T].push(S)
        
            
    def placePly(self, Player, Str):
        F = 'F'                 #Caps for White and lower case for black
        S = 'S'
        C = 'C'
        if(int(Player) != 1):
            F='f'
            S='s'
            C='c'
        if(int(Player) == 1):
            if(Str[0]=='C'): 
                self.Caps[0] -= 1
            else:
                self.Flats[0] -= 1
        else:
            if(Str[0]=='C'):
                self.Caps[1] -= 1
            else:
                self.Flats[1] -= 1
        T = self.strToNum(Str)
        if(Str[0]>='a' and Str[0]<=chr(ord('a')+self.N)): ##Changed condition to include any dimension
            self.B[T].push(F)
        if(Str[0]=='C'): 
            self.B[T].push(C)
        if(Str[0]=='S'):
            self.B[T].push(S)
            		
			
    def movePly(self, Player, Str):
        if(Str[0]>='0' and Str[0]<='5'):
            l = len(Str)
            V=0                         #Directions
            H=0
            if(Str[3]=='+'):
                V=-1
            if(Str[3]=='-'):
                V=1
            if(Str[3]=='<'):
                H=-1
            if(Str[3]=='>'):
                H=1
            T = self.strToNum(Str)
            for x in range(int(Str[0])):
                self.Buffer.push(self.B[T].pop())
            for x in range(4,l):
                for y in range(ord(Str[x])-48):             #The Actual Movement
                    Temp = T +(5*V*(x-3)) + H*(x-3)
                    self.B[Temp].push(self.Buffer.pop())


    def strToNum(self,Str):         #For Now Str is in PTN, i.e., Portable Tak Notations only. Other representations are not needed right now
        if(Str[0]>='a' and Str[0]<=chr(ord('a')+self.N)): 
            return (ord(Str[0]) - 97) + 5*(5-int(Str[1]))
        if(Str[0]=='C'): 
            return (ord(Str[1]) - 97) + 5*(5-int(Str[2]))
        if(Str[0]=='S'):
            return (ord(Str[1]) - 97) + 5*(5-int(Str[2]))
        if(Str[0]>='0' and Str[0]<='5'):
            return (ord(Str[1]) - 97) + 5*(5-int(Str[2]))
        return -1


    def numToStr(self,Num):
        if Num < 0 or Num >= self.N*self.N:
            return ''
        col = Num % self.N
        row = int(Num / self.N)
        return chr(col + 97) + str(5-row)


    def getAllMoves(self, Player):      #Call This 
        all_moves = []
        for x in range(self.N*self.N):
            if(self.B[x].isEmpty()):    #Place Plies
                X = self.numToStr(x)
                if(self.Flats[Player-1]>0):
                    all_moves.append(X)
                    all_moves.append('S'+X)
                if(self.Caps[Player-1]>0):
                    all_moves.append('C'+X)
            else:
                if(Player==1 and self.B[x].peek().isupper()):
                    all_moves += (self.__getStackMoves(x,Player))
                if(Player!=1 and not self.B[x].peek().isupper()):
                    all_moves += (self.__getStackMoves(x,Player))
        if all_moves == []:
            pass
        return all_moves


    def __getStackMoves(self, sq, Player):    #Move Plies
        all_moves = []
        r = sq / self.N
        c = sq % self.N
        size = self.B[sq].size()
        dirs = ['+', '-', '<', '>']
        up = r
        down = self.N - 1 - r
        right = self.N - 1 - c
        left = c
        rem_squares = [up, down, left, right]
        for x in range(min(size,self.N)):
            part_list = self.__partition(x + 1)
            for di in range(4):
                part_dir = [part for part in part_list if len(part) <= rem_squares[di]] 
                for part in part_dir:
                    if self.__check_valid(sq, dirs[di], part) == True:
                        part_string = ''.join([str(i) for i in part])
                        all_moves.append(str(sum(part)) + self.numToStr(sq) + dirs[di] + part_string)
        return all_moves


    def __partition(self, n):         #All possible permutations using recursion
        part_list = []
        part_list.append([n])
        for x in range(1, n):
            for y in self.__partition(n - x):
                part_list.append([x] + y)
        return part_list


    #TODO: Flattening Stones Rule
    def __check_valid(self, square, direction, partition):    #Crosschecks partitions against rules
        if direction == '+':
            change = -self.N
        elif direction == '-':
            change = +self.N
        elif direction == '>':
            change = 1
        elif direction == '<':
            change = -1
        for i in range(len(partition)):
            next_square = square + change * (i + 1)
            if self.B[next_square].size() > 0:
                pass
            if self.B[next_square].size() > 0 and (self.B[next_square].peek() == 'C' or self.B[next_square].peek() == 'c'):
                return False
            if self.B[next_square].size() > 0 and (self.B[next_square].peek() == 'S' or self.B[next_square].peek() == 's'):
                return False
        return True


    #TODO: Flat Victory
    def checkVictory(self):                 #Two Types of Victories
        if self.__checkRoadVictory(1):              #Road Victory
            return 1
        elif self.__checkRoadVictory(2):
            return -1
        #elif self.__checkFlatVictory(1):           #Flat Victory
        return 0                                    #No Victory


    def __getNeighbour(self, pos):                        #Sorry for the Ambiguity between N(Neighbour) and self.N(Board Size)
        N = []
        if pos<0 or pos>=(self.N*self.N):                   #Outside
            return N
        elif pos==0:                                        #Top Left Corner
            N = [pos+1, pos+self.N]
        elif pos == self.N-1:                               #Top Right Corner
            N = [pos-1, pos+self.N]
        elif pos == self.N*(self.N-1):                      #Bottom Left Corner
            N = [pos+1, pos-self.N]
        elif pos == self.N*self.N -1:                       #Bottom Right Corner
            N = [pos-1, pos-self.N]
        elif pos < self.N:                                  #Top Edge
            N = [pos-1, pos+1, pos+self.N]
        elif pos%self.N == 0:                               #Left Edge
            N = [pos+1, pos+self.N, pos-self.N]
        elif ((pos+1)%self.N) == 0:                         #Right Edge
            N = [pos-1, pos+self.N, pos-self.N]
        elif pos >= self.N*(self.N-1):                      #Bottom Edge
            N = [pos-1, pos+1, pos-self.N]
        else:                                               #Inside
            N = [pos-1, pos+1, pos+self.N, pos-self.N]
        return N


    def __checkRoadVictory(self, Player):
        return self.__checkVRoad(Player) or self.__checkHRoad(Player)
    

    def __checkVRoad(self, Player):
        DFSStack = Stack()
        Visited = set()
        Win = False
        F = 'F'                 #Capital for White and lower case for black
        C = 'C'
        self.VThreatLenght = 0
        if(int(Player) != 1):
            F='f'
            C='c'
        for x in range(self.N): #Vertical Roads
            X = ''
            if not self.B[x].isEmpty():
                X = self.B[x].peek()
            if(X==F or X==C):
                DFSStack.push(x)
                Visited.add(x)
        while(not DFSStack.isEmpty()):
            Neighbour = self.__getNeighbour(DFSStack.peek())
            NAdd = 0
            for N in Neighbour:           #Sorry for the Ambiguity between N(Neighbour) and self.N(Board Size)
                X = ''
                if not self.B[N].isEmpty():
                    X = self.B[N].peek()
                if not N in Visited:
                    if(X==F or X==C):
                        DFSStack.push(N)
                        if DFSStack.size() > self.VThreatLength:
                            self.VThreatLength = DFSStack.size()
                        Visited.add(N)
                        if N >= self.N*(self.N-1):
                            Win = True
                            return Win
                        NAdd = 1
            if NAdd == 0 and not DFSStack.isEmpty():
                    Temp = DFSStack.pop()
        return Win


    def __checkHRoad(self, Player):
        DFSStack = Stack()
        Visited = set()
        Win = False
        F = 'F'                 #Capital for White and lower case for black
        C = 'C'
        HThreatLength = 0
        if(int(Player) != 1):
            F='f'
            C='c'
        for x in range(self.N): #Horizontal Roads
            X = ''
            if not self.B[x*self.N].isEmpty():
                X = self.B[x*self.N].peek()
            if(X==F or X==C):
                DFSStack.push(x*self.N)
                Visited.add(x)
        while(not DFSStack.isEmpty()):
            Neighbour = self.__getNeighbour(DFSStack.peek())
            NAdd = 0
            for N in Neighbour:
                X = ''
                if not self.B[N].isEmpty():
                    X = self.B[N].peek()
                if not N in Visited:
                    if(X==F or X==C):
                        DFSStack.push(N)
                        if DFSStack.size() > self.HThreatLength:
                            self.HThreatLength = DFSStack.size()
                        Visited.add(N)
                        NAdd += 1
                        if (N+1)%self.N == 0:
                            Win = True
                            return Win
            if NAdd == 0 and not DFSStack.isEmpty():
                Temp = DFSStack.pop()
        return Win
        

    #TODO: Threat Score
    def evaluate(self, Player):     
        Score = self.checkVictory() * 100000
        P=1
        if Score == 0:
            F = 'F'                 #Caps for White and lower case for black
            S = 'S'
            C = 'C'
            P = 1
            if(int(Player) != 1):
                F='f'
                S='s'
                C='c'
                P = -1
            Flat = 35
            Cap = 30
            Wall = 10
            SelfCaptive = 25
            NSelfCaptive = 15
            
            for x in range(self.N*self.N):
                factor = 10 * P
                if(x%self.N==0 or (x+1)%self.N==0 or x<self.N or x>=self.N*(self.N-1)):     #Edges Will have less influence
                    factor = 7 * P
                if not self.B[x].isEmpty():
                    size = self.B[x].size()
                    T = self.B[x].ps(size)
                    if T[size-1]==F:
                        Score += Flat * factor
                        for t in T:                 #This is also considering the topmost piece. Will have to see how it affects the performance later
                            if t==F:
                                Score += SelfCaptive * factor
                            else:
                                Score += NSelfCaptive * factor
                    if T[size-1]==C:
                        Score += Cap * factor
                        for t in T:                 
                            if t==F:
                                Score += SelfCaptive * factor
                            else:
                                Score += NSelfCaptive * factor
                    if T[size-1]==S:
                        Score += Wall * factor
                        for t in T:                 
                            if t==F:
                                Score += SelfCaptive * factor
                            else:
                                Score += NSelfCaptive * factor
        ThreatLength = self.VThreatLength
        if ThreatLength < self.HThreatLength:
            ThreatLength = self.HThreatLength
        return Score + ThreatLength*300*P
                        

    def playMM(self,Player):    #Optimize by using Recursion?
        P = 1
        if Player == 2:
            P = - 1
        currBoard = Board()
        currBoard = currBoard.fromParent(self)
        moves_0 = (self.getAllMoves(Player))
        BestMove = []
        BestScore = 0           
        for m0 in moves_0:              #Depth 1
            flag_reject = False
            currB_1 = Board()
            currB_1 = currB_1.fromParent(currBoard)
            currB_1.move(Player, m0)
            moves_1 = currB_1.getAllMoves(Player+P)
            T1 = 0
            temp = currB_1.evaluate(Player) * P
            if temp >= 100000:
                BestScore = temp
                BestMove = []
                BestMove.append(m0)
                break
            for m1 in moves_1:          #Depth 2
                currB_2 = Board()
                currB_2 = currB_2.fromParent(currB_1)
                currB_2.move(Player+P, m1)
                moves_2 = currB_2.getAllMoves(Player)
                #print(moves_2)
                T2 = 0
                temp2 = currB_2.evaluate(Player+P)  * P
                if temp2 <= -90000:
                    #print(m0)
                    #print(m1)
                    flag_reject = True
                    break
                for m2 in moves_2:      #Depth 3
                    currB_3 = Board()
                    currB_3 = currB_3.fromParent(currB_2)
                    currB_3.move(Player, m2)
                    moves_3 = currB_3.getAllMoves(Player+P)
                    #print(moves_3)
                    T3 = 0
                    temp3 = currB_3.evaluate(Player)* P
                    #print(temp3)
                    if temp3 >= 100000:
                        T2 = temp3*3
                        if not flag_reject:
                            BestMove = []
                            BestMove.append(m0)
                        break
                    if temp3 < temp:
                        continue
                    #4 or more depth is too slow without optimization
                    if T2 < temp3*3+T3:
                        T2 = temp3*3  + T3
                if T1 < temp2*4+T2:
                    T1 = temp2*4  + T2
            if BestScore < temp*5+T1 and not flag_reject:
                BestScore = (temp*5  + T1)
                #print(BestScore)
                BestMove = []
                BestMove.append(m0)
            elif BestScore == temp*5+T1 and not flag_reject:
                BestMove.append(m0)
                
        
        if(BestMove==[]):
            self.play(1,Player)
        BM = BestMove[random.randint(0, len(BestMove)-1)]
        print(BM)
        self.move(Player, BM)
        self.render_gui.render(self)
        #return BestMove
        

    def playMM2(self, Player):      #Reduces Time by half. But is still 1 min wait time.
        currBoard = Board()
        currBoard = currBoard.fromParent(self)
        moves_0 = (self.getAllMoves(Player))
        futures = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            for m0 in moves_0:
                fut = pool.submit(playM2, Player, currBoard, m0)        #This was a lot of headache
                futures.append(fut.result())
        BestScore=0
        P=1
        Moves = []
        if Player!=1:
            P=-1
        for score, move in futures:
            if BestScore < score*P:
                Moves = []
                Moves.append(move)
                BestScore = score*P
            elif BestScore == score*P:
                Moves.append(move)

        if(Moves==[]):
            print("ERROR!!!")
            self.play(1,Player)
        BM = Moves[random.randint(0, len(Moves)-1)]
        print(BM,end=' ')
        self.move(Player, BM)
        #print(futures)  

    
    def play(self, diff, Player):
        if(not self.Flag):
            if(Player==1):
                self.move(Player,'a5')
                print('a5',end=' ')
                return
            else:
                if(self.B[0].isEmpty()):        #Hardcoded as there is no need for a complex code here. We need to put opponent in corners.
                    self.move(Player,'a5')
                    print('a5',end=' ')
                else:                           #Since it is the First Move, One of these two squares is bound to be empty
                    self.move(Player,chr(self.N-1 + 97) + str(1)) #e1 for 5x5 and so on
                    print(chr(self.N-1 + 97) + str(1),end=' ')
                return
        if diff == 1:
            self.playRandom(Player)
        elif diff == 2:
            self.playMM(Player)
        elif diff == 3:
            self.playMM2(Player)
        elif diff == 4:
            Move, Score = self.alphaBeta(Player, True, -100000, 100000, 0, 3)
            self.move(Player, Move)
            print(Move,end=' ')


    def playRandom(self,Player):
        all_moves = []
        all_moves = self.getAllMoves(Player)
        move = all_moves[random.randint(0, len(all_moves)-1)]
        print(move)
        self.move(Player, move)


    def alphaBeta(self, Player, maxNode, alpha, beta, depth, CurD):
        BestMove = ''
        P = 1
        if Player != 1:
            P = -1
        if depth == CurD:
            best = self.evaluate(Player)
            #print("Test1")
            return BestMove, best;
        CB = Board()
        CB = CB.fromParent(self)
        ValMov = CB.getAllMoves(Player)
        #print(ValMov)
        if maxNode:
            V = -100000
            for m in ValMov:
                CB2 = Board()
                CB2 = CB2.fromParent(CB)
                #print(CB2.getAllMoves(Player))
                #print(CB2.B[1].ps(CB2.B[1].size()))
                CB2.move(Player,m)
                
                X, value = CB2.alphaBeta(Player+P, False, alpha, beta, depth+1, CurD)

                if value >= 90000:
                    BestMove = m
                    V = value
                if V < value:
                    BestMove = m
                    V = value
                alpha = max(alpha, V)
                if(beta<=alpha):
                    #print("Beta < Alpha")
                    break
            return BestMove, V
        else:
            V = 100000
            for m in ValMov:
                CB2 = Board()
                CB2 = CB2.fromParent(CB)
                CB2.move(Player, m)
                X, value = CB2.alphaBeta(Player+P, True, alpha, beta,depth+1, CurD)
                if value <= -90000:
                    BestMove = m
                    V = value
                if V > value:
                    BestMove = m
                    V = value
                beta = min(beta, V)
                if(beta <= alpha):
                    #print("Beta < Alpha!")
                    break
            return BestMove, V
                    

        


def playM2(Player, currBoard, m):       #Couldn't do multithreading with Method inside class. #StillANovice
    
    P=1
    if Player!=1:
        P=-1
    CB1 = Board()
    CB1 = CB1.fromParent(currBoard)
    CB1.move(Player, m)
    T1 = CB1.evaluate(Player)
    if T1*P >= 90000:
        return 100000, m
    T2=0
    T3=0
    moves_1 = CB1.getAllMoves(Player+P)
    for m1 in moves_1:
        CB2 = Board()
        CB2 = CB2.fromParent(CB1)
        CB2.move(Player+P, m1)
        T2 = CB2.evaluate(Player+P)
        if T2*P <= -90000:
            #print(m,end=' ')
            #print(m1)
            return 0, m
        moves_2 = CB2.getAllMoves(Player)
        for m2 in moves_2:
            CB3 = Board()
            CB3 = CB3.fromParent(CB2)
            CB3.move(Player, m2)
            T3 = CB3.evaluate(Player)
            if T3*P >= 90000:
                return 100000, m
    T = T1*5 + T2*4 + T3*3
    #print('y')
    return T, m



    
