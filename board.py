#Rajkumar Pagey
#Board is used for Board Representation, Piece Representation and State Updation
#This Version is just for Prototyping purpose

from pythonds.basic.stack import Stack
import random

class Board:

    def pieces(self, N):
        if(N==5):
            self.Flats = [21,21]
            self.Caps = [1,1]

    def check(self, Player):
        pos = 0
        F = 'F'                 #Caps for White and lower case for black
        S = 'S'
        C = 'C'
        
        if(int(Player) != 1):
            F='f'
            S='s'
            C='c'

        while(True):
            if(pos<0):
                break
            
            if(not self.B[pos].isEmpty()):
                if(self.B[pos]==F or self.B[pos]==C):
                    if(pos>self.N*(self.N-1)):
                        if(not self.B[pos+self.N].isEmpty()):
                           if(self.B[pos+self.N].peek()==F or self.B[pos+self.N].peek()==C):
                                pos += self.N
                        elif(pos%N!=0):
                            if(self.B[pos-1].isEmpty()):
                                if(self.B[pos-1].peek()==F or self.B[pos-1].peek()==C):
                                    pos -= 1
                    elif(pos%N!=N-1 and not self.B[pos+1].isEmpty()):
                        if(self.B[pos+1].peek()==F or self.B[pos+1].peek()==C):
                            pos += 1
                else:
                    self.Win = True;
                    self.Winner = Player
                    break
            elif(pos<self.N-1):
                pos +=1
            elif(pos>self.N):
                pos -= self.N
            else:
                break
            #print(pos)
        pos = 0
#Incomplete:::

        i = 0;
        while(True):
            if(pos<0):
                break

            
            
            #print(pos)
            if(not self.B[pos].isEmpty()):
                if(self.B[pos].peek()==F or self.B[pos].peek()==C):
                    #print(self.B[pos+1].isEmpty())
                    if((pos%self.N)<(self.N-1) and (not self.B[pos+1].isEmpty())):
                        if(self.B[pos+1].peek()==F or self.B[pos+1].peek()==C):
                            pos += 1
                    elif(pos>self.N and not self.B[pos-self.N].isEmpty()):
                            if(self.B[pos-self.N].peek()==F or self.B[pos-self.N].peek()==C):
                                pos -= self.N
                    elif(pos<(self.N*(self.N-1)) and not self.B[pos+self.N].isEmpty()):
                            if(self.B[pos+self.N].peek()==F or self.B[pos+self.N].peek()==C):
                                pos += self.N
                    
                    if(pos%self.N==self.N-1):
                        self.Win = True;
                        self.Winner = Player
                        print(self.Winner,end=F)
                        print(" is the Winner")
                        break
            if(pos%self.N==0 and pos<self.N*(self.N-1)):
                    pos += self.N
            if(i>25):
                break    
            #print(F)
            i +=1
    
    def __init__(self):
        #Initialize Board
        self.N = 5
        self.B = []
        self.Win = False
        self.Winner = ""
        for x in range(self.N*self.N):
            self.B.append(Stack())

        #Initialize Temp Variable
        self.Flag = False        #False for First Move, True from Second
        self.Buffer = Stack()    #For Movement
        self.Move = True         #True for Player 1, False for Player 2; Change Later

        self.pieces(self.N)     #For future Use

        self.Map1 = [0]*self.N*self.N              #Control Map
        

    def move(self, Player, Str):
        F = 'F'                 #Caps for White and lower case for black
        S = 'S'
        C = 'C'
		
        if(self.Flag):
            if(int(Player) != 1):
                F='f'
                S='s'
                C='c'
				
            #self.show()
            #Place Ply
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
            #self.Map1[T] = (Player,1)
			
			

            #Move Ply
            if(Str[0]>='0' and Str[0]<='5'):
                l = len(Str)
                V=0                         #Directions
                H=0
                if(Str[3]=='+'):
                    V=1
                if(Str[3]=='-'):
                    V=-1
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
                        
        else:                                               #Need to optimize this #TODO
            if(int(Player) != 2):
                F='f'
                S='s'
                C='c'
            else:
                self.Flag = True

            #self.show()
            print(" ")
            if(Str[0]>='a' and Str[0]<='e'): #for 5x5... Not sure how to check for 6x6 and larger
                T = 5*(ord(Str[0]) - 97) + int(Str[1]) - 1
                #print(T)
                self.B[T].push(F)
            if(Str[0]=='C'): 
                T = 5*(ord(Str[1]) - 97) + int(Str[2]) - 1
                #print(T)
                self.B[T].push(C)
            if(Str[0]=='S'):
                T = 5*(ord(Str[1]) - 97) + int(Str[2]) - 1
                self.B[T].push(S)

        self.maps()
        #self.check(Player)
        #if(self.Win):
         #   print(self.Winner)
         #   print(" is the Winner")

    def strToNum(self,Str):
        if(Str[0]>='a' and Str[0]<='e'): #for 5x5... Not sure how to check for 6x6 and larger #TODO
            return 5*(ord(Str[0]) - 97) + int(Str[1]) - 1
        if(Str[0]=='C'): 
            return 5*(ord(Str[1]) - 97) + int(Str[2]) - 1
        if(Str[0]=='S'):
            return 5*(ord(Str[1]) - 97) + int(Str[2]) - 1
        if(Str[0]>='0' and Str[0]<='5'):
            return 5*(ord(Str[1]) - 97) + int(Str[2]) - 1
        return -1

    def numToStr(self,Num):
        if Num < 0 or Num >= self.N*self.N:
            return ''
        col = Num % self.N
        row = int(Num / self.N)
        return chr(row + 97) + str(col + 1)

    def maps(self):
        for x in range(self.N*self.N):
            size = self.B[x].size()
            if(size>5):
                size = 5
            Temp = self.B[x].ps(size)
            if(size!=0):
                if(Temp[size-1].isupper()):
                    self.Map1 = [1,Temp.count('F')]
            print(Temp,end='\t')
            if(x%self.N==self.N-1):
                print('')
            
            
    def show(self):                         #This is for Debugging, but I'll need to use some GUI for proper Stack view #TODO
        for x in range(self.N*self.N):
            if(not self.B[x].isEmpty()):
                print(self.B[x].peek(), end='\t')
            else:
                print('_',end='\t')
            if(x%5==4):
                print("")

    def getAllMoves(self, Player):
        all_moves = []
        for x in range(self.N*self.N):
            if(self.B[x].isEmpty()):
                X = self.numToStr(x)
                if(self.Flats[Player-1]>0):
                    all_moves.append(X)
                    all_moves.append('S'+X)
                if(self.Caps[Player-1]>0):
                    all_moves.append('C'+X)
            else:
                if(Player==1 and self.B[x].peek().isupper()):
                    all_moves += (self.getStackMoves(x,Player))
                if(Player!=1 and not self.B[x].peek().isupper()):
                    all_moves += (self.getStackMoves(x,Player))
        return all_moves

    def getStackMoves(self, sq, Player):
        all_moves = []
        r = sq % self.N
        c = sq / self.N
        size = self.B[sq].size()
        dirs = ['+', '-', '<', '>']
        up = self.N - 1 - c
        down = c
        right = self.N - 1 - r
        left = r
        rem_squares = [up, down, left, right]
        for x in range(min(size,self.N)):
            part_list = self.partition(x + 1)
            for di in range(4):
                part_dir = [part for part in part_list if len(part) <= rem_squares[di]] #######
                for part in part_dir:
                    if self.check_valid(x, dirs[di], part):
                        part_string = ''.join([str(i) for i in part])
                        all_moves.append(str(sum(part)) + self.numToStr(sq) + dirs[di] + part_string)
        return all_moves

    def partition(self, n):
        part_list = []
        part_list.append([n])
        for x in range(1, n):
            for y in self.partition(n - x):
                part_list.append([x] + y)
        return part_list

    def check_valid(self, square, direction, partition):
        if direction == '+':
            change = self.N
        elif direction == '-':
            change = -self.N
        elif direction == '>':
            change = 1
        elif direction == '<':
            change = -1
        for i in range(len(partition)):
            next_square = square + change * (i + 1)
            if self.B[next_square].size() > 0 and (self.B[next_square].peek() == 'C' or self.B[next_square].peek() == 'c'):
                return False
            if self.B[next_square].size() > 0 and (self.B[next_square].peek() == 'S' or self.B[next_square].peek() == 's') and i != len(partition) - 1:
                return False
            if i == len(partition) - 1 and self.B[next_square].size() > 0 and (self.B[next_square].peek() == 'S' or self.B[next_square].peek() == 's'):
                return False
            if i == len(partition) - 1 and self.B[next_square].size() > 0 and (self.B[next_square].peek() == 'C' or self.B[next_square].peek() == 'c'):
                return False
            return True

    def play(self,diff,Player):
        if(not self.Flag):
            if(Player==1):
                self.move(Player,'a1')
                return
            else:
                if(self.B[0].isEmpty()):
                    self.move(Player,'a1')
                else:
                    self.move(Player,'e1') #for 5x5 only; #TODO for other dimensions
                return
        if diff == 1:
            self.playRandom(Player)

    def playRandom(self,Player):
        all_moves = []
        all_moves = self.getAllMoves(Player)
        move = all_moves[random.randint(0, len(all_moves)-1)]
        print(move)
        self.move(Player, move)
            
                
#Bo = Board()
#Bo.move(1,"c3")
#Bo.show()
#print(Bo.getAllMoves(2))

#file_object = open("1.ptn", "r")

#B = Board()

#S = file_object.readline()
#while(S):
 #   C = S.count(' ')
  #  Mov = []
   # Mov = S.split(' ')
    #B.move(1, Mov[1])
    
    #if(C==2):
     #   B.move(2, Mov[2].replace("\n",""))
        
    #S = file_object.readline()
    
#B.show()
