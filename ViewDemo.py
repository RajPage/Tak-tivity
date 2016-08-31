from board import Board

file_object = open("1.ptn", "r")

B = Board()

S = file_object.readline()
while(S):
    C = S.count(' ')
    Mov = []
    Mov = S.split(' ')
    B.move(1, Mov[1])
    
    if(C==2):
        B.move(2, Mov[2])
        
    S = file_object.readline()
    
B.show()
