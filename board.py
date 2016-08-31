#Rajkumar Pagey
#Board is used for Board Representation, Piece Representation and State Updation
#This Version is just for Demo

from pythonds.basic.stack import Stack

class Board:

    def pieces(self, N):
        if(N==5):
            self.WPiece = 21
            self.BPiece = 21
        
    
    def __init__(self):
        #Initialize Board
        self.N = 5
        self.B = []
        for x in range(self.N*self.N):
            self.B.append(Stack())

        #Initialize Temp Variable
        self.Flag = False        #False for First Move, True from Second
        self.Buffer = Stack()    #For Movement
        self.Move = True         #True for Player 1, False for Player 2; Change Later

        self.pieces(self.N)     #For future Use
        

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
            if(Str[0]>='a' and Str[0]<='e'): #for 5x5... Not sure how to check for 6x6 and larger #TODO
                T = 5*(ord(Str[0]) - 97) + int(Str[1]) - 1
                self.B[T].push(F)
            if(Str[0]=='C'): 
                T = 5*(ord(Str[1]) - 97) + int(Str[2]) - 1
                self.B[T].push(C)
            if(Str[0]=='S'):
                T = 5*(ord(Str[1]) - 97) + int(Str[2]) - 1
                self.B[T].push(S)

            #Move Ply
            if(Str[0]>='0' and Str[0]<='5'):
                l = len(Str)
                T = 5*(ord(Str[1]) - 97) + int(Str[2]) - 1
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

                for x in range(int(Str[0])):
                    self.Buffer.push(self.B[T].pop())

                for x in range(4,l):
                    for y in range(ord(Str[x])-48):             #The Actual Movement
                        Temp = T +(5*H*(x-3)) + V*(x-3)
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
        
            
    def show(self):                         #This is for Debugging, but I'll need to use some GUI for proper Stack view #TODO
        for x in range(self.N*self.N):
            if(not self.B[x].isEmpty()):
                print(self.B[x].peek(), end='\t')
            else:
                print('_',end='\t')
            if(x%5==4):
                print("")

#Bo = Board()
#Bo.move(1,"c3")
#Bo.show()

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
