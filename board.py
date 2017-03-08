from stack import Stack
import random

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


    def pieces(self, N):        #Remaining Pieces
        if(N==5):
            F=21
        if(N==6):
            F=20
        if(N==7):
            F=40
        self.Flats = [F,F]
        self.Caps = [1,1]       #7x7 can have 1 or 2 caps depending on players. I've assumed C=1


    def fromParent(self, parent):       #Copy Constructor
        self.N = parent.N
        self.B = parent.B
        self.Winner = parent.Winner
        self.Flag = True        
        self.Buffer = Stack()    
        self.Move = parent.Move
        self.Flats = parent.Flats
        self.Caps = parent.Caps
        return self
    

    def move(self, Player, Str):
        F = 'F'                 #Caps for White and lower case for black
        S = 'S'
        C = 'C'
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


    def strToNum(self,Str):
        if(Str[0]>='a' and Str[0]<='e'): #for 5x5... Not sure how to check for 6x6 and larger #TODO
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
                part_dir = [part for part in part_list if len(part) <= rem_squares[di]] #######
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
                print(self.B[next_square].peek())
                print(square,direction)
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


    def __getNeighbour(self, pos):                        #Sorry for the Ambiguity between N(Neighbour) and self.N(Board Size)
        N = []
        if pos<0 or pos>=(self.N*self.N):                   #Outside
            return N
        elif pos==0:                                        #Top Left Corner
            N += [pos+1, pos+self.N]
        elif pos == self.N-1:                               #Top Right Corner
            N += [pos-1, pos+self.N]
        elif pos == self.N*(self.N-1):                      #Bottom Left Corner
            N += [pos+1, pos-self.N]
        elif pos == self.N*self.N -1:                       #Bottom Right Corner
            N += [pos-1, pos-self.N]
        elif pos < self.N:                                  #Top Edge
            N += [pos-1, pos+1, pos+self.N]
        elif pos%self.N == 0:                               #Left Edge
            N += [pos+1, pos+self.N, pos-self.N]
        elif (pos+1)%self.N == 0:                           #Right Edge
            N += [pos-1, pos+self.N, pos-self.N]
        elif pos >= self.N*(self.N-1):                      #Bottom Edge
            N += [pos-1, pos+1, pos-self.N]
        else:                                               #Inside
            N += [pos-1, pos+1, pos+self.N, pos-self.N]
        return N


    def __checkRoadVictory(self, Player):
        DFSStack = Stack()
        Visited = set()
        Win = False
        F = 'F'                 #Capital for White and lower case for black
        C = 'C'
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
            for N in Neighbour:           #Sorry for the Ambiguity between N(Neighbour) and self.N(Board Size)
                if N >= self.N*(self.N-1):
                    Win = True
                    return Win
                NAdd = 0
                X = ''
                if not self.B[N].isEmpty():
                    X = self.B[N].peek()
                if not N in Visited:
                    if(X==F or X==C):
                        DFSStack.push(N)
                        Visited.add(N)
                        NAdd += 1
                if NAdd == 0 and not DFSStack.isEmpty():
                    Temp = DFSStack.pop()
        DFSStack = Stack()
        Visited = set()
        for x in range(self.N): #Horizontal Roads
            X = ''
            if not self.B[x*self.N].isEmpty():
                X = self.B[x*self.N].peek()
            if(X==F or X==C):
                DFSStack.push(x)
                Visited.add(x)
        while(not DFSStack.isEmpty()):
            Neighbour = self.__getNeighbour(DFSStack.peek())
            NAdd = 0
            for N in Neighbour:
                if (N+1)%self.N == 0:
                    Win = True
                    return Win
                X = ''
                if not self.B[N].isEmpty():
                    X = self.B[N].peek()
                if not N in Visited:
                    if(X==F or X==C):
                        DFSStack.push(N)
                        Visited.add(N)
                        NAdd += 1
            if NAdd == 0 and not DFSStack.isEmpty():
                Temp = DFSStack.pop()
        return Win 


    #def evaluate(self):
        
    

    def play(self, diff, Player):
        if(not self.Flag):
            if(Player==1):
                self.move(Player,'a1')
                return
            else:
                if(self.B[0].isEmpty()):
                    self.move(Player,'a1')
                else:
                    self.move(Player,chr(self.N-1 + 97) + str(1)) #e1 for 5x5 and so on
                return
        if diff == 1:
            self.playRandom(Player)


    def playRandom(self,Player):
        all_moves = []
        all_moves = self.getAllMoves(Player)
        move = all_moves[random.randint(0, len(all_moves)-1)]
        print(move)
        self.move(Player, move)


    
