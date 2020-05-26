from tkinter import *
from tkinter import ttk
from tkinter.ttk import Notebook
from tkinter import messagebox
import random
from googletrans import Translator
import os
from gtts import gTTS
from playsound import playsound
import csv
from threading import Thread

###############
'''
If you have Python3
Open your terminal and run
--------------
python3 -m pip install gtts
python3 -m pip install playsound
python3 -m pip install googletrans
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
brew install portaudio
python3 -m pip install pyaudio
python3 -m pip install pyobjc
--------------
'''



deletemp3 = True 
allfolder = os.listdir()

#############WRITE CSV IF NOT IN CURRENT FOLDER #############
def writevocab():
	data = [['こんにちは','Hello'],
				['こんばんは','Good evening']]
	with open('vocab.csv','w',newline='',encoding='utf-8') as f:
		fw = csv.writer(f)
		fw.writerows(data)

if 'vocab.csv' not in allfolder:
	writevocab()

############# READ VOCAB.CSV FUNCTION #############
def readvocab():
	with open('vocab.csv',newline='',encoding='utf-8') as f:
		fr = csv.reader(f)
		conf = list(fr)
		print(conf)
	return conf

############# DELETE MP3 IF IN FOLDER #############

if deletemp3:
	for f in allfolder:
		if f[-3:] == 'mp3':
			os.remove(f)

randomnum = list(range(65,90)) #gen A-z for ascii
global playagain
playagain = True

def generatename():
	nm = ''
	for i in range(15):
		rd = chr(random.choice(randomnum))
		nm += rd
	nm += '.mp3'
	return nm

allfilename = []


################# READ VOCAB ##################

connection = False 
global allvocab

allvocab = readvocab() #read vocab from vocab.csv inside current folder
allvocabdict = {}

def UpdateVocab():
	global allvocab
	
	v_statusbar.set('Updating Vocab...')
	vocablist.delete(*vocablist.get_children())
	print('Updating Vocab...')
	allvocab = readvocab()
	vclist = []
	for vc in allvocab:
		if vc[0] not in allvocabdict:
			allvocabdict[vc[0]] = vc[1]
		vclist.append(vc)
	for v in vclist:
		vocablist.insert('','end',value=v)

#################GOOGLE SHEET##################

GUI = Tk()
GUI.title('YiPun by Uncle Engineer v.0.0.1')
GUI.geometry('1100x600+0+0')
GUI.state('zoomed')
try:
	GUI.iconbitmap('flashcard.ico')
except:
	pass


menubar = Menu(GUI)
GUI.config(menu=menubar)

filemenu = Menu(menubar,tearoff=0)
# filemenu.add_command(label='Close', command=GUI.quit)
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='Exit',command=lambda: GUI.withdraw())

vocabmenu = Menu(menubar,tearoff=0)
#vocabmenu.add_command(label='Update Vocab',command=UpdateVocab)
vocabmenu.add_command(label='Add Vocab',command=lambda x=None: (Tab.select(F3),E1.focus()))
menubar.add_cascade(label='Vocab',menu=vocabmenu)


import webbrowser
def ContactUs():
	url = 'http://uncle-engineer.com'
	webbrowser.open(url)


def UncleEngineer():
	url = 'https://www.facebook.com/UncleEngineer'
	webbrowser.open(url)

def Documentation():
	url = 'https://github.com/UncleEngineer/YiPun'
	webbrowser.open(url)

helpmenu = Menu(menubar,tearoff=0)
helpmenu.add_command(label='Contact Us',command=ContactUs)
helpmenu.add_command(label='Donate',command=lambda: messagebox.showinfo('Donate','Paypal: loong.wissawakorn@gmail.com\nName: Uncle Engineer'))
helpmenu.add_command(label='Uncle Engineer',command=UncleEngineer)
helpmenu.add_command(label='Documentation',command=Documentation)
menubar.add_cascade(label='Help',menu=helpmenu)



Font = ('TH Sarabun',16)
TKFont = ttk.Style()
TKFont.configure('TButton', font=('TH Sarabun', 12))

Tab = Notebook(GUI)

F1 = Frame(Tab)
F2 = Frame(Tab)
F3 = Frame(Tab)
Tab.pack(fill=BOTH, expand=1)

try:
	flashcard = PhotoImage(file='tab_flashcard.png')
	vocab = PhotoImage(file='tab_vocab.png')
	transicon = PhotoImage(file='translate.png')

	Tab.add(F1, text='Flashcard', image=flashcard,compound='top')
	Tab.add(F2, text='All vocab', image=vocab,compound='top')
	Tab.add(F3, text='Translate', image=transicon,compound='top')
except:
	Tab.add(F1, text='Flashcard')
	Tab.add(F2, text='All vocab')
	Tab.add(F3, text='Translate')

global current_vocab
current_vocab = None
global checked
checked = False

def RandomFlashcard(event=None):
	v_check.set('')
	global checked
	checked =False
	vc = random.choice(allvocab)
	global current_vocab
	current_vocab = vc
	print(vc)
	v_vocab.set(vc[0])
	v_trans.set('')
	global playagain
	playagain = True

def ShowTranslate(event=None):
	v_trans.set(current_vocab[1])

def CheckTranslate(event=None):
	global checked
	print([v_check.get()],[current_vocab[1]])
	if v_check.get() == current_vocab[1].replace(' ','') and checked != True:
		v_score.set(int(v_score.get()) + 1)
		
		checked = True
		#RandomFlashcard() #uncomment this if autonextword

	v_trans.set(current_vocab[1])

##########################

def SpeakNow(event=None):
	print(allfilename)
	print(v_vocab.get())
	global playagain
	tts = gTTS(text=v_vocab.get(), lang='ja')

	if playagain == True:
		name = generatename()
		allfilename.append(name)

		tts.save(name)
		playagain = False

	if len(allfilename) > 1:
		os.remove(allfilename[0])
		del allfilename[0]
	playsound(allfilename[0])


def SpeakNow2(event=None):


	#v_translatenow.get()
	global playagain

	if v_radio.get() == 'ja':
		tts = gTTS(text=v_transvocab.get(), lang='ja')
	else:
		tts = gTTS(text=v_texttras.get(), lang='ja')
	
	if playagain == True:
		name = generatename()
		allfilename.append(name)

		tts.save(name)
		playagain = False


	
	if len(allfilename) > 1:
		os.remove(allfilename[0])
		del allfilename[0]
	playsound(allfilename[0])


GUI.bind('<F4>',SpeakNow2)

def SpeakNow3(vocab_sound):

	#v_translatenow.get()
	global playagain
	tts = gTTS(text=vocab_sound, lang='ja')

	if playagain == True:
		name = generatename()
		allfilename.append(name)

		tts.save(name)
		playagain = True
	
	if len(allfilename) > 1:
		os.remove(allfilename[0])
		del allfilename[0]
	playsound(allfilename[0])
##########################


FB0 = Frame(F1)
FB0.place(x=100,y=200)


check_label = Label(FB0,text='Check Meaning',font=(None,20))
check_label.grid(row=0,column=0)

v_check = StringVar()
check_vocab = ttk.Entry(FB0,textvariable=v_check,font=(None,20),width=50)
check_vocab.grid(row=0,column=1,padx=20,pady=20)
check_vocab.focus()
#### BIND #####
check_vocab.bind('<Return>',CheckTranslate)
GUI.bind('<F1>',RandomFlashcard)
GUI.bind('<F2>',ShowTranslate)

FB1 = Frame(F1)
FB1.place(x=100,y=300)


nextvocab = ttk.Button(FB1,text='Next word',command=RandomFlashcard)
nextvocab.grid(row=1,column=1,padx=20,ipadx=20,ipady=10)

nextvocab = ttk.Button(FB1,text='Show Meaning',command=ShowTranslate)
nextvocab.grid(row=1,column=2,padx=20,ipadx=20,ipady=10)

checkvocab = ttk.Button(FB1,text='Check Meaning',command=CheckTranslate)
checkvocab.grid(row=1,column=3,padx=20,ipadx=20,ipady=10)

speak = ttk.Button(FB1,text='Play Sound',command=SpeakNow)
speak.grid(row=1,column=4,padx=20,ipadx=20,ipady=10)

GUI.bind('<F3>',SpeakNow)

#######LABEL VOCAB########
#FB2 = Frame(F1)
#FB2.place(x=100,y=50)
v_vocab = StringVar()
v_trans = StringVar()

show_vocab = Label(F1, textvariable=v_vocab,font=(None,50,'bold'))
show_vocab.place(x=100,y=20)

show_translate = Label(F1, textvariable=v_trans,font=(None,30,'bold'),fg='green')
show_translate.place(x=100,y=100)

v_score = StringVar()
v_score.set('0')

score_label =Label(F1,text='Points',font=(None,30))
score_label.place(x=50,y=400)

score = Label(F1, textvariable=v_score,font=(None,30,'bold'),fg='red')
score.place(x=150,y=400)

def SoundTreeview(event=None):
	global playagain
	try:
		select = vocablist.selection()
		data = vocablist.item(select)
		print(data)
		vocabsound = data['values'][0]
		SpeakNow3(vocabsound)
		playagain == False

	except:
		messagebox.showinfo('Please Select Row','Plese select a vocab')


############## TAB2 #############
def ReplaceVocab(event=None):
	data = []

	for k,v in allvocabdict.items():
		dt = [k,v]
		print(dt)
		data.append(dt)

	with open('vocab.csv','w',newline='',encoding='utf-8') as f:
		fw = csv.writer(f)
		fw.writerows(data)
	UpdateVocab()
	CountVocab()

def UpdateMeaningVocab(vocab,trans):
	global allvocabdict
	allvocabdict[vocab] = trans
	ReplaceVocab()
	UpdateVocab()
	CountVocab()




GUI.bind('<F12>',ReplaceVocab)


def DeleleVocab(event=None):
	try:
		select = vocablist.selection()
		print('SELECT ID', select)
		if len(select) == 1:
			data = vocablist.item(select)
			selectvocab = data['values'][0]
			print('Deleting..',selectvocab)
			del allvocabdict[selectvocab]
			ReplaceVocab()
		else:
			for sl in select:
				data = vocablist.item(sl)
				selectvocab = data['values'][0]
				
				print('Deleting..',selectvocab)
				del allvocabdict[selectvocab]
				ReplaceVocab()
				
			selectvocab = data['values'][0] #ดักจับ error
	except:
		print('ERROR')


def UpdateVocabUI(event=None):
	try:
		select = vocablist.selection()
		print('SELECT ID', select)
		data = vocablist.item(select)
		v1 = data['values'][0]
		v2 = data['values'][1]

		def SaveVocab(event=None):
			nv1 = v_updatevocab.get()
			nv2 = v_updatevocab2.get()
			UpdateMeaningVocab(nv1,nv2)
			print(f'Updated: {nv1} to {nv2}')
			GUI2.withdraw()

		GUI2 = Toplevel()
		GUI2.geometry('400x250+0+0')
		GUI2.title('Update Meaning')
		v_updatevocab = StringVar()
		v_updatevocab.set(v1)
		v_updatevocab2 = StringVar()
		v_updatevocab2.set(v2)
		EM1 = ttk.Entry(GUI2,textvariable=v_updatevocab,font=(None,20,'bold'))
		EM1.pack(pady=10)
		EM2 = ttk.Entry(GUI2,textvariable=v_updatevocab2,font=(None,20))
		EM2.pack(pady=10)
		EM2.bind('<Return>',SaveVocab)
		EM2.focus()
		BS = ttk.Button(GUI2,text='Save',command=SaveVocab)
		BS.pack(ipadx=20,ipady=20)

		GUI2.bind('<Escape>',lambda x: GUI2.withdraw())
		GUI2.mainloop()
	except:
		messagebox.showwarning('Please Select Vocab','Plese select a word')

v_countvocab = StringVar()
L1 = Label(F2,text='All Vocabulary:',font=(None,20)).place(x=50,y=30)
L1 = Label(F2,textvariable=v_countvocab,font=(None,20)).place(x=200,y=30)
L2 = Label(F2,text='Double Click for Playsound',font=(None,15)).place(x=50,y=600)
header = ['Vocab','Translation']



vocablist = ttk.Treeview(F2, columns=header, show='headings',height=10)
vocablist.place(x=20,y=80)

L2 = Label(F2,text='Mac OS: Control + D for Delete Vocab, F7 for Change Meaning, Double Click for Playsound').place(x=50,y=520)

###############
def RunSoundTreeview(event=None):
	v_statusbar.set('Play Sound...')
	task = Thread(target=SoundTreeview)
	task.start()

vocablist.bind('<Double-1>', RunSoundTreeview)
vocablist.bind('<Control-d>',DeleleVocab)
vocablist.bind('<F11>',UpdateVocabUI)

#### Right Click Menu ####
deletemenu = Menu(GUI,tearoff=0)
deletemenu.add_command(label='Delete Vocab',command=DeleleVocab)
deletemenu.add_command(label='Change Meaning',command=UpdateVocabUI)

def popup(event):
	deletemenu.post(event.x_root,event.y_root)

vocablist.bind('<Button-3>',popup)

vocablist.bind('<F7>',UpdateVocabUI)



for hd in header:
	#tree.column("#0",minwidth=0,width=100, stretch=NO)
	vocablist.heading(hd,text=hd)

headerwidth = [(100,600),(100,400)]

for hd,W in zip(header,headerwidth):
	vocablist.column(hd,minwidth=W[0],width=W[1])


# for vc in allvocab:
# 	if vc[0] not in allvocabdict:
# 		vocablist.insert('','end',value=vc)
# 		allvocabdict[vc[0]] = vc[1]


style = ttk.Style()
style.configure("Treeview.Heading", font=(None, 15),rowheight=40)
style.configure("Treeview", font=(None, 20),rowheight=40)


scrolling = ttk.Scrollbar(F2, orient="vertical", command=vocablist.yview)
scrolling.pack(side='right',fill='y')
vocablist.configure(yscrollcommand=scrolling.set)


##############################
def add_vocab(list_data):
	with open('vocab.csv','a',newline='',encoding='utf-8') as f:
		fw = csv.writer(f)
		fw.writerow(list_data)

Lam = Translator()

v_jisho = StringVar()

def TranslateNow(event=None):
	print(v_radio.get(), v_texttras.get())

	trans = Lam.translate(v_texttras.get(),dest=v_radio.get())
	v_jisho.set(trans.text)
	alltext = ''
	alltext += trans.text
	if trans.pronunciation != None and v_radio.get() == 'ja':
		alltext += '\nคำอ่าน: ' + trans.pronunciation
	v_translatenow.set(alltext)
	v_transvocab.set(trans.text)
	if savetosheet.get() == 1:
		try:
			if v_radio2.get() == 'google':
				texttrans = trans.text
			else:
				texttrans = v_manualtrans.get()

			if v_radio.get() == 'th' or v_radio.get() == 'en':
				if v_texttras.get() not in allvocabdict:
					add_vocab([v_texttras.get(),texttrans])
			else:
				if v_texttras.get() not in allvocabdict:
					add_vocab([texttrans,v_texttras.get()])

			v_statusbar.set('Record done!')
			UpdateVocab()
			CountVocab()
		except:
			print('Can not save')
	global playagain
	playagain = True

L1 = Label(F3, text = 'Type a vocab / sentence',font=(None,20))
L1.pack(pady=10)


FR0 = LabelFrame(F3,text='Translate to')
FR0.pack()

v_radio = StringVar()

RB1 = Radiobutton(FR0,text='   Japanese',variable=v_radio,value='ja')
RB2 = Radiobutton(FR0,text=' Thai  ',variable=v_radio,value='th')
RB3 = Radiobutton(FR0,text='English   ',variable=v_radio,value='en')
RB1.invoke()

RB1.grid(row=0,column=1,pady=5,padx=10)
RB2.grid(row=0,column=2,pady=5,padx=10)
RB3.grid(row=0,column=3,pady=5,padx=10)

FR1 = LabelFrame(F3,text='Automated / Manual')
FR1.pack(pady=10)

def ShowTranslateManual(event=None):
	if v_radio2.get() == 'google':
		try:
			LM2.grid_forget()
			E2.grid_forget()
		except:
			pass
	else:
		LM2.grid(row=0,column=0)
		E2.grid(row=1,column=0)


v_radio2 = StringVar()

RB3 = Radiobutton(FR1,text='Google Translate',variable=v_radio2,value='google',command=ShowTranslateManual)
RB4 = Radiobutton(FR1,text='Manual Translate',variable=v_radio2,value='manual',command=ShowTranslateManual)
RB3.invoke()
RB3.grid(row=0,column=3,pady=5,padx=10)
RB4.grid(row=0,column=4,pady=5,padx=10)

savetosheet = IntVar()
savetosheet.set(0)

cbtn = Checkbutton(F3,text='Save to Database',variable=savetosheet)
cbtn.pack()

# if connection == False:
# 	cbtn.config(state='disabled')


v_texttras = StringVar() #เก็บสิ่งที่เราพิมพ์ไว้
E1 = ttk.Entry(F3, textvariable = v_texttras,font=(None,20),width=70)
E1.pack(pady=10)
E1.bind('<Return>',TranslateNow)

FLM = Frame(F3)
FLM.pack()

LM2 = Label(FLM,text='Manual Translate')
LM2.grid(row=0,column=0)

v_manualtrans = StringVar() #เก็บสิ่งที่เราพิมพ์ไว้
E2 = ttk.Entry(FLM, textvariable = v_manualtrans,font=(None,20),width=70)
E2.grid(row=1,column=0)
E2.bind('<Return>',TranslateNow)

EBF = Frame(F3)
EBF.pack(pady=20,ipadx=20,ipady=10)

EB1 = ttk.Button(EBF,text='Translate',command=TranslateNow)
EB1.grid(row=0,column=0,padx=10,ipadx=15,ipady=10)

EB2 = ttk.Button(EBF,text='Playsound',command=SpeakNow2)
EB2.grid(row=0,column=1,padx=10,ipadx=15,ipady=10)

#EB3 = ttk.Button(EBF,text='อ่านออกเสียง (ความหมายญี่ปุ่น)',command=SpeakNow3)
#EB3.grid(row=0,column=2,padx=10,ipadx=15,ipady=10)

v_transvocab =StringVar()

v_translatenow = StringVar()
v_translatenow.set('----Result----')

F31 = Frame(F3)
F31.pack(pady=20)

trans_label =Label(F31,text='Meaning',font=(None,30))
trans_label.pack()

resulttext = Label(F31, textvariable=v_translatenow,font=(None,30,'bold'),fg='red')
resulttext.pack()


# hide manual translation in the first time
LM2.grid_forget()
E2.grid_forget()

def JishoWeb(event=None):
	gettext = v_jisho.get()
	if len(gettext) > 0:
		url = 'https://jisho.org/search/'+ gettext
		webbrowser.open(url)
GUI.bind('<F5>',JishoWeb)

def on_click(event):
    #print('widget:', event.widget)
    #print('x:', event.x)
    #print('y:', event.y)
    #selected = nb.identify(event.x, event.y)
    #print('selected:', selected) # it's not usefull
    clicked_tab = Tab.tk.call(Tab._w, "identify", "tab", event.x, event.y)
    #print('clicked tab:', clicked_tab)
    active_tab = Tab.index(Tab.select())
    #print(' active tab:', active_tab)

    if clicked_tab == 2:
    	E1.focus()
    elif clicked_tab == 1:
    	RandomFlashcard()


    # if clicked_tab == active_tab:
    #     Tab.forget(clicked_tab)

def CountVocab():
	count = len(allvocabdict)
	v_countvocab.set(count)



Tab.bind('<Button-1>', on_click)
##### STATUS BAR ####
v_statusbar = StringVar()

statusbar = Label(F3, textvariable=v_statusbar, bd=1, relief=SUNKEN, anchor='w')
statusbar.pack(side=BOTTOM, fill=X)

UpdateVocab()
print('CURRENT VOCAB: ',allvocabdict)
CountVocab()

# def ChangeTab(event=None):
# 	Tab.select(F2)

# GUI.bind('<F9>',ChangeTab)


GUI.mainloop()
