import tkinter as tk
from tkinter import *
import numpy as np
import matplotlib.pyplot as plt

window=tk.Tk()


flagging=False
# knowledge_base=[]

new_inference=[]

ai_move="None"

def flag():
    global flagging
    if flagging:
        flagging=False
    else:
        flagging=True

button=Button(window,text='Flag',bg="red",command=flag)
button.pack()


canvas= Canvas(window, width=100, height=100)
canvas.pack(side=LEFT)
pixelVirtual = tk.PhotoImage(width=1, height=1)

suggestion = tk.Label(window, text="None")
suggestion.pack(side=RIGHT)

size=8

class Box():
    def __init__(self,pos):
        self.pos=pos
        self.value=0
        self.explored=False
        self.button=Button(canvas,image=pixelVirtual,text='*',command=self.switch,bg="white",width=40,height=40,compound="c")
        self.button.grid(row = pos[0], column = pos[1])

    def switch(self):
        global flagging
        global ai_move


        if self.button['bg']=='white' or self.button['bg']=='green':
            if flagging:
                self.button.configure(bg = "green")
                self.button.configure(fg = "white")
                self.button.configure(text = "f")
                flagging=False

            elif self.pos in bombs:
                self.button.configure(bg = "red")
                self.button.configure(fg = "white")
                self.button.configure(text = str(self.value))
                print("Bomb exploded")
                # exit()
            
            else:
                self.button.configure(bg = "black")
                self.button.configure(fg = "white")
                self.button.configure(text = str(self.value)+"("+str(self.pos[0])+","+str(self.pos[1])+")")
                if self.value==0:
                    expose_neighbours(self.pos)
            if game_ended():
                print("You WIN !!!")
                exit()
            else:
                ai_move=AI()
                # print(ai_move)



class Board():
    def __init__(self,bombs):
        self.board=[]
        self.bombs=bombs
        for i in range(size):
            temp=[]
            for j in range(size):
                s=Box([i,j])
                temp.append(s)
            self.board.append(temp)

        for i in range(size):
            for j in range(size):
                self.board[i][j].value=self.neighbours([i,j])
    

    def neighbours(self,pos):
        if pos in self.bombs:
            return -10
        sum=0
        for i in range(pos[0]-1,pos[0]+2):
            for j in range(pos[1]-1,pos[1]+2):
                if [i,j] in self.bombs:
                    sum+=1
        
        return sum


number_of_bombs=np.random.randint(4,size*2+2)

bombs=[]

for i in range(number_of_bombs):
    x=np.random.randint(size)
    y=np.random.randint(size)
    bombs.append([x,y])

my_board=Board(bombs)

# for i in range(size):
#     for j in range(size):
#         my_board.board[i][j].switch()

print(number_of_bombs)

# button=Button(window,text='r')
# button.pack(side=RIGHT)


def game_ended():
    f=[]
    no_f=0
    for i in range(size):
        for j in range(size):
            if (my_board.board[i][j].button['bg']=="green"):
                no_f+=1
                f.append([i,j])
    if no_f==number_of_bombs:
        bombs_arr=np.array(bombs)
        bombs_sorted= bombs_arr[bombs_arr[:,1].argsort()]
        bombs_sorted= bombs_sorted[bombs_sorted[:,0].argsort()]

        # print(bombs_sorted)
        # f=np.array(f)
        # print(f)
        if (bombs_sorted==f).all():
            return True

    else:
        return False

def AI():
    # global knowledge_base
    inference=[]
    knowledge_base=[]
    for i in range(size):
        for j in range(size):
            if my_board.board[i][j].button['bg']!="black":
                continue
            if my_board.board[i][j].value==0:
                continue
            my_board.board[i][j].explored=True
            print(i,j)

            t=[]
            for x in range(i-1,i+2):
                for y in range(j-1,j+2):
                    if x < 0 or y < 0 or x > size-1 or y > size-1:
                        continue
                    if my_board.board[x][y].button['bg']=="black":
                        continue
                    t.append([x,y])
            knowledge_base.append({"self pos":[i,j],"info":{"pos":t,"number":my_board.board[i][j].value}})


    for k in knowledge_base:
        if len(k["info"]["pos"])==k["info"]["number"]:
            if k["info"] in inference:
                continue
            else:
                inference.append(k["info"])
        for t in knowledge_base:
            if t==k:
                continue
            if (all(x in k["info"]["pos"] for x in t["info"]["pos"])):
                temp=[]
                for x in k["info"]["pos"]:
                    if x in t["info"]["pos"]:
                        continue
                    else:
                        temp.append(x)
                inf={"pos":temp,"number":k["info"]["number"]-t["info"]["number"]}
                if inf in inference:
                    continue
                inference.append(inf)
    global new_inference
    for i in inference:
        if i in new_inference:
            continue
        if i["number"]==0 and i["pos"]!=[]:
            suggestion.configure(text=i)
            new_inference.append(i)
            break
        if i["number"]==len(i["pos"]):
            suggestion.configure(text=i)
            new_inference.append(i)
            break
    print("KB+++++++++++++++++++++++++++++++++")
    for k in knowledge_base:
        print(k)
    print(len(knowledge_base))
    print("inference**************************")
    for i in inference:
        print(i)
    print(len(inference))
    with open("e.txt","w") as f:
        f.write(str(new_inference))

    return "Hi"



def expose_neighbours(pos):
    # print(pos)
    
    for i in range(pos[0]-1,pos[0]+2):
        for j in range(pos[1]-1,pos[1]+2):
            if i < 0 or j < 0 or i > size-1 or j > size-1:
                continue 
            if i==pos[0] and j==pos[1]:
                continue
            # print("*************************",i,j)
            my_board.board[i][j].switch()


window.mainloop()