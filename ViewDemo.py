from board import Board

file_object = open("1.ptn", "r")

B = Board()

S = file_object.readline()
while(S):
    C = S.count(' ')
    Mov = []
    Mov = S.split(' ')
    #B.show()
    #print("-----------------------------------")
    B.move(1, Mov[1])

    #B.show()
    #print("-----------------------------------")

    
    if(C==2):
        B.move(2, Mov[2])
    
    
    S = file_object.readline()
    
B.show()
B.check(1)
#B.check(2)
