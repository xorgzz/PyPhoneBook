import string
import os
from tkinter import *

mainFolder = __file__[0:-7] 

def saveContact(name, number, contact_id, popup, infoLabelPopup):
	switch = True
	allowed = list(string.ascii_letters + string.digits + " .-_")
	allowed_num = list(string.digits + " -")
	errMessage = [
	["Set the name for contact\n(only letters, numbers and \".\", \"-\", \"_\")", "red"],
	["Set the number for contact\n(9 digits, seperated with \"-\" or \" \")", "red"]]
	if len(name) != 0:
		for i in range(len(name)):
			if name[i] not in allowed:
				switch = False
				infoLabelPopup["text"], infoLabelPopup["fg"] = errMessage[0]
				break

		if switch:
			if len(disp2int(number)) == 11:
				for i in range(len(number)):
					if number[i] not in allowed_num:
						switch = False
						infoLabelPopup["text"], infoLabelPopup["fg"] = errMessage[1]
						break
				if switch:
					infoLabelPopup["text"], infoLabelPopup["fg"] = ["Saving", "green"]
					allContacts = num_read()
					allContacts[contact_id][0], allContacts[contact_id][1] = name, number
					num_overwrite(allContacts)
					updateMyList() 
					popup.destroy()
			else:
				switch=False
				infoLabelPopup["text"], infoLabelPopup["fg"] = errMessage[1]



	else: infoLabelPopup["text"], infoLabelPopup["fg"] = errMessage[0]

def deleteContact(contact_id, popup):
	allContacts = num_read()
	allContacts.pop(contact_id)
	num_overwrite(allContacts)
	updateMyList()
	popup.destroy()

def updateMyList():
	allContacts = num_read()
	mylist.delete(0,END)
	for i in range(len(allContacts)):
	   mylist.insert(i, f"{allContacts[i][0]} : {allContacts[i][1]}")

def options(event):
	selected_indices = mylist.curselection()
	selected_person = ",".join([mylist.get(i) for i in selected_indices])
	name, number, contact_id = selected_person.split(" : ")[0], selected_person.split(" : ")[1], selected_indices[0]
	popup = Toplevel(root)
	popWidth = 380
	popHeight = 240
	popup.geometry(f"{popWidth}x{popHeight}")
	popup.wm_resizable(False,False)
	popup.title(f"Contact to {name}")

	Label(popup, text="Name:", font="Consolas").place(x=10, y=10)
	Label(popup, text="Number:", font="Consolas").place(x=10, y=40)

	infoLabelPopup = Label(popup, text="", font=("Consolas", 10), fg="red")
	infoLabelPopup.place(x=popWidth/2, y=popHeight/2-35, anchor="center")
	
	new_name = Entry(popup, width=25, font="Consolas")
	new_name.place(x=90, y=10)
	new_name.insert(0,name)
	new_num = Entry(popup, width=25, font="Consolas")
	new_num.place(x=90, y=40)
	new_num.insert(0,number)

	save = Button(popup, text="OK", font="Consolas", width=10, height=1, fg="green", bg="lightgrey", command=lambda:saveContact(new_name.get(), new_num.get(), contact_id, popup, infoLabelPopup))
	cancel = Button(popup, text="Delete", font="Consolas", width=10, height=1, fg="red", bg="lightgrey", command=lambda:deleteContact(contact_id, popup))
	save.place(x=50, y=180)
	cancel.place(x=200, y=180)

def contactsPopup():
	global mylist
	popup = Toplevel(root)
	popWidth=360
	popHeight=500
	popup.geometry(f"{popWidth}x{popHeight}")
	popup.wm_resizable(False,False)
	popup.title("Your contacts")
	popup.grid_columnconfigure(0, weight=3)
	allContacts = num_read()

	scrollbar = Scrollbar(popup)
	scrollbar.pack( side = RIGHT, fill = Y )

	mylist = Listbox(popup, yscrollcommand = scrollbar.set, width=100, font="Consolas")
	mylist.bind('<Double-1>', options)
	tmpvar = mylist
	updateMyList()

	mylist.pack( side = LEFT, fill = BOTH )
	scrollbar.config( command = mylist.yview )

def num_overwrite(data):
	fp = open(f"{mainFolder}number.arch", "w")

	for i in range(len(data)):
		fp.write(f"{data[i][0]}<=>{data[i][1]}\n")

def num_read():
	fp = open(f"{mainFolder}number.arch", "r")
	allData = fp.read().split("\n")
	if allData[-1] == "":
		allData.pop()

	for i in range(len(allData)):
		allData[i] = [allData[i].split("<=>")[0], allData[i].split("<=>")[1]]

	return allData

def num_append(name, num):
	fp = open(f"{mainFolder}number.arch", "a")
	fp.write(f"{name}<=>{num}\n")
	fp.close

def deen(val):
	valInterpreter = {
		0:DISABLED,
		1:NORMAL
	}

	for i in range(len(buttList)):
		buttList[i]["state"] = valInterpreter.get(val)

def saveNewContact(name, p_number, infoLabelPopup, popup):
	switch = True
	allowed = list(string.ascii_letters + string.digits + " .-_")
	errMessage = ["Set the name for contact\n(only letters, numbers and \".\", \"-\", \"_\")", "red"]
	sucMessage = ["Saving...", "green"]
	if len(name.get()) != 0:
		contactName = name.get()
		for i in range(len(contactName)):
			if contactName[i] not in allowed:
				switch = False
				break

		if switch:
			infoLabelPopup["text"], infoLabelPopup["fg"] = sucMessage
			# deen(1)
			num_append(contactName, p_number)
			disp["text"], disp["fg"] = "Enter number", "white"
			popup.destroy()
			return
	
	infoLabelPopup["text"], infoLabelPopup["fg"] = errMessage

def savePopUp(p_number):
	global infoLabel
	if len(p_number) == 11:
		# deen(0)
		popup = Toplevel(root)
		popWidth = 380
		popHeight = 240
		popup.geometry(f"{popWidth}x{popHeight}")
		popup.wm_resizable(False,False)
		popup.title("Add contact")
		Label(popup, text="Number:", font="Consolas").place(x=10, y=10)
		Label(popup, text=p_number, font="Consolas").place(x=90, y=10)
		Label(popup, text="Name:", font="Consolas").place(x=10, y=40)

		infoLabelPopup = Label(popup, text="", font=("Consolas", 10), fg="red")
		infoLabelPopup.place(x=popWidth/2, y=popHeight/2-35, anchor="center")
		
		name = Entry(popup, width=25, font="Consolas")
		name.place(x=90, y=40)

		save = Button(popup, text="Save", font="Consolas", width=10, height=1, fg="green", bg="lightgrey", command=lambda:saveNewContact(name, p_number, infoLabelPopup, popup))
		cancel = Button(popup, text="Cancel", font="Consolas", width=10, height=1, fg="red", bg="lightgrey", command=lambda:popup.destroy())

		save.place(x=50, y=180)
		cancel.place(x=200, y=180)
	else:
		infoLabel["text"] = "Number too short !!"

def disp2int(number):
	data_out = str()
	for i in range(len(number)):
		if number[i] != " ": data_out += number[i]
		elif number[i] == " ": data_out += "-"
		else: data_out="0"
	return data_out

def press(val):
	global infoLabel
	infoLabel["text"] = ""
	if val <=9 and val >= 0:
		if disp["fg"] == "white":
			disp["text"], disp["fg"] = "", "black"
		if len(disp["text"]) < 11:
			if len(disp["text"]) == 3 or len(disp["text"]) == 7:
				disp["text"] += "-"	
			disp["text"] += str(val)
	elif val == -1 and len(disp["text"]) > 0 and disp["fg"] == "black":
		if len(disp["text"]) == 1:
			disp["text"], disp["fg"] = "Enter number", "white"
		else:
			try:
				if disp["text"][-2] == "-":
					disp["text"] = disp["text"][0:-1]
			except:
				pass
			disp["text"] = disp["text"][0:-1]

width = 600
height = 640

root = Tk()
root.title("Phone Book")
root.iconphoto(False, PhotoImage(file = mainFolder + "phone.png"))
root.geometry(f"{width}x{height}")
root.wm_resizable(False, False)

disp = Label(root, font=("Consolas", 32), text="Enter number", fg="white", bg="lightgrey", borderwidth=5, relief="solid", width=24, height=2)
disp.grid(row=0, column=0, padx=5, pady=5, columnspan=5)

# Warning / Info Label
infoLabel = Label(root, font=("Consolas", 12), text="", fg="red")
infoLabel.place(x=width/2, y=(height/2-180),anchor="center")

numpad = Frame(root, bg="lightgrey")
numpad.grid(row=1, column=1, columnspan=3, rowspan=5, pady=32)

# 1st row of main numpad
b1 = Button(numpad, font=("Consolas", 16), text="1", bg="lightgrey", borderwidth=5, relief="raised", width=6, height=2, command=lambda: press(1))
b1.grid(row=0,column=0,padx=8,pady=8)
b2 = Button(numpad, font=("Consolas", 16), text="2", bg="lightgrey", borderwidth=5, relief="raised", width=6, height=2, command=lambda: press(2))
b2.grid(row=0,column=1,padx=8,pady=8)
b3 = Button(numpad, font=("Consolas", 16), text="3", bg="lightgrey", borderwidth=5, relief="raised", width=6, height=2, command=lambda: press(3))
b3.grid(row=0,column=2,padx=8,pady=8)

# 2nd row of main numpad
b4 = Button(numpad, font=("Consolas", 16), text="4", bg="lightgrey", borderwidth=5, relief="raised", width=6, height=2, command=lambda: press(4))
b4.grid(row=1,column=0,padx=8,pady=8)
b5 = Button(numpad, font=("Consolas", 16), text="5", bg="lightgrey", borderwidth=5, relief="raised", width=6, height=2, command=lambda: press(5))
b5.grid(row=1,column=1,padx=8,pady=8)
b6 = Button(numpad, font=("Consolas", 16), text="6", bg="lightgrey", borderwidth=5, relief="raised", width=6, height=2, command=lambda: press(6))
b6.grid(row=1,column=2,padx=8,pady=8)

# 3rd row of main numpad
b7 = Button(numpad, font=("Consolas", 16), text="7", bg="lightgrey", borderwidth=5, relief="raised", width=6, height=2, command=lambda: press(7))
b7.grid(row=2,column=0,padx=5,pady=5)
b8 = Button(numpad, font=("Consolas", 16), text="8", bg="lightgrey", borderwidth=5, relief="raised", width=6, height=2, command=lambda: press(8))
b8.grid(row=2,column=1,padx=8,pady=8)
b9 = Button(numpad, font=("Consolas", 16), text="9", bg="lightgrey", borderwidth=5, relief="raised", width=6, height=2, command=lambda: press(9))
b9.grid(row=2,column=2,padx=8,pady=8)

# 4th row of main numpad
bdel = Button(numpad, font=("Consolas", 16), text="DEL", fg="red", bg="lightgrey", borderwidth=5, relief="raised", width=6, height=2, command=lambda: press(-1))
bdel.grid(row=3,column=0,padx=8,pady=8)
b0 = Button(numpad, font=("Consolas", 16), text="0", bg="lightgrey", borderwidth=5, relief="raised", width=6, height=2, command=lambda: press(0))
b0.grid(row=3,column=1,padx=8,pady=8)
bsave = Button(numpad, font=("Consolas", 16), text="SAVE", fg="green", bg="lightgrey", borderwidth=5, relief="raised", width=6, height=2, command=lambda: savePopUp(disp["text"]))
bsave.grid(row=3,column=2,padx=8,pady=8)

# 5th row of main numpad
ph = PhotoImage(file = mainFolder + "glass2.png")
bcheck = Button(numpad, font=("Consolas", 16), image=ph, bg="lightgrey", borderwidth=5, relief="raised",  compound=LEFT)
bcheck.grid(row=4,column=0,padx=8,pady=8)
bcontacts = Button(numpad, font=("Consolas", 16), text="contacts", bg="lightgrey", borderwidth=5, relief="raised", width=15, height=2, command=lambda: contactsPopup())
bcontacts.grid(row=4,column=1,padx=8,pady=8, columnspan=2)

buttList = [b1,b2,b3,b4,b5,b6,b7,b8,b9,b0,bsave,bcheck,bdel,bcontacts]

root.mainloop()
