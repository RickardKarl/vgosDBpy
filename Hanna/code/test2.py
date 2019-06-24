

from tkinter import *
from collections import deque
test = {"hej":2, "heej":3, "heeej":4}
window = Tk()

window.title("Choose two or three")


window.geometry('600x300')

lbl = Label(window, text="Click on two or three of the bottoms that you would like to plot")
lbl.grid(column=0, row=0)
place=0;
btn =[]
queue = deque()
names=[]
for key in test:
    names.append(key)

def clicked(i):
    if len(queue) <=3 :
        queue.append(names[i])
    else :
        queue.popleft()
        queue.append(names[i])

    print(queue)
    return


for key in test:
    btn.append(Button(window, text=key, command = lambda:clicked(place) ) )
    btn[place].grid(column=0, row=place+1)
    place = place+1

window.mainloop()



"""


from tkinter import *

window = Tk()

window.title("Welcome to LikeGeeks app")

window.geometry('350x200')

lbl = Label(window, text="Hello")

lbl.grid(column=0, row=0)

txt = Entry(window,width=10)

txt.grid(column=1, row=0)
choosen=[]

def clicked():
    choosen.append()
    print(choosen)

    btn.configure(text= res)

btn = Button(window, text="Click Me", command=clicked())

btn.grid(column=2, row=0)

window.mainloop()
"""
