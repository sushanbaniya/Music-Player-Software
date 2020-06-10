from tkinter import *

root = Tk()

playphoto = PhotoImage(file ='images/play.png')
playbtn = Button(root, image = playphoto)
playbtn.grid(column = 0, row = 0, padx = 10)

stopbutton = PhotoImage(file ='images/stop.png')
stopbtn = Button(root, image = stopbutton)
stopbtn.grid(column = 1, row = 0, padx = 10)


pauseimage = PhotoImage(file ='images/pause.png')
pausebtn = Button(root, image = pauseimage)
pausebtn.grid(column = 2, row = 0, padx = 10)

root.mainloop()