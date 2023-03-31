"""
EasyGuiRevisionInfo = "version 0.83 2008-06-12"

EasyGui provides an easy-to-use interface for simple GUI interaction
with a user.  It does not require the programmer to know anything about
tkinter, frames, widgets, callbacks or lambda.  All GUI interactions are
invoked by simple function calls that return results.

Documentation is in an accompanying file, easygui.txt.

WARNING about using EasyGui with IDLE
=====================================

You may encounter problems using IDLE to run programs that use EasyGui. Try it
and find out.  EasyGui is a collection of Tkinter routines that run their own
event loops.  IDLE is also a Tkinter application, with its own event loop.  The
two may conflict, with the unpredictable results. If you find that you have
problems, try running your program outside of IDLE.

Note that EasyGui requires Tk release 8.0 or greater.
"""
EasyGuiRevisionInfo = "version 0.83 2008-06-12"

# see easygui.txt for revision history information

__all__ = ['ynbox'
	, 'ccbox'
	, 'boolbox'
	, 'indexbox'
	, 'msgbox'
	, 'buttonbox'
	, 'integerbox'
	, 'multenterbox'
	, 'enterbox'
	, 'choicebox'
	, 'codebox'
	, 'textbox'
	, 'diropenbox'
	, 'fileopenbox'
	, 'filesavebox'
	, 'passwordbox'
	, 'multpasswordbox'
	, 'multchoicebox'
	, 'abouteasygui'
	]

import sys, os
from tkinter import *
if TkVersion < 8.0 :
	print ("\n" * 3)
	print ("*"*75)
	print ("Running Tk version:", TkVersion)
	print ("You must be using Tk version 8.0 or greater to use EasyGui.")
	print ("Terminating.")
	print ("*"*75)
	print ("\n" * 3)
	sys.exit(0)

def dq(s): return '"%s"' % s

rootWindowPosition = "+300+200"
import string

DEFAULT_FONT_FAMILY   = ("MS", "Sans", "Serif")
MONOSPACE_FONT_FAMILY = ("Courier")
DEFAULT_FONT_SIZE     = 10
BIG_FONT_SIZE         = 12
SMALL_FONT_SIZE       =  9
CODEBOX_FONT_SIZE     =  9
TEXTBOX_FONT_SIZE     = DEFAULT_FONT_SIZE


from tkinter import filedialog

#-------------------------------------------------------------------
# various boxes built on top of the basic buttonbox
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# ynbox
#-----------------------------------------------------------------------
def ynbox(msg="Shall I continue?", title=" ", choices=("Yes", "No"), image=None):
	"""
	Display a msgbox with choices of Yes and No.

	The default is "Yes".

	The returned value is calculated this way::
		if the first choice ("Yes") is chosen, or if the dialog is cancelled:
			return 1
		else:
			return 0

	If invoked without a msg argument, displays a generic request for a confirmation
	that the user wishes to continue.  So it can be used this way::
		if ynbox(): pass # continue
		else: sys.exit(0)  # exit the program

	@arg msg: the msg to be displayed.
	@arg title: the window title
	@arg choices: a list or tuple of the choices to be displayed
	"""
	return boolbox(msg, title, choices, image=None)

#-----------------------------------------------------------------------
# ccbox
#-----------------------------------------------------------------------
def ccbox(msg="Shall I continue?", title=" ",choices=("Continue", "Cancel"), image=None):
	"""
	Display a msgbox with choices of Continue and Cancel.

	The default is "Continue".

	The returned value is calculated this way::
		if the first choice ("Continue") is chosen, or if the dialog is cancelled:
			return 1
		else:
			return 0

	If invoked without a msg argument, displays a generic request for a confirmation
	that the user wishes to continue.  So it can be used this way::

		if ccbox():
			pass # continue
		else:
			sys.exit(0)  # exit the program

	@arg msg: the msg to be displayed.
	@arg title: the window title
	@arg choices: a list or tuple of the choices to be displayed
	"""
	return boolbox(msg, title, choices, image=None)


#-----------------------------------------------------------------------
# boolbox
#-----------------------------------------------------------------------
def boolbox(msg="Shall I continue?", title=" ", choices=("Yes","No"), image=None):
	"""
	Display a boolean msgbox.

	The default is the first choice.

	The returned value is calculated this way::
		if the first choice is chosen, or if the dialog is cancelled:
			returns 1
		else:
			returns 0
	"""
	reply = buttonbox(msg=msg, choices=choices, title=title, image=None)
	if reply == choices[0]: return 1
	else: return 0


#-----------------------------------------------------------------------
# indexbox
#-----------------------------------------------------------------------
def indexbox(msg="Shall I continue?", title=" ", choices=("Yes","No"), image=None):
	"""
	Display a buttonbox with the specified choices.
	Return the index of the choice selected.
	"""
	reply = buttonbox(msg=msg, choices=choices, title=title, image=None)
	index = -1
	for choice in choices:
		index = index + 1
		if reply == choice: return index
	raise AssertionError("There is a program logic error in the EasyGui code for indexbox.")


#-----------------------------------------------------------------------
# msgbox
#-----------------------------------------------------------------------
def msgbox(msg="(Your message goes here)", title=" ", ok_button="OK",image=None):
	"""
	Display a messagebox
	"""
	if type(ok_button) != type("OK"):
		raise AssertionError("The 'ok_button' argument to msgbox must be a string.")

	return buttonbox(msg=msg, title=title, choices=[ok_button], image=image)


#-------------------------------------------------------------------
# buttonbox
#-------------------------------------------------------------------
def buttonbox(msg="",title=" ",choices=("Button1", "Button2", "Button3"), image=None):
	"""
	Display a msg, a title, and a set of buttons.
	The buttons are defined by the members of the choices list.
	Return the text of the button that the user selected.

	@arg msg: the msg to be displayed.
	@arg title: the window title
	@arg choices: a list or tuple of the choices to be displayed
	"""
	global root, __replyButtonText, __widgetTexts, buttonsFrame
	ImageErrorMsg = (
		"\n\n---------------------------------------------\n"
		"%s  NOT SHOWN\n%s")

	if image:
		image = os.path.normpath(image)
		junk,ext = os.path.splitext(image)
		if ext.lower() == ".gif":
			if os.path.exists(image):
				pass
			else:
				msg += ImageErrorMsg % (image, "Image file not found.")
				image = None
		else:
			msg += ImageErrorMsg % (image, "Image file is not a .gif file.")
			image = None

	# Initialize __replyButtonText to the first choice.
	# This is what will be used if the window is closed by the close button.
	__replyButtonText = choices[0]

	root = Tk()
	root.protocol('WM_DELETE_WINDOW', denyWindowManagerClose )
	root.title(title)
	root.iconname('Dialog')
	root.geometry(rootWindowPosition)
	root.minsize(400, 100)

	# ------------- define the frames --------------------------------------------
	messageFrame = Frame(root)
	messageFrame.pack(side=TOP, fill=BOTH)

	if image:
		imageFrame = Frame(root)
		imageFrame.pack(side=BOTTOM, fill=BOTH)

	buttonsFrame = Frame(root)
	buttonsFrame.pack(side=BOTTOM, fill=BOTH)

	# -------------------- place the widgets in the frames -----------------------
	messageWidget = Message(messageFrame, text=msg, width=400)
	messageWidget.configure(font=(DEFAULT_FONT_FAMILY,DEFAULT_FONT_SIZE))
	messageWidget.pack(side=TOP, expand=YES, fill=X, padx='3m', pady='3m')

	if image:
		image = PhotoImage(file=image)
		label = Label(image=image)
		label.image = image # keep a reference!
		label.pack(side=TOP, expand=YES, fill=X, padx='1m', pady='1m')

	__put_buttons_in_buttonframe(choices)

	# -------------- the action begins -----------
	# put the focus on the first button
	__firstWidget.focus_force()
	root.mainloop()
	root.destroy()
	return __replyButtonText


#-------------------------------------------------------------------
# integerbox
#-------------------------------------------------------------------
def integerbox(msg="", title=" ", default="", argLowerBound=0, argUpperBound=99):
	"""
	Show a box in which a user can enter an integer.

	In addition to arguments for msg and title, this function accepts
	integer arguments for default_value, lowerbound, and upperbound.

	The default_value argument may be None.

	When the user enters some text, the text is checked to verify
	that it can be converted to an integer between the lowerbound and upperbound.

	If it can be, the integer (not the text) is returned.

	If it cannot, then an error msg is displayed, and the integerbox is
	redisplayed.

	If the user cancels the operation, None is returned.
	"""
	if default != "":
		if type(default) != type(1):
			raise AssertionError(
				"integerbox received a non-integer value for "
				+ "default of " + dq(str(default)) , "Error")

	if type(argLowerBound) != type(1):
		raise AssertionError(
			"integerbox received a non-integer value for "
			+ "argLowerBound of " + dq(str(argLowerBound)) , "Error")

	if type(argUpperBound) != type(1):
		raise AssertionError(
			"integerbox received a non-integer value for "
			+ "argUpperBound of " + dq(str(argUpperBound)) , "Error")

	if msg == "":
		msg = ("Enter an integer between " + str(argLowerBound)
			+ " and "
			+ str(argUpperBound)
			)

	while 1:
		reply = enterbox(msg, title, str(default))
		if reply == None: return None

		try:
			reply = int(reply)
		except:
			msgbox ("The value that you entered:\n\t%s\nis not an integer." % dq(str(reply))
					, "Error")
			continue

		if reply < argLowerBound:
			msgbox ("The value that you entered is less than the lower bound of "
				+ str(argLowerBound) + ".", "Error")
			continue

		if reply > argUpperBound:
			msgbox ("The value that you entered is greater than the upper bound of "
				+ str(argUpperBound) + ".", "Error")
			continue

		# reply has passed all validation checks.
		# It is an integer between the specified bounds.
		return reply

#-------------------------------------------------------------------
# multenterbox
#-------------------------------------------------------------------
def multenterbox(msg="Fill in values for the fields.", title=" "
	, fields  = (), values = () ):
	"""
Show screen with multiple data entry fields.

If there are fewer values than names, the list of values is padded with
empty strings until the number of values is the same as the number of names.

If there are more values than names, the list of values
is truncated so that there are as many values as names.

Returns a list of the values of the fields,
or None if the user cancels the operation.

Here is some example code, that shows how values returned from
multenterbox can be checked for validity before they are accepted::
    ----------------------------------------------------------------------
    msg = "Enter your personal information"
    title = "Credit Card Application"
    fieldNames = ["Name","Street Address","City","State","ZipCode"]
    fieldValues = []  # we start with blanks for the values
    fieldValues = multenterbox(msg,title, fieldNames)

    # make sure that none of the fields was left blank
    while 1:
        if fieldValues == None: break
        errmsg = ""
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
        if errmsg == "": break # no problems found
        fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)

    print "Reply was:", fieldValues
    ----------------------------------------------------------------------

@arg msg: the msg to be displayed.
@arg title: the window title
@arg fields: a list of fieldnames.
@arg values:  a list of field values
"""
	return __multfillablebox(msg,title,fields,values,None)


#-----------------------------------------------------------------------
# multpasswordbox
#-----------------------------------------------------------------------
def multpasswordbox(msg="Fill in values for the fields.", title=" "
	, fields  = (), values = ()  ):
	"""
Same interface as multenterbox.  But in multpassword box,
the last of the fields is assumed to be a password, and
is masked with asterisks.

Here is some example code, that shows how values returned from
multpasswordbox can be checked for validity before they are accepted::
----------------------------------------------------------------------
msg = "Enter logon information"
title = "Demo of multpasswordbox"
fieldNames = ["Server ID", "User ID", "Password"]
fieldValues = []  # we start with blanks for the values
fieldValues = multpasswordbox(msg,title, fieldNames)

# make sure that none of the fields was left blank
while 1:
    if fieldValues == None: break
    errmsg = ""
    for i in range(len(fieldNames)):
        if fieldValues[i].strip() == "":
            errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
    if errmsg == "": break # no problems found
    fieldValues = multpasswordbox(errmsg, title, fieldNames, fieldValues)

print "Reply was:", fieldValues
----------------------------------------------------------------------
"""
	return __multfillablebox(msg,title,fields,values,"*")

#-----------------------------------------------------------------------
# __multfillablebox
#-----------------------------------------------------------------------
def __multfillablebox(msg="Fill in values for the fields.", title=" "
	, fields=(), values=(), argMaskCharacter = None ):

	global root, __multenterboxText, __multenterboxDefaultText, cancelButton, entryWidget, okButton

	choices = ["OK", "Cancel"]
	if len(fields) == 0: return None

	fields = list(fields[:])  # convert possible tuples to a list
	values = list(values[:])  # convert possible tuples to a list

	if   len(values) == len(fields): pass
	elif len(values) >  len(fields):
		fields = fields[0:len(values)]
	else:
		while len(values) < len(fields):
			values.append("")

	root = Tk()
	root.protocol('WM_DELETE_WINDOW', denyWindowManagerClose )
	root.title(title)
	root.iconname('Dialog')
	root.geometry(rootWindowPosition)
	root.bind("<Escape>", __multenterboxCancel)

	# -------------------- put subframes in the root --------------------
	messageFrame = Frame(root)
	messageFrame.pack(side=TOP, fill=BOTH)

	#-------------------- the msg widget ----------------------------
	messageWidget = Message(messageFrame, width="4.5i", text=msg)
	messageWidget.configure(font=(DEFAULT_FONT_FAMILY,DEFAULT_FONT_SIZE))
	messageWidget.pack(side=RIGHT, expand=1, fill=BOTH, padx='3m', pady='3m')

	global entryWidgets
	entryWidgets = []

	lastWidgetIndex = len(fields) - 1

	for widgetIndex in range(len(fields)):
		argFieldName  = fields[widgetIndex]
		argFieldValue = values[widgetIndex]
		entryFrame = Frame(root)
		entryFrame.pack(side=TOP, fill=BOTH)

		# --------- entryWidget ----------------------------------------------
		labelWidget = Label(entryFrame, text=argFieldName)
		labelWidget.pack(side=LEFT)

		entryWidgets.append(Entry(entryFrame, width=40))
		entryWidgets[widgetIndex].configure(font=(DEFAULT_FONT_FAMILY,BIG_FONT_SIZE))
		entryWidgets[widgetIndex].pack(side=RIGHT, padx="3m")
		entryWidgets[widgetIndex].bind("<Return>", __multenterboxGetText)
		entryWidgets[widgetIndex].bind("<Escape>", __multenterboxCancel)

		# for the last entryWidget, if this is a multpasswordbox,
		# show the contents as just asterisks
		if widgetIndex == lastWidgetIndex:
			if argMaskCharacter:
				entryWidgets[widgetIndex].configure(show=argMaskCharacter)

		# put text into the entryWidget
		entryWidgets[widgetIndex].insert(0,argFieldValue)
		widgetIndex += 1

	# ------------------ ok button -------------------------------

	buttonsFrame = Frame(root)
	buttonsFrame.pack(side=BOTTOM, fill=BOTH)


	okButton = Button(buttonsFrame, takefocus=1, text="OK")
	okButton.pack(expand=1, side=LEFT, padx='3m', pady='3m', ipadx='2m', ipady='1m')
	okButton.bind("<Return>"  , __multenterboxGetText)
	okButton.bind("<Button-1>", __multenterboxGetText)

	# ------------------ cancel button -------------------------------
	cancelButton = Button(buttonsFrame, takefocus=1, text="Cancel")
	cancelButton.pack(expand=1, side=RIGHT, padx='3m', pady='3m', ipadx='2m', ipady='1m')
	cancelButton.bind("<Return>"  , __multenterboxCancel)
	cancelButton.bind("<Button-1>", __multenterboxCancel)

	# ------------------- time for action! -----------------
	entryWidgets[0].focus_force()    # put the focus on the entryWidget
	root.mainloop()  # run it!

	# -------- after the run has completed ----------------------------------
	root.destroy()  # button_click didn't destroy root, so we do it now
	return __multenterboxText

#-----------------------------------------------------------------------
# __multenterboxGetText
#-----------------------------------------------------------------------
def __multenterboxGetText(event):
	global root, __multenterboxText, entryWidget
	__multenterboxText = []
	global entryWidgets
	for entryWidget in entryWidgets:
		__multenterboxText.append(entryWidget.get())

	root.quit()

def __multenterboxCancel(event):
	global root,  __multenterboxDefaultText, __multenterboxText
	__multenterboxText = None

	root.quit()


#-------------------------------------------------------------------
# enterbox
#-------------------------------------------------------------------
def enterbox(msg="Enter something.", title=" ", default="",strip=True):
	"""
	Show a box in which a user can enter some text.

	You may optionally specify some default text, which will appear in the
	enterbox when it is displayed.

	Returns the text that the user entered, or None if he cancels the operation.

	By default, enterbox strips its result (i.e. removes leading and trailing
	whitespace).  (If you want it not to strip, use keyword argument: strip=False.)
	This makes it easier to test the results of the call::

		reply = enterbox(....)
		if reply:
			...
		else:
			...
	"""
	result = __fillablebox(msg, title, default=default, argMaskCharacter=None)
	if result and strip:
		result = result.strip()
	return result


def passwordbox(msg="Enter your password.", title=" ", default=""):
	"""
	Show a box in which a user can enter a password.
	The text is masked with asterisks, so the password is not displayed.
	Returns the text that the user entered, or None if he cancels the operation.
	"""
	return __fillablebox(msg, title, default, "*")


def __fillablebox(msg, title="", default="", argMaskCharacter=None):
	"""
	Show a box in which a user can enter some text.
	You may optionally specify some default text, which will appear in the
	enterbox when it is displayed.
	Returns the text that the user entered, or None if he cancels the operation.
	"""

	global root, __enterboxText, __enterboxDefaultText, cancelButton, entryWidget, okButton

	if title == None: title == ""
	if default == None: default = ""
	__enterboxDefaultText = default
	__enterboxText        = __enterboxDefaultText
	choices = ["OK", "Cancel"]

	root = Tk()
	root.protocol('WM_DELETE_WINDOW', denyWindowManagerClose )
	root.title(title)
	root.iconname('Dialog')
	root.geometry(rootWindowPosition)
	root.bind("<Escape>", __enterboxCancel)

	# -------------------- put subframes in the root --------------------
	messageFrame = Frame(root)
	messageFrame.pack(side=TOP, fill=BOTH)

	entryFrame = Frame(root)
	entryFrame.pack(side=TOP, fill=BOTH)

	buttonsFrame = Frame(root)
	buttonsFrame.pack(side=BOTTOM, fill=BOTH)

	#-------------------- the msg widget ----------------------------
	messageWidget = Message(messageFrame, width="4.5i", text=msg)
	messageWidget.configure(font=(DEFAULT_FONT_FAMILY,DEFAULT_FONT_SIZE))
	messageWidget.pack(side=RIGHT, expand=1, fill=BOTH, padx='3m', pady='3m')

	# --------- entryWidget ----------------------------------------------
	entryWidget = Entry(entryFrame, width=40)
	entryWidget.configure(font=(DEFAULT_FONT_FAMILY,BIG_FONT_SIZE))
	if argMaskCharacter:
		entryWidget.configure(show=argMaskCharacter)
	entryWidget.pack(side=LEFT, padx="3m")
	entryWidget.bind("<Return>", __enterboxGetText)
	entryWidget.bind("<Escape>", __enterboxCancel)
	# put text into the entryWidget
	entryWidget.insert(0,__enterboxDefaultText)

	# ------------------ ok button -------------------------------
	okButton = Button(buttonsFrame, takefocus=1, text="OK")
	okButton.pack(expand=1, side=LEFT, padx='3m', pady='3m', ipadx='2m', ipady='1m')
	okButton.bind("<Return>"  , __enterboxGetText)
	okButton.bind("<Button-1>", __enterboxGetText)

	''' dead code ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# ------------------ (possible) restore button -------------------------------
	if default != None:
		# make a button to restore the default text
		restoreButton = Button(buttonsFrame, takefocus=1, text="Restore default")
		restoreButton.pack(expand=1, side=LEFT, padx='3m', pady='3m', ipadx='2m', ipady='1m')
		restoreButton.bind("<Return>"  , __enterboxRestore)
		restoreButton.bind("<Button-1>", __enterboxRestore)
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ dead code '''

	# ------------------ cancel button -------------------------------
	cancelButton = Button(buttonsFrame, takefocus=1, text="Cancel")
	cancelButton.pack(expand=1, side=RIGHT, padx='3m', pady='3m', ipadx='2m', ipady='1m')
	cancelButton.bind("<Return>"  , __enterboxCancel)
	cancelButton.bind("<Button-1>", __enterboxCancel)

	# ------------------- time for action! -----------------
	entryWidget.focus_force()    # put the focus on the entryWidget
	root.mainloop()  # run it!

	# -------- after the run has completed ----------------------------------
	root.destroy()  # button_click didn't destroy root, so we do it now
	return __enterboxText



def __enterboxGetText(event):
	global root, __enterboxText, entryWidget
	__enterboxText = entryWidget.get()

	root.quit()

def __enterboxRestore(event):
	global root, __enterboxText, entryWidget
	entryWidget.delete(0,len(entryWidget.get()))
	entryWidget.insert(0, __enterboxDefaultText)

def __enterboxCancel(event):
	global root,  __enterboxDefaultText, __enterboxText
	__enterboxText = None

	root.quit()

def denyWindowManagerClose():
	""" don't allow WindowManager close
	"""
	x = Tk()
	x.withdraw()
	x.bell()
	x.destroy()



#-------------------------------------------------------------------
# multchoicebox
#-------------------------------------------------------------------
def multchoicebox(msg="Pick as many items as you like.",title=" ",choices=(), **kwargs):
	"""
	Present the user with a list of choices.
	allow him to select multiple items and return them in a list.
	if the user doesn't choose anything from the list, return the empty list.
	return None if he cancelled selection.

	@arg msg: the msg to be displayed.
	@arg title: the window title
	@arg choices: a list or tuple of the choices to be displayed
	"""
	if len(choices) == 0: choices = ["Program logic error - no choices were specified."]

	global __choiceboxMultipleSelect
	__choiceboxMultipleSelect = 1
	return __choicebox(msg, title, choices)


#-----------------------------------------------------------------------
# choicebox
#-----------------------------------------------------------------------
def choicebox(msg="Pick something.",title=" ",  choices=(),  buttons=()   ):
	"""
	Present the user with a list of choices.
	return the choice that he selects.
	return None if he cancels the selection selection.

	@arg msg: the msg to be displayed.
	@arg title: the window title
	@arg choices: a list or tuple of the choices to be displayed
	"""
	if len(choices) == 0: choices = ["Program logic error - no choices were specified."]

	global __choiceboxMultipleSelect
	__choiceboxMultipleSelect = 0
	return __choicebox(msg,title,choices,buttons)


#-----------------------------------------------------------------------
# __choicebox
#-----------------------------------------------------------------------
def __choicebox(msg, title, choices,  buttons=() ):
	"""
	internal routine to support choicebox() and multchoicebox()
	"""
	global root, __choiceboxResults, choiceboxWidget, defaultText
	global choiceboxWidget, choiceboxChoices
	#-------------------------------------------------------------------
	# If choices is a tuple, we make it a list so we can sort it.
	# If choices is already a list, we make a new list, so that when
	# we sort the choices, we don't affect the list object that we
	# were given.
	#-------------------------------------------------------------------
	choices = list(choices[:])
	if len(choices) == 0: choices = ["Program logic error - no choices were specified."]
	defaultButtons = ["OK", "Cancel"]

	# make sure all choices are strings
	for index in range(len(choices)):
		choices[index] = str(choices[index])

	if buttons:
		if type(buttons) == type("abc"): # user sent a string
			choiceboxButtons = [buttons]
		else: # we assume user sent in a list or tuple of strings
			choiceboxButtons = buttons
	else:
		choiceboxButtons = defaultButtons

	lines_to_show = min(len(choices), 20)
	lines_to_show = 20

	if title == None: title = ""

	# Initialize __choiceboxResults
	# This is the value that will be returned if the user clicks the close icon
	__choiceboxResults = None

	root = Tk()
	root.protocol('WM_DELETE_WINDOW', denyWindowManagerClose )
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()
	root_width = int((screen_width * 0.8))
	root_height = int((screen_height * 0.5))
	root_xpos = int((screen_width * 0.1))
	root_ypos = int((screen_height * 0.05))

	root.title(title)
	root.iconname('Dialog')
	rootWindowPosition = "+0+0"
	root.geometry(rootWindowPosition)
	root.expand=NO
	root.minsize(root_width, root_height)
	rootWindowPosition = "+" + str(root_xpos) + "+" + str(root_ypos)
	root.geometry(rootWindowPosition)

	# ---------------- put the frames in the window -----------------------------------------
	message_and_buttonsFrame = Frame(root)
	message_and_buttonsFrame.pack(side=TOP, fill=X, expand=NO)

	messageFrame = Frame(message_and_buttonsFrame)
	messageFrame.pack(side=LEFT, fill=X, expand=YES)
	#messageFrame.pack(side=TOP, fill=X, expand=YES)

	buttonsFrame = Frame(message_and_buttonsFrame)
	buttonsFrame.pack(side=RIGHT, expand=NO, pady=0)
	#buttonsFrame.pack(side=TOP, expand=YES, pady=0)

	choiceboxFrame = Frame(root)
	choiceboxFrame.pack(side=BOTTOM, fill=BOTH, expand=YES)

	# -------------------------- put the widgets in the frames ------------------------------

	# ---------- put a msg widget in the msg frame-------------------
	messageWidget = Message(messageFrame, anchor=NW, text=msg, width=int(root_width * 0.9))
	messageWidget.configure(font=(DEFAULT_FONT_FAMILY,DEFAULT_FONT_SIZE))
	messageWidget.pack(side=LEFT, expand=YES, fill=BOTH, padx='1m', pady='1m')

	# --------  put the choiceboxWidget in the choiceboxFrame ---------------------------
	choiceboxWidget = Listbox(choiceboxFrame
		, height=lines_to_show
		, borderwidth="1m"
		, relief="flat"
		, bg="white"
		)

	if __choiceboxMultipleSelect:
		choiceboxWidget.configure(selectmode=MULTIPLE)

	choiceboxWidget.configure(font=(DEFAULT_FONT_FAMILY,DEFAULT_FONT_SIZE))

	# add a vertical scrollbar to the frame
	rightScrollbar = Scrollbar(choiceboxFrame, orient=VERTICAL, command=choiceboxWidget.yview)
	choiceboxWidget.configure(yscrollcommand = rightScrollbar.set)

	# add a horizontal scrollbar to the frame
	bottomScrollbar = Scrollbar(choiceboxFrame, orient=HORIZONTAL, command=choiceboxWidget.xview)
	choiceboxWidget.configure(xscrollcommand = bottomScrollbar.set)

	# pack the Listbox and the scrollbars.  Note that although we must define
	# the textbox first, we must pack it last, so that the bottomScrollbar will
	# be located properly.

	bottomScrollbar.pack(side=BOTTOM, fill = X)
	rightScrollbar.pack(side=RIGHT, fill = Y)

	choiceboxWidget.pack(side=LEFT, padx="1m", pady="1m", expand=YES, fill=BOTH)

	#---------------------------------------------------
	# sort the choices
	# eliminate duplicates
	# put the choices into the choiceboxWidget
	#---------------------------------------------------
	for index in range(len(choices)):
		choices[index] == str(choices[index])

	choices.sort( lambda x,y: cmp(x.lower(),    y.lower())) # case-insensitive sort
	lastInserted = None
	choiceboxChoices = []
	for choice in choices:
		if choice == lastInserted: pass
		else:
			choiceboxWidget.insert(END, choice)
			choiceboxChoices.append(choice)
			lastInserted = choice

	root.bind('<Any-Key>', KeyboardListener)

	# put the buttons in the buttonsFrame
	if len(choices) > 0:
		okButton = Button(buttonsFrame, takefocus=YES, text="OK", height=1, width=6)
		okButton.pack(expand=NO, side=TOP,  padx='2m', pady='1m', ipady="1m", ipadx="2m")
		okButton.bind("<Return>", __choiceboxGetChoice)
		okButton.bind("<Button-1>",__choiceboxGetChoice)

		# now bind the keyboard events
		choiceboxWidget.bind("<Return>", __choiceboxGetChoice)
		choiceboxWidget.bind("<Double-Button-1>", __choiceboxGetChoice)
	else:
		# now bind the keyboard events
		choiceboxWidget.bind("<Return>", __choiceboxCancel)
		choiceboxWidget.bind("<Double-Button-1>", __choiceboxCancel)

	cancelButton = Button(buttonsFrame, takefocus=YES, text="Cancel", height=1, width=6)
	cancelButton.pack(expand=NO, side=BOTTOM, padx='2m', pady='1m', ipady="1m", ipadx="2m")
	cancelButton.bind("<Return>", __choiceboxCancel)
	cancelButton.bind("<Button-1>", __choiceboxCancel)

	# add special buttons for multiple select features
	if len(choices) > 0 and __choiceboxMultipleSelect:
		selectionButtonsFrame = Frame(messageFrame)
		selectionButtonsFrame.pack(side=RIGHT, fill=Y, expand=NO)

		selectAllButton = Button(selectionButtonsFrame, text="Select All", height=1, width=6)
		selectAllButton.bind("<Button-1>",__choiceboxSelectAll)
		selectAllButton.pack(expand=NO, side=TOP,  padx='2m', pady='1m', ipady="1m", ipadx="2m")

		clearAllButton = Button(selectionButtonsFrame, text="Clear All", height=1, width=6)
		clearAllButton.bind("<Button-1>",__choiceboxClearAll)
		clearAllButton.pack(expand=NO, side=TOP,  padx='2m', pady='1m', ipady="1m", ipadx="2m")


	# -------------------- bind some keyboard events ----------------------------
	root.bind("<Escape>", __choiceboxCancel)

	# --------------------- the action begins -----------------------------------
	# put the focus on the choiceboxWidget, and the select highlight on the first item
	choiceboxWidget.select_set(0)
	choiceboxWidget.focus_force()

	# --- run it! -----
	root.mainloop()

	root.destroy()
	return __choiceboxResults


def __choiceboxGetChoice(event):
	global root, __choiceboxResults, choiceboxWidget

	if __choiceboxMultipleSelect:
		__choiceboxResults = [choiceboxWidget.get(index) for index in choiceboxWidget.curselection()]

	else:
		choice_index = choiceboxWidget.curselection()
		__choiceboxResults = choiceboxWidget.get(choice_index)

	# print "Debugging> mouse-event=", event, " event.type=", event.type
	# print "Debugging> choice =", choice_index, __choiceboxResults
	root.quit()


def __choiceboxSelectAll(event):
	global choiceboxWidget, choiceboxChoices
	choiceboxWidget.selection_set(0, len(choiceboxChoices)-1)

def __choiceboxClearAll(event):
	global choiceboxWidget, choiceboxChoices
	choiceboxWidget.selection_clear(0, len(choiceboxChoices)-1)



def __choiceboxCancel(event):
	global root, __choiceboxResults

	__choiceboxResults = None
	root.quit()


def KeyboardListener(event):
	global choiceboxChoices, choiceboxWidget
	key = event.keysym
	if len(key) <= 1:
		if key in string.printable:
			# Find the key in the list.
			# before we clear the list, remember the selected member
			try:
				start_n = int(choiceboxWidget.curselection()[0])
			except IndexError:
				start_n = -1

			## clear the selection.
			choiceboxWidget.selection_clear(0, 'end')

			## start from previous selection +1
			for n in range(start_n+1, len(choiceboxChoices)):
				item = choiceboxChoices[n]
				if item[0].lower() == key.lower():
					choiceboxWidget.selection_set(first=n)
					choiceboxWidget.see(n)
					return
			else:
				# has not found it so loop from top
				for n in range(len(choiceboxChoices)):
					item = choiceboxChoices[n]
					if item[0].lower() == key.lower():
						choiceboxWidget.selection_set(first = n)
						choiceboxWidget.see(n)
						return

				# nothing matched -- we'll look for the next logical choice
				for n in range(len(choiceboxChoices)):
					item = choiceboxChoices[n]
					if item[0].lower() > key.lower():
						if n > 0:
							choiceboxWidget.selection_set(first = (n-1))
						else:
							choiceboxWidget.selection_set(first = 0)
						choiceboxWidget.see(n)
						return

				# still no match (nothing was greater than the key)
				# we set the selection to the first item in the list
				lastIndex = len(choiceboxChoices)-1
				choiceboxWidget.selection_set(first = lastIndex)
				choiceboxWidget.see(lastIndex)
				return

#-------------------------------------------------------------------
# codebox
#-------------------------------------------------------------------

def codebox(msg="", title=" ", text=""):
	"""
	Display some text in a monospaced font, with no line wrapping.
	This function is suitable for displaying code and text that is
	formatted using spaces.

	The text parameter should be a string, or a list or tuple of lines to be
	displayed in the textbox.
	"""
	textbox(msg, title, text, codebox=1 )

#-------------------------------------------------------------------
# textbox
#-------------------------------------------------------------------
def textbox(msg="", title=" ", text="", codebox=0):
	"""
	Display some text in a proportional font with line wrapping at word breaks.
	This function is suitable for displaying general written text.

	The text parameter should be a string, or a list or tuple of lines to be
	displayed in the textbox.
	"""

	if msg == None: msg = ""
	if title == None: title = ""

	global root, __replyButtonText, __widgetTexts, buttonsFrame
	choices = ["0K"]
	__replyButtonText = choices[0]


	root = Tk()

	root.protocol('WM_DELETE_WINDOW', denyWindowManagerClose )

	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()
	root_width = int((screen_width * 0.8))
	root_height = int((screen_height * 0.5))
	root_xpos = int((screen_width * 0.1))
	root_ypos = int((screen_height * 0.05))

	root.title(title)
	root.iconname('Dialog')
	rootWindowPosition = "+0+0"
	root.geometry(rootWindowPosition)
	root.expand=NO
	root.minsize(root_width, root_height)
	rootWindowPosition = "+" + str(root_xpos) + "+" + str(root_ypos)
	root.geometry(rootWindowPosition)


	mainframe = Frame(root)
	mainframe.pack(side=TOP, fill=BOTH, expand=YES)

	# ----  put frames in the window -----------------------------------
	# we pack the textboxFrame first, so it will expand first
	textboxFrame = Frame(mainframe, borderwidth=3)
	textboxFrame.pack(side=BOTTOM , fill=BOTH, expand=YES)

	message_and_buttonsFrame = Frame(mainframe)
	message_and_buttonsFrame.pack(side=TOP, fill=X, expand=NO)

	messageFrame = Frame(message_and_buttonsFrame)
	messageFrame.pack(side=LEFT, fill=X, expand=YES)

	buttonsFrame = Frame(message_and_buttonsFrame)
	buttonsFrame.pack(side=RIGHT, expand=NO)

	# -------------------- put widgets in the frames --------------------

	# put a textbox in the top frame
	if codebox:
		character_width = int((root_width * 0.6) / CODEBOX_FONT_SIZE)
		textbox = Text(textboxFrame,height=25,width=character_width, padx="2m", pady="1m")
		textbox.configure(wrap=NONE)
		textbox.configure(font=(MONOSPACE_FONT_FAMILY, CODEBOX_FONT_SIZE))

	else:
		character_width = int((root_width * 0.6) / SMALL_FONT_SIZE)
		textbox = Text(
			textboxFrame
			, height=25
			, width=character_width
			, padx="2m"
			, pady="1m"
			)
		textbox.configure(wrap=WORD)
		textbox.configure(font=(DEFAULT_FONT_FAMILY,TEXTBOX_FONT_SIZE))


	# some simple keybindings for scrolling
	mainframe.bind("<Next>" , textbox.yview_scroll( 1,PAGES))
	mainframe.bind("<Prior>", textbox.yview_scroll(-1,PAGES))

	mainframe.bind("<Right>", textbox.xview_scroll( 1,PAGES))
	mainframe.bind("<Left>" , textbox.xview_scroll(-1,PAGES))

	mainframe.bind("<Down>", textbox.yview_scroll( 1,UNITS))
	mainframe.bind("<Up>"  , textbox.yview_scroll(-1,UNITS))


	# add a vertical scrollbar to the frame
	rightScrollbar = Scrollbar(textboxFrame, orient=VERTICAL, command=textbox.yview)
	textbox.configure(yscrollcommand = rightScrollbar.set)

	# add a horizontal scrollbar to the frame
	bottomScrollbar = Scrollbar(textboxFrame, orient=HORIZONTAL, command=textbox.xview)
	textbox.configure(xscrollcommand = bottomScrollbar.set)

	# pack the textbox and the scrollbars.  Note that although we must define
	# the textbox first, we must pack it last, so that the bottomScrollbar will
	# be located properly.

	# Note that we need a bottom scrollbar only for code.
	# Text will be displayed with wordwrap, so we don't need to have a horizontal
	# scroll for it.
	if codebox:
		bottomScrollbar.pack(side=BOTTOM, fill=X)
	rightScrollbar.pack(side=RIGHT, fill=Y)

	textbox.pack(side=LEFT, fill=BOTH, expand=YES)


	# ---------- put a msg widget in the msg frame-------------------
	messageWidget = Message(messageFrame, anchor=NW, text=msg, width=int(root_width * 0.9))
	messageWidget.configure(font=(DEFAULT_FONT_FAMILY,DEFAULT_FONT_SIZE))
	messageWidget.pack(side=LEFT, expand=YES, fill=BOTH, padx='1m', pady='1m')

	# put the buttons in the buttonsFrame
	okButton = Button(buttonsFrame, takefocus=YES, text="OK", height=1, width=6)
	okButton.pack(expand=NO, side=TOP,  padx='2m', pady='1m', ipady="1m", ipadx="2m")
	okButton.bind("<Return>"  , __textboxOK)
	okButton.bind("<Button-1>", __textboxOK)
	okButton.bind("<Escape>"  , __textboxOK)


	# ----------------- the action begins ----------------------------------------
	try:
		# load the text into the textbox
		if type(text) == type("abc"): pass
		else:
			try:
				text = "".join(text)  # convert a list or a tuple to a string
			except:
				msgbox("Exception when trying to convert "+ str(type(text)) + " to text in textbox")
				sys.exit(16)
		textbox.insert(END,text, "normal")

		# disable the textbox, so the text cannot be edited
		textbox.configure(state=DISABLED)
	except:
		msgbox("Exception when trying to load the textbox.")
		sys.exit(16)

	try:
		okButton.focus_force()
	except:
		msgbox("Exception when trying to put focus on okButton.")
		sys.exit(16)

	root.mainloop()
	root.destroy()
	return __replyButtonText

#-------------------------------------------------------------------
# __textboxOK
#-------------------------------------------------------------------
def __textboxOK(event):
	global root

	root.quit()



#-------------------------------------------------------------------
# diropenbox
#-------------------------------------------------------------------
def diropenbox(msg=None, title=None, default=None):
	"""
	A dialog to get a directory name.
	Note that the msg argument, if specified, is ignored.

	Returns the name of a directory, or None if user chose to cancel.

	If the "default" argument specifies a directory name,
	and that directory exists,
	then the dialog box will start with that directory.
	"""
	root = Tk()
	root.withdraw()
	if default == None:
		f = tkFileDialog.askdirectory(parent=root, title=title)
	else:
		f = tkFileDialog.askdirectory(parent=root, title=title, initialdir=default)
	if not f: return None
	return os.path.normpath(f)


#-------------------------------------------------------------------
# fileopenbox
#-------------------------------------------------------------------
def fileopenbox(msg=None, title=None, default=None):
	"""
	A dialog to get a file name.
	Returns the name of a file, or None if user chose to cancel.

	If the "default" argument specifies a file name,
	then the dialog box will start with that file.
	"""
	root = Tk()
	root.withdraw()
	f = tkFileDialog.askopenfilename(parent=root,title=title, initialfile=default)
	if not f: return None
	return os.path.normpath(f)


#-------------------------------------------------------------------
# filesavebox
#-------------------------------------------------------------------
def filesavebox(msg=None, title=None, default=None):
	"""
	A file to get the name of a file to save.
	Returns the name of a file, or None if user chose to cancel.

	If the "default" argument specifies a file name,
	then the dialog box will start with that file.
	"""
	root = Tk()
	root.withdraw()
	f = tkFileDialog.asksaveasfilename(parent=root, title=title, initialfile=default)
	if not f: return None
	return os.path.normpath(f)


#-------------------------------------------------------------------
# utility routines
#-------------------------------------------------------------------
# These routines are used by several other functions in the EasyGui module.

def __buttonEvent(event):
	"""
	Handle an event that is generated by a person clicking a button.
	"""
	global  root, __widgetTexts, __replyButtonText
	__replyButtonText = __widgetTexts[event.widget]
	root.quit() # quit the main loop


def __put_buttons_in_buttonframe(choices):
	"""Put the buttons in the buttons frame
	"""
	global __widgetTexts, __firstWidget, buttonsFrame

	__widgetTexts = {}
	i = 0

	for buttonText in choices:
		tempButton = Button(buttonsFrame, takefocus=1, text=buttonText)
		tempButton.pack(expand=YES, side=LEFT, padx='1m', pady='1m', ipadx='2m', ipady='1m')

		# remember the text associated with this widget
		__widgetTexts[tempButton] = buttonText

		# remember the first widget, so we can put the focus there
		if i == 0:
			__firstWidget = tempButton
			i = 1

		# bind the keyboard events to the widget
		tempButton.bind("<Return>", __buttonEvent)
		tempButton.bind("<Button-1>", __buttonEvent)


#-----------------------------------------------------------------------
#
# test/demo easygui
#
#-----------------------------------------------------------------------
def _test():
	# simple way to clear the console
	print ("\n" * 100)
	# START DEMONSTRATION DATA ===================================================
	choices_abc = ["This is choice 1", "And this is choice 2"]
	msg = "Pick one! This is a huge choice, and you've got to make the right one " \
		"or you will surely mess up the rest of your life, and the lives of your " \
		"friends and neighbors!"
	title = ""

	# ============================= define a code snippet =========================
	code_snippet = ("dafsdfa dasflkj pp[oadsij asdfp;ij asdfpjkop asdfpok asdfpok asdfpok"*3) +"\n"+\
"""# here is some dummy Python code
for someItem in myListOfStuff:
	do something(someItem)
	do something()
	do something()
	if somethingElse(someItem):
		doSomethingEvenMoreInteresting()

"""*16
	#======================== end of code snippet ==============================

	#================================= some text ===========================
	text_snippet = ((\
"""It was the best of times, and it was the worst of times.  The rich ate cake, and the poor had cake recommended to them, but wished only for enough cash to buy bread.  The time was ripe for revolution! """ \
*5)+"\n\n")*10

	#===========================end of text ================================

	intro_message = ("Pick the kind of box that you wish to demo.\n\n"
	 + "In EasyGui, all GUI interactions are invoked by simple function calls.\n\n" +
	"EasyGui is different from other GUIs in that it is NOT event-driven.  It allows" +
	" you to program in a traditional linear fashion, and to put up dialogs for simple" +
	" input and output when you need to. If you are new to the event-driven paradigm" +
	" for GUIs, EasyGui will allow you to be productive with very basic tasks" +
	" immediately. Later, if you wish to make the transition to an event-driven GUI" +
	" paradigm, you can move to an event-driven style with a more powerful GUI package" +
	"such as anygui, PythonCard, Tkinter, wxPython, etc."
	+ "\n\nEasyGui is running Tk version: " + str(TkVersion)
	)

	#========================================== END DEMONSTRATION DATA


	while 1: # do forever
		choices = [
			"msgbox",
			"buttonbox",
			"buttonbox(image) -- an example of buttonbox with an 'image' specification",
			"choicebox",
			"multchoicebox",
			"textbox",
			"ynbox",
			"ccbox",
			"enterbox",
			"codebox",
			"integerbox",
			"boolbox",
			"indexbox",
			"filesavebox",
			"fileopenbox",
			"passwordbox",
			"multenterbox",
			"multpasswordbox",
			"diropenbox",
			"About EasyGui",
			" Help"
			]
		choice = choicebox(msg=intro_message
			, title="EasyGui " + EasyGuiRevisionInfo
			, choices=choices)

		if not choice: return

		reply = choice.split()

		if   reply[0] == "msgbox":
			reply = msgbox("short msg", "This is a long title")
			print ("Reply was:", repr(reply))

		elif reply[0] == "About":
			reply = abouteasygui()

		elif reply[0] == "Help":
			help("easygui")

		elif reply[0] == "buttonbox":
			reply = buttonbox()
			print ("Reply was:", repr(reply))

			reply = buttonbox(msg=msg
			, title="Demo of Buttonbox with many, many buttons!"
			, choices=choices)
			print ("Reply was:", repr(reply))

		elif reply[0] == "buttonbox(image)":
			image = "python_and_check_logo.gif"

			msg   = "Pretty nice, huh!"
			reply=msgbox(msg,image=image, ok_button="Wow!")
			print ("Reply was:", repr(reply))

			msg   = "Do you like this picture?"
			choices = ["Yes","No","No opinion"]

			reply=buttonbox(msg,image=image,choices=choices)
			print ("Reply was:", repr(reply))

			image = os.path.normpath("python_and_check_logo.png")
			reply=buttonbox(msg,image=image, choices=choices)
			print ("Reply was:", repr(reply))

			image = os.path.normpath("zzzzz.gif")
			reply=buttonbox(msg,image=image, choices=choices)
			print ("Reply was:", repr(reply))

		elif reply[0] == "boolbox":
			reply = boolbox()
			print ("Reply was:", repr(reply))

		elif reply[0] == "enterbox":
			message = "Enter the name of your best friend."\
			          "\n(Result will be stripped.)"
			reply = enterbox(message, "Love!", "     Suzy Smith     ")
			print ("Reply was:", repr(reply))

			message = "Enter the name of your best friend."\
			          "\n(Result will NOT be stripped.)"
			reply = enterbox(message, "Love!", "     Suzy Smith     ",strip=False)
			print ("Reply was:", repr(reply))

			reply = enterbox("Enter the name of your worst enemy:", "Hate!")
			print ("Reply was:", repr(reply))

		elif reply[0] == "integerbox":
			reply = integerbox(
				"Enter a number between 3 and 333",
				"Demo: integerbox WITH a default value",
				222, 3, 333)
			print ("Reply was:", repr(reply))

			reply = integerbox(
				"Enter a number between 0 and 99",
				"Demo: integerbox WITHOUT a default value"
				)
			print ("Reply was:", repr(reply))

		elif reply[0] == "diropenbox":
			title = "Demo of diropenbox"
			msg = "This is a test of the diropenbox.\n\nPick the directory that you wish to open."
			d = diropenbox(msg, title)
			print ("You chose directory...:", d)

		elif reply[0] == "fileopenbox":
			f = fileopenbox()
			print ("You chose to open file:", f)

		elif reply[0] == "filesavebox":
			f = filesavebox()
			print ("You chose to save file:", f)

		elif reply[0] == "indexbox":
			title = reply[0]
			msg   =  "Demo of " + reply[0]
			choices = ["Choice1", "Choice2", "Choice3", "Choice4"]
			reply = indexbox(msg, title, choices)
			print ("Reply was:", repr(reply))

		elif reply[0] == "passwordbox":
			reply = passwordbox("Demo of password box WITHOUT default"
				+ "\n\nEnter your secret password", "Member Logon")
			print ("Reply was:", str(reply))

			reply = passwordbox("Demo of password box WITH default"
				+ "\n\nEnter your secret password", "Member Logon", "alfie")
			print ("Reply was:", str(reply))

		elif reply[0] == "multenterbox":
			msg = "Enter your personal information"
			title = "Credit Card Application"
			fieldNames = ["Name","Street Address","City","State","ZipCode"]
			fieldValues = []  # we start with blanks for the values
			fieldValues = multenterbox(msg,title, fieldNames)

			# make sure that none of the fields was left blank
			while 1:
				if fieldValues == None: break
				errmsg = ""
				for i in range(len(fieldNames)):
					if fieldValues[i].strip() == "":
						errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
				if errmsg == "": break # no problems found
				fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)

			print ("Reply was:", fieldValues)

		elif reply[0] == "multpasswordbox":
			msg = "Enter logon information"
			title = "Demo of multpasswordbox"
			fieldNames = ["Server ID", "User ID", "Password"]
			fieldValues = []  # we start with blanks for the values
			fieldValues = multpasswordbox(msg,title, fieldNames)

			# make sure that none of the fields was left blank
			while 1:
				if fieldValues == None: break
				errmsg = ""
				for i in range(len(fieldNames)):
					if fieldValues[i].strip() == "":
						errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
				if errmsg == "": break # no problems found
				fieldValues = multpasswordbox(errmsg, title, fieldNames, fieldValues)

			print ("Reply was:", fieldValues)


		elif reply[0] == "ynbox":
			reply = ynbox(msg, title)
			print ("Reply was:", repr(reply))

		elif reply[0] == "ccbox":
			reply = ccbox(msg)
			print ("Reply was:", repr(reply))

		elif reply[0] == "choicebox":
			longchoice = "This is an example of a very long option which you may or may not wish to choose."*2
			listChoices = ["nnn", "ddd", "eee", "fff", "aaa", longchoice
					, "aaa", "bbb", "ccc", "ggg", "hhh", "iii", "jjj", "kkk", "LLL", "mmm" , "nnn", "ooo", "ppp", "qqq", "rrr", "sss", "ttt", "uuu", "vvv"]

			msg = "Pick something. " + ("A wrapable sentence of text ?! "*30) + "\nA separate line of text."*6
			reply = choicebox(msg=msg, choices=listChoices)
			print ("Reply was:", repr(reply))

			msg = "Pick something. "
			reply = choicebox(msg=msg, choices=listChoices)
			print ("Reply was:", repr(reply))

			msg = "Pick something. "
			reply = choicebox(msg="The list of choices is empty!", choices=[])
			print ("Reply was:", repr(reply))

		elif reply[0] == "multchoicebox":
			listChoices = ["aaa", "bbb", "ccc", "ggg", "hhh", "iii", "jjj", "kkk"
				, "LLL", "mmm" , "nnn", "ooo", "ppp", "qqq"
				, "rrr", "sss", "ttt", "uuu", "vvv"]

			msg = "Pick as many choices as you wish."
			reply = multchoicebox(msg,"DEMO OF multchoicebox", listChoices)
			print ("Reply was:", repr(reply))

		elif reply[0] == "textbox":
			msg = "Here is some sample text. " * 16
			reply = textbox(msg, "Text Sample", text_snippet)
			print ("Reply was:", repr(reply))

		elif reply[0] == "codebox":
			msg = "Here is some sample code. " * 16
			reply = codebox(msg, "Code Sample", code_snippet)
			print ("Reply was:", repr(reply))

		else:
			msgbox("Choice\n\n" + choice + "\n\nis not recognized", "Program Logic Error")
			return

EASYGUI_ABOUT_INFORMATION = '''
========================================================================
version 0.83 2008-06-12
========================================================================

BUG FIXES
------------------------------------------------------
 * fixed a bug in which fileopenbox, filesavebox, and diropenbox
   were returning an empty tuple, rather than None, when a user
   cancelled.  Thanks to Nate Soares for reporting this and sending
   in a fix.

BACKWARD-INCOMPATIBLE CHANGES
------------------------------------------------------
 * changed enterbox so that by default it strips its result
   (i.e. removes leading and trailing whitespace).
   If you want it not to strip, use keyword argument:  strip=False.

   This change makes it easier to test the results of the call::

		reply = enterbox(....)
		if reply:
			...
		else:
			...

 * changed the name of the "button_text" (formerly "buttonMessage") parameter
   to "ok_button" in the msgbox parameters.

========================================================================
version 0.80 2008-06-02
========================================================================

ENHANCEMENTS
------------------------------------------------------
 * added image keyword to msgbox and buttonbox
   Note that it can display only .gif images.
   see: http://effbot.org/tkinterbook/photoimage.htm
 * improved a lot of the docstrings.
 * added a new abouteasygui() function

BUG FIXES
------------------------------------------------------
 * changed mutable default arguments (lists) to tuples

 * diropenbox, fileopenbox, and filesavebox now execute
   os.path.normpath() on the choice before returning it.
   This fixes a nasty bug/inconvenience for Windows users.

 * In integerbox:
   old behavior: If user cancels, the default value is returned.
   new behavior: If user cancels, None is returned.

   NOTE that this bugfix has the potential to break existing programs.


CHANGES
------------------------------------------------------
 * removed the "restore default" button on enterbox.
   It was non-standard and was too long to display properly in
   some environments.
 * default message for buttonbox changed from
   "Shall I continue?" to just "".

BACKWARD-INCOMPATIBLE CHANGES
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   These changes may break backward compatibility.

   Note that the following changes may break backward compatibility
   in programs that invoke EasyGui functions with keyword
   (rather than positional) arguments.

   They have been changed in order to standardize keyword arguments, so
   that EasyGui functions can be more easily used with keyword arguments.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
changed parameter name "message"              to "msg" everywhere
changed parameter name "buttonMessage"        to "button_text"
changed parameter name "argListOfFieldNames"  to "fields"
changed parameter name "argListOfFieldValues" to "values"

changed the following parameter names  to "default":
    argDefault
    argDefaultPassword
    argDefaultText
    argInitialFile
    argInitialDir
'''

def abouteasygui():
	"""
	shows the easygui revision history
	"""
	codebox("About EasyGui\n"+EasyGuiRevisionInfo,"EasyGui",EASYGUI_ABOUT_INFORMATION)
	return None



if __name__ == '__main__':
	_test()
