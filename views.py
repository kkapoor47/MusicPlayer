from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3  # for finding the total length of song because pygame dont let ous know
import tkinter.ttk as ttk

root = Tk()
root.title('Music Player')
root.geometry('500x400')

# Initialize Pygame Mixer
pygame.mixer.init()


# add_song function
def add_song():
    song = filedialog.askopenfilename(initialdir='Music/', title="Choose a Song", filetypes=(("mp3 Files", "*.mp3"),))
    # stripping out directory info and .mp3
    song = song.replace('C:/Users/khush/PycharmProjects/music_player/Music/', '')
    song = song.replace(".mp3", "")

    songBox.insert(END, song)


# add many song to playlist
def add_many_song():
    songs = filedialog.askopenfilenames(initialdir='Music/', title="Choose a Song", filetypes=(("mp3 Files", "*.mp3"),))

    # loop through song list and replace directory info and mp3 for all the added songs
    for song in songs:
        song = song.replace('C:/Users/khush/PycharmProjects/music_player/Music/', '')
        song = song.replace(".mp3", "")

        songBox.insert(END, song)


# play selected song
def play():
    #set stopped variable to false so song can play
    global stopped
    stopped=False

    # Reset slider and statuc bar
    status_bar.config(text='')
    mySlider.config(value=0)

    song = songBox.get(ACTIVE)  # get whatever song has been selected
    song = f"C:/Users/khush/PycharmProjects/music_player/Music/{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # # call the time function to get song length
    play_time()

    #get current volume
    # currentVolume = pygame.mixer.music.get_volume()
    # sliderLabel.config(text=currentVolume*100)

    # sliderPosition = int(song_length)
    # mySlider.config(to=sliderPosition, value=0)


# stop current playing song
global stopped
stopped=False
def stop():
    #Reset slider and statuc bar
    status_bar.config(text='')
    mySlider.config(value=0)

    #stopping song
    pygame.mixer.music.stop()
    songBox.selection_clear(ACTIVE)
    # clear status bar
    status_bar.config(text='')

    #stop variable to true
    global stopped
    stopped=True




# Global pause variable
global paused
paused = False


# pause and unpause current playing song
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:  # if song was paused then we have to unpause the song
        # unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        # pause
        pygame.mixer.music.pause()
        paused = True


# forward or next song
def nextSong():
    # Reset slider and statuc bar
    status_bar.config(text='')
    mySlider.config(value=0)


    # get current song tuple(number)
    next_one = songBox.curselection()

    # add one to current number to  move forward

    # print(next_one)
    # print(next_one[0])
    next_one = next_one[0] + 1
    # grab song title from playlist
    song = songBox.get(next_one)
    print(song)

    song = f"C:/Users/khush/PycharmProjects/music_player/Music/{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # move ACTIVE bar in playlist
    songBox.selection_clear(0, END)  # active bar disappears

    songBox.activate(next_one)  # have bar on next song

    # set active bar on next song
    songBox.selection_set(next_one, last=None)


# Backward or previous Song
def previousSong():
    # Reset slider and statuc bar
    status_bar.config(text='')
    mySlider.config(value=0)

    # get current song tuple(number)
    next_one = songBox.curselection()

    # add one to current number to  move forward

    # print(next_one)
    # print(next_one[0])
    next_one = next_one[0] - 1
    # grab song title from playlist
    song = songBox.get(next_one)
    print(song)

    song = f"C:/Users/khush/PycharmProjects/music_player/Music/{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # move ACTIVE bar in playlist
    songBox.selection_clear(0, END)  # active bar disappears

    songBox.activate(next_one)  # have bar on next song

    # set active bar on next song
    songBox.selection_set(next_one, last=None)


# Delete highlighted song
def delete_song():
    stop()
    #delete currently selected song
    songBox.delete(ANCHOR)
    # stop music if its playing
    pygame.mixer.music.stop()


# delete all song
def delete_all_song():
    stop()
    #delete all songs
    songBox.delete(0, END)
    # stop music if its playing
    pygame.mixer.music.stop()


# grab song length and time info
def play_time():
    #check for double times when slider moves
    if stopped:
        return

    current_time = pygame.mixer.music.get_pos() / 1000  # get current position (time) of song

    # temp label to get data
    # sliderLabel.config(text=f'Slider: {int(mySlider.get())}and SongPosition:{int(current_time)} ')

    # convert time
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

    # get current song tuple
    # current_song = songBox.curselection()

    # grab song title from playlist
    song = songBox.get(ACTIVE)
    # print(song)

    song = f"C:/Users/khush/PycharmProjects/music_player/Music/{song}.mp3"

    # Load song length with mutagen
    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length
    # convert into time format
    converted_current_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    # increase current time by 1 sec
    current_time += 1

    if int(mySlider.get())==int(song_length):
        status_bar.config(text=f'Time Elapsed:   {converted_current_song_length}')

    elif paused:
        pass

    elif int(mySlider.get()) == int(current_time):
        # slider hasnt moved

        # call the time function to get song length
        sliderPosition = int(song_length)

        mySlider.config(to=sliderPosition, value=int(current_time))
    else:
        # slider has been moved
        # call the time function to get song length
        sliderPosition = int(song_length)

        mySlider.config(to=sliderPosition, value=int(mySlider.get()))

        # convert time
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(mySlider.get())))

        # output  timpe to status bar
        status_bar.config(text=f'Time Elapsed:   {converted_current_time} of  {converted_current_song_length}')

        #move this thing along by one second
        nextTime=int(mySlider.get())+1
        mySlider.config(value=nextTime)

    # output  timpe to status bar
    # status_bar.config(text=f'Time Elapsed:   {converted_current_time}  of  {converted_current_song_length}')

    # update slider positon as current song is playing
    # mySlider.config(value=int(current_time))

    # update time
    status_bar.after(1000, play_time)

        # Slider function

def slide(x):

    # sliderLabel.config(text=f'{int(mySlider.get())} of {int(song_length)}')
    song = songBox.get(ACTIVE)  # get whatever song has been selected
    song = f"C:/Users/khush/PycharmProjects/music_player/Music/{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(mySlider.get()))

def volume(x):
    pygame.mixer.music.set_volume(volumeSlider.get())
    #get current volume
    # currentVolume=pygame.mixer.music.get_volume()
    # sliderLabel.config(text=currentVolume*100)

#Master Frame
masterFrame=Frame(root)
masterFrame.pack(pady=20)




# playlist box
songBox = Listbox(masterFrame, bg='black', fg="green", width="60", selectbackground="gray", selectforeground="black")
songBox.grid(row=0,column=0)

# play buttons images
backwardButton_img = PhotoImage(file='backward.png')
forwardButton_img = PhotoImage(file='forward (1).png')
playButton_img = PhotoImage(file='play-button.png')
pauseButton_img = PhotoImage(file='pause.png')
stopButton_img = PhotoImage(file='stop-button.png')

# player control frame
control_frame = Frame(masterFrame)
control_frame.grid(row=1,column=0,pady=20)

#create volume control Frame
volumeFrame=LabelFrame(masterFrame,text='Volume')
volumeFrame.grid(row=0,column=1)

# play Buttons
backwardButton = Button(control_frame, image=backwardButton_img, borderwidth=0, command=previousSong)
forwardButton = Button(control_frame, image=forwardButton_img, borderwidth=0, command=nextSong)
playButton = Button(control_frame, image=playButton_img, borderwidth=0, command=play)
pauseButton = Button(control_frame, image=pauseButton_img, borderwidth=0, command=lambda: pause(
    paused))  # pause ia a function and we have passed a global variable called paused
stopButton = Button(control_frame, image=stopButton_img, borderwidth=0, command=stop)

backwardButton.grid(row=0, column=0, padx=5)
forwardButton.grid(row=0, column=1, padx=5)
playButton.grid(row=0, column=2, padx=5)
pauseButton.grid(row=0, column=3, padx=5)
stopButton.grid(row=0, column=4, padx=5)

# menubar
myMenu = Menu(root)
root.config(menu=myMenu)

# add song menu
songMenu = Menu(myMenu)
myMenu.add_cascade(label="Add Songs", menu=songMenu)
songMenu.add_cascade(label="Add one song to playlist", command=add_song)

# add many song to playlist
songMenu.add_cascade(label="Add Many song to playlist", command=add_many_song)

# create delete song menu
removeSong_menu = Menu(myMenu)
myMenu.add_cascade(label="Remove Songs", menu=removeSong_menu)
removeSong_menu.add_command(label="Delete a Song from playlist", command=delete_song)
removeSong_menu.add_command(label="Delete all Song from playlist", command=delete_all_song)

# Status bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# create Song slider
mySlider = ttk.Scale(masterFrame, from_=0, to=100, orient=HORIZONTAL, value=0, length=360, command=slide)
mySlider.grid(row=2,column=0,pady=10)


#create volume slider
volumeSlider = ttk.Scale(volumeFrame, from_=0, to=1, orient=VERTICAL, value=1, length=120, command=volume)
volumeSlider.pack(pady=15)

# create slider label
# sliderLabel = Label(root, text="0")
# sliderLabel.pack(pady=2)

root.mainloop()
