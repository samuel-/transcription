## pour les chevronnées de la transcription, avec tout mon foie, samuel 
## 

import vlc
#import easygui
import keyboard
#import glob
from time import sleep
import json
#from po import ttkTimer
from pathlib import Path, WindowsPath

try:
	from tkinter import *
	from tkinter.ttk import Style
	from tkinter.ttk import Scale as TTKScale
	from tkinter import filedialog
#	from Tkinter import *
except:
	print("erreur")
	

with open('config.json') as json_file:
    config = json.load(json_file)

class Myplayer:
	def __init__(self):
		self.soundfile = None
		self.recent_index = None
		self.m_length = 0
		self.m_mins = 0
		self.decalages = [2000, 4000]
		self.rate = 1
		self.posmem = 0
		self.timemem = 0
	def setrate(self, r):
		self.rate = r
	
mimi = Myplayer()
player = vlc.MediaPlayer()
mediafile = None
sleep(0.5)

def reclastpos():
	try:
		tim = player.get_time()
		print('setting tim', tim)
		config['lastfiles'][-1]['tim'] = tim
		with open('config.json', 'w') as outfile:
			json.dump(config, outfile)
	except:
		print('tim razté')

def isinrecentfiles(soundPath):
	path = str(soundPath)
	index = None
	for i, media in enumerate(config['lastfiles']):
		if path in media['path']:
			index = i
			break
	if index != None:
		print('found at index',index)
	islast = index == len(config['lastfiles'])-1
	inlist =  index != None
	return inlist, islast, index

def updaterecentfiles(soundPath, inlist, islast, index):
	name = soundPath.name
	path = str(soundPath)
	
	if inlist:
		if islast:
			print('same sound')
			return
		else:
			sound = config['lastfiles'].pop(index)
			print('sound found', sound)
	else:
		sound = {'name': name, 'path': path}
		print('new sound', sound)
	
	config['lastfiles'].append(sound)
	
	if len(config['lastfiles'])>10:
		config['lastfiles'].pop(0)
	
	with open('config.json', 'w') as outfile:
		json.dump(config, outfile)
	
	fillMenu()

def openfile(f=None):
	global player, mediafile
	if config['options']['lastpos'] == 'True' and mediafile != None:
		reclastpos()
	
	try:
		if f != None:
			print('opening', f)
			soundfilePath = Path(f)
			soundfile = str(soundfilePath)
		else:
			root.filename = filedialog.askopenfilename(initialdir = ".", title = "Choisis ton fichier", 
				filetypes = (("sons","*.mp3 *.wav *.aiff *.flac *.ogg"), ("tous","*.*")))
			if root.filename == '':
				print("ouverture du fichier annulée")
				return
			else:
				soundfilePath = Path(root.filename)
				soundfile = str(soundfilePath)
				print('file opened', soundfile)
	except IOError:
		print('échec ouverture du fichier')
	
	playingfile.set(soundfile)
	mediafile = vlc.Media(soundfile)
	player.set_media(mediafile)
	
	try:
		player.set_pause(1)
		player.audio_set_volume(0)
		player.play()
		player.set_position(0)
		#pos.set(0)
		player.audio_set_volume(90)
		
		playingvar.set("Lecture")
		
		m_length = 0
		i = 0
		while m_length < 10 and i < 30:
			sleep(0.1)
			m_length = player.get_length()
			i += 1
		if m_length < 10:
			print("ERREUR CHARGEMENT DU FICHIER")
		
	except:	
		print("erreur lancement du fichier")
	
	inlist, islast, index = isinrecentfiles(soundfilePath)
	
	if inlist and config['options']['lastpos'] == 'True' :
		if 'tim' in config['lastfiles'][index].keys():
			newposition = config['lastfiles'][index]['tim']
			player.set_time(newposition)
			sleep(0.1)
			pos.set(player.get_position())
			setmemory()
			print('lecture au temps', newposition)
	updaterecentfiles(soundfilePath, inlist, islast, index)
	
	if config['options']['playlast'] == 'False':
		playpause()
	

def effacerrecents():
	pass

def playpause():
	if player.is_playing():
		player.pause()
		playingvar.set("Pause")
		print('pause')
	else:
		player.play()
		playingvar.set("Lecture")
		print('play')

def moving(e):
	position = float(pos.get())
	#print(position,type(position))
	if player != None:
		print(player.get_state())
		player.set_position(position)

def convertMillis(millis):
	millis = int(millis)
	seconds=(millis/1000)%60
	seconds = int(seconds)
	minutes=(millis/(1000*60))%60
	minutes = int(minutes)
	hours=(millis/(1000*60*60))%24
	return ("%d:%d:%d" % (hours, minutes, seconds))

def configit(param, var):
	if var.get():
		config['options'][param] = 'True'
	else:
		config['options'][param] = 'False'
	print(config)
	with open('config.json', 'w') as outfile:
		json.dump(config, outfile)

def setmemory():
	if player != None:
		mimi.timemem = player.get_time()
		mimi.posmem = player.get_position()
		posmem.set(mimi.posmem)
def tomemory():
	if player != None:
		pos.set(mimi.posmem)
		posLabel.set(convertMillis(mimi.timemem))
		player.set_position(mimi.posmem)
def back(i=0,sens=1):
	if player != None:
		mimi.timemem = player.get_time()
		mimi.posmem = player.get_position()
		posmem.set(mimi.posmem)
		time = mimi.timemem  - mimi.decalages[i]*sens
		player.set_time(time)
		pos.set(player.get_position())
		posLabel.set(convertMillis(time))

def setrate(x):
	if player != None:
		if x == -1:
			r = 1
		else:
			r = mimi.rate + x
		r = max(min(r,3),0.25)
		mimi.setrate(r)
		print('Vitesse de lecture', mimi.rate)
		player.set_rate(mimi.rate)
		rateLabel.set(mimi.rate)

def update_clock(_=None):
	pos.set(player.get_position())
	time = player.get_time()
	posLabel.set(convertMillis(time))
	root.after(1000, update_clock)
	#print('tic')


def fermer():
	print('byebye')
	if config['options']['lastpos'] == 'True' and mediafile != None:
		reclastpos()
	player.release()
	
	root.destroy()


root = Tk()
root.title("Transcription ☺☻♥♦♣♠•◘○")
root.protocol("WM_DELETE_WINDOW", fermer)
s = Style()
#print(s.theme_names())
#s.theme_use('vista')

pos = DoubleVar()
posmem = DoubleVar()
posLabel = StringVar()
rateLabel = StringVar()
rateLabel.set(1)
playingvar = StringVar()
playingfile = StringVar()
playingvar.set("Stop")

openlast = BooleanVar()
openlast.set((config['options']['openlast'] == 'True'))
lastpos = BooleanVar()
lastpos.set((config['options']['lastpos'] == 'True'))
playlast = BooleanVar()
playlast.set((config['options']['playlast'] == 'True'))

def fillMenu():
	last = config['lastfiles']
	recentfiles.delete(0,11)
	if len(last)>0:
		for i in range(len(last)-1, -1, -1):
			nom = last[i]['name']
			path = last[i]['path']
			recentfiles.add_command(label=nom, command=lambda bpath=path:openfile(bpath))
menubar = Menu(root)
# create a pulldown menu, and add it to the menu bar
recentfiles = Menu(menubar, tearoff=0)
fillMenu()
menubar.add_cascade(label="Fichiers Récents", menu=recentfiles)
###########################
menubar.add_command(label="Ouvrir", command=openfile)
###########################
menubar.add_separator()
configmenu = Menu(menubar, tearoff=0)
configmenu.add_checkbutton(label="Lire les fichiers dès l'ouverture", variable=playlast, command=lambda:configit('playlast', playlast))
configmenu.add_checkbutton(label="Ouvrir tout de suite le dernier fichier lu", variable=openlast, command=lambda:configit('readlast', readlast))
configmenu.add_checkbutton(label="Se souvenir de la position de lecture", variable=lastpos, command=lambda:configit('lastpos', lastpos))
#configmenu.add_checkbutton(label="Se souvenir des fichiers récents")
#configmenu.add_separator()
#configmenu.add_command(label="Raccourcis et réglages")

menubar.add_cascade(label="Options", menu=configmenu)
###########################
menubar.add_separator()
menubar.add_command(label="Quitter", command=fermer)
###########################
root.config(menu=menubar)
###########################

# progression
#w2 = Scale(root, from_=0, to=10, length=600, label="durée <<", showvalue=1, resolution=-1, orient=HORIZONTAL)
Label(root, textvariable=playingfile).pack()
Label(root, textvariable=playingvar).pack()
w2 = TTKScale(root, from_=0, to=1, length=600, orient=HORIZONTAL, command=moving, variable=pos)
w2.pack(fill=X, expand=1)
w3 = TTKScale(root, from_=0, to=1, length=600, orient=HORIZONTAL, variable=posmem, takefocus=0)
w3.state(['disabled'])
w3.pack(fill=X, expand=1)
Label(root, textvariable=posLabel).pack()

Button(root, text="<<<", command=lambda:back(1)).pack(side=LEFT, padx=5, pady=5)
Button(root, text="<<", command=lambda:back(0)).pack(side=LEFT, padx=5, pady=5)
Button(root, text="Play/Pause", command=playpause).pack(side=LEFT, padx=5, pady=5)
Button(root, text=">>", command=lambda:back(0,-1)).pack(side=LEFT, padx=5, pady=5)
Button(root, text=">>>", command=lambda:back(1,-1)).pack(side=LEFT, padx=5, pady=5)

Button(root, text="§", command=setmemory).pack(side=LEFT, padx=5, pady=5)
Button(root, text="§!", command=tomemory).pack(side=LEFT, padx=5, pady=5)
#Button(root, text="%", command=memory).pack()

Button(root, text="+ lent", command=lambda:setrate(-0.125)).pack(side=LEFT, padx=5, pady=5)
Button(root, text="x 1", command=lambda:setrate(-1)).pack(side=LEFT, padx=5, pady=5)
Button(root, text="+ rapide", command=lambda:setrate(0.125)).pack(side=LEFT, padx=5, pady=5)
Label(root, textvariable=rateLabel).pack(side=LEFT, padx=5, pady=5)
#TTKScale(root, from_=0.25, to=3, length=100, orient=HORIZONTAL, command=None, variable=rate).pack()

#Button(root, text="Quitter", command=root.destroy).pack(side = RIGHT)

legende = "play/pause: Alt Gr        "
legende += "<</>>: (Ctrl) Alt ⇔        "
legende += "§: right_Shift        "
legende += "→§: Alt right_Shift        "
legende += "vitesse: Alt ⇕       "
Label(root, text=legende).pack(side=BOTTOM, fill=X, padx=5, pady=5)
##⇕ ⇒⇐⇑⇓⇔⇕⇕
# play/pause: Alt Gr      <</>>: (Ctrl) Alt ⇔   	§: right_Shift    →§: Alt right_Shift

keyboard.add_hotkey('alt gr', playpause)

keyboard.add_hotkey('alt+gauche', lambda:back(0))
keyboard.add_hotkey('ctrl+alt+gauche', lambda:back(1))

keyboard.add_hotkey('alt+droite', lambda:back(0,-1))
keyboard.add_hotkey('ctrl+alt+droite', lambda:back(1,-1))

keyboard.add_hotkey('right shift', setmemory)
keyboard.add_hotkey('alt+right shift', tomemory)

#volume
#keyboard.add_hotkey('ctrl+haut', tomemory)
#keyboard.add_hotkey('ctrl+bas', tomemory)

keyboard.add_hotkey('alt+haut', lambda:setrate(0.125))
keyboard.add_hotkey('alt+bas', lambda:setrate(-0.125))
keyboard.add_hotkey('alt+bas+haut', lambda:setrate(-1))



if config['options']['openlast'] == 'True':
	try:
		openfile(config['lastfiles'][-1]['path'])
	except:
		pass

update_clock(None)

mainloop()
#player.release()
#root.destroy()

#keyboard.wait()



