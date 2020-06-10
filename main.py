from tkinter import *
import tkinter.messagebox
from pygame import mixer
from mutagen.mp3 import MP3
from tkinter import filedialog
import os
import time
import threading
from tkinter import ttk
from ttkthemes import themed_tk as tk

# Creating Window
root = tk.ThemedTk()
root.get_themes()
root.set_theme("radiance")


# Adding a Status Bar

statusbar = ttk.Label(root, text="Welcome to Sushan's Music Player", relief=SUNKEN, anchor=W, font='Aerial 10 bold')
statusbar.pack(side=BOTTOM, fill=X)

# Creating a menubar
menubar = Menu(root)
root.config(menu=menubar)

playlist = []


def browsefile():
    global filename_path
    filename_path = filedialog.askopenfilename()
    addplaylist(filename_path)


def addplaylist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1


# Creating SubMenu
submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=submenu)
submenu.add_command(label="Open", command=browsefile)
submenu.add_command(label="Exit", command=root.destroy)


def aboutus():
    tkinter.messagebox.showinfo('About Us', 'This music player is created by SUSHAN BANIYA.')


submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=submenu)
submenu.add_command(label="About Us", command=aboutus)

mixer.init()

root.title("Sushan's Music Player")
root.iconbitmap(r'images/melody.ico')

leftframe = Frame(root)
leftframe.pack(side=LEFT)

playlistbox = Listbox(leftframe)

playlistbox.pack()

addbtn = ttk.Button(leftframe, text="+ Add", command=browsefile)
addbtn.pack(side=LEFT)


def delsongs():
    selectedsong = playlistbox.curselection()
    selectedsong = int(selectedsong[0])
    playlistbox.delete(selectedsong)
    playlist.pop(selectedsong)


deletebtn = ttk.Button(leftframe, text="- Delete", command=delsongs)
deletebtn.pack(side=LEFT)

rightframe = Frame(root)
rightframe.pack()

topframe = Frame(rightframe)
topframe.pack()

filelabel = Label(topframe, text='This only plays .wav songs not .mp3', fg='red')
filelabel.pack(pady=10)

lengthlabel = ttk.Label(topframe, text='Total Length - --:--')
lengthlabel.pack()

currenttimelabel = ttk.Label(topframe, text='Current Time - --:--', relief=GROOVE)
currenttimelabel.pack()


def showdetails():
    filelabel['text'] = "Playing Music" + " -- " + os.path.basename(filename_path)

    file_data = os.path.splitext(filename_path)

    if file_data[1] == '.mp3':
        audio = MP3(filename_path)
        totallength = audio.info.length


    else:
        a = mixer.Sound(filename_path)
        totallength = a.get_length()
    mins, secs = divmod(totallength, 60)
    mins = round(mins)
    secs = round(secs)

    timeformat = '{:02d}:{:02d}'.format(mins, secs)

    lengthlabel['text'] = "Total length: " + timeformat

    t1 = threading.Thread(target=startcount, args=(totallength,))
    t1.start()


def startcount(t):
    global paused
    x = 0
    while x <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(x, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time: " + timeformat
            time.sleep(1)
            x += 1


def playmusic():
    global paused

    if paused == True:
        mixer.music.unpause()
        statusbar['text'] = "Music Unpaused"
    else:
        try:
            selectedsong = playlistbox.curselection()
            selectedsong = int(selectedsong[0])
            playit = playlist[selectedsong]
            mixer.music.load(playit)
            mixer.music.play()
            statusbar['text'] = "Playing Music" + " -- " + os.path.basename(filename_path)
            showdetails()
        except:
            tkinter.messagebox.showerror('Error', 'Select a .wav song first by clicking on "+Add" and then select that song and play. ')


def stopmusic():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"


paused = False


def pausemusic():
    global paused
    paused = True
    mixer.music.pause()
    statusbar['text'] = "Music Paused"


def rewindmusic():
    playmusic()
    statusbar['text'] = "Music Rewinded"


def set_vol(val):
    volume = float(val) / 117
    mixer.music.set_volume(volume)


muted = False


def mutemusic():
    global muted
    if muted == True:
        mixer.music.set_volume(0.7)
        scale.set(70)
        volumebtn.configure(image=volumephoto)
        muted = False
    else:
        mixer.music.set_volume(0)
        scale.set(0)
        volumebtn.configure(image=mutephoto)
        muted = True


middleframe = Frame(rightframe)
middleframe.pack(padx=30, pady=30)

playphoto = PhotoImage(file='images/play.png')
playbtn = ttk.Button(middleframe, image=playphoto, command=playmusic)
playbtn.grid(column=0, row=0, padx=10)

stopbutton = PhotoImage(file='images/stop.png')
stopbtn = ttk.Button(middleframe, image=stopbutton, command=stopmusic)
stopbtn.grid(column=1, row=0, padx=10)

pauseimage = PhotoImage(file='images/pause.png')
pausebtn = ttk.Button(middleframe, image=pauseimage, command=pausemusic)
pausebtn.grid(column=2, row=0, padx=10)

# Bottom Frame

bottomframe = Frame(rightframe)
bottomframe.pack()

rewindphoto = PhotoImage(file='images/rewind.png')
rewindbtn = ttk.Button(bottomframe, image=rewindphoto, command=rewindmusic)
rewindbtn.grid(row=0, column=0, padx=30)

mutephoto = PhotoImage(file='images/mute.png')
volumephoto = PhotoImage(file='images/volume.png')
volumebtn = ttk.Button(bottomframe, image=volumephoto, command=mutemusic)
volumebtn.grid(row=0, column=1, padx=30)

scale = ttk.Scale(bottomframe, from_=0, to=117, orient=HORIZONTAL, command=set_vol)
scale.set(70)
mixer.music.set_volume(0.7)
scale.grid(row=0, column=2, pady=15)


def onclosing():
    stopmusic()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", onclosing)
root.mainloop()
