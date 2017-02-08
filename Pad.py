# Setting up imports
import tkinter, re, CAM
from tkinter import filedialog

# Class declaration
class Pad:
    # Constructor initialisation
    def __init__(self, masterWindow):

        # Perform main setup routine
        self.root = masterWindow
        self.Frame = tkinter.Frame(masterWindow)
        self.Frame.pack(expand="yes", fill="both")
        self.MenuBar = tkinter.Menu(masterWindow)
        self.CreateMenus()

        # Setup the main text area
        self.textArea = tkinter.Text(self.Frame)
        self.textArea.pack(expand="yes", fill="both")

        # Create keyboard bindings
        self.textArea.bind("<Control-S>", self.SaveAs)
        self.textArea.bind("<Control-s>", self.Save)
        self.textArea.bind("<Control-n>", self.New)
        self.textArea.bind("<Control-o>", self.Open)
        self.textArea.bind("<Control-r>", self.Run)
        self.textArea.bind("<Control-R>", self.ReplaceWindow)
        self.textArea.bind("<Control-p>", self.HelpWindow)
        self.textArea.bind("<Key>", self.CheckEdit)
        self.root.protocol("WM_DELETE_WINDOW", lambda :self.CheckAction("quit"))

        # Setup file control variables
        self.Saved = False
        self.Edited = False
        self.filePath = "Untitled"
        self.root.title("Pad - " + self.filePath)
        self.LastWord = None
        self.DocsPath = "DOCUMENTATION.txt"

    # Creates all cascade menus and adds their commands
    def CreateMenus(self):
        # File menu setup
        fileMenu = tkinter.Menu(self.MenuBar, tearoff=0)
        fileMenu.add_command(label="New", command=self.New)
        fileMenu.add_command(label="Open...", command=self.Open)
        fileMenu.add_command(label="Save", command=self.Save)
        fileMenu.add_command(label="Save As...", command=self.SaveAs)
        fileMenu.add_command(label="Run", command=self.Run)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=lambda: self.CheckAction("quit"))
        self.MenuBar.add_cascade(label="File", menu=fileMenu)

        # Edit menu setup
        editMenu = tkinter.Menu(self.MenuBar, tearoff=0)
        editMenu.add_command(label="Replace", command=self.ReplaceWindow)
        self.MenuBar.add_cascade(label="Edit", menu=editMenu)

        # Edit menu setup
        helpMenu = tkinter.Menu(self.MenuBar, tearoff=0)
        helpMenu.add_command(label="Shortcuts", command=self.HelpWindow)
        helpMenu.add_command(label="Documentation", command=self.ShowDocumentation)
        self.MenuBar.add_cascade(label="Help", menu=helpMenu)   

    # SaveAs function that can be called either through the file menu or keyboard shortcut 
    def SaveAs(self, event=None):
        # Get filepath from a popup window
        self.filePath = tkinter.filedialog.asksaveasfilename()
        if self.filePath == "":
            self.filePath = "Untitled"
            return
        self.Saved = True
        self.Save()

    # Save function that uses basic recursion with saveas function to check for saving
    def Save(self, event=None):
        # Check if not saved before
        if not self.Saved:
            self.SaveAs()
            return
        # Set title of the window to the file path removing asterisk in process
        self.root.title("Pad - " + self.filePath)
        
        # Get all text
        text = self.textArea.get("1.0", 'end-1c').split('\n')
        
        # Write to a file with the given path
        file = open(self.filePath, 'w')
        for i in text:
            file.write(i + '\n')
        file.close()
        self.Edited = False

    # Function for showing documentation of the CAM programming language
    def ShowDocumentation(self):
        docWindow = tkinter.Tk()
        docWindow.title("Documentation")
        docs = tkinter.Text(docWindow)
        docs.pack(expand="yes", fill="both")
        file = open(self.DocsPath, 'r')
        for line in file:
            docs.insert("end", line)
        file.close()
        docs.configure(state="disabled")
        docWindow.mainloop()

    # Open function for opening **text based** files
    def Open(self, event=None):
        # Prevent user from losing current work unless they want to
        if self.Edited:
            if not self.CheckAction():
                return
        # Ask for filepath and delete current text contents and replcae with the new text from the desired file
        self.filePath = tkinter.filedialog.askopenfilename()
        if self.filePath == "":
            self.filePath = "Pad - Untitled"
            return
        self.textArea.delete("1.0", 'end-1c')
        self.root.title("Pad - " + self.filePath)
        file = open(self.filePath, 'r')
        for line in file:
            self.textArea.insert("end", line)
        file.close()
        self.Saved = True
        self.Edited = False

    # Function for creating new blank document
    def New(self, event=None):
        # Prevents user from losing work unless they want to
        if self.Edited:
            if not self.CheckAction():
                return
        self.root.title("Pad - Untitled*")
        self.Saved = False
        self.Edited = False
        self.textArea.delete("1.0", 'end-1c')

    # Function for running CAM code
    def Run(self, event=None):
        # Save file first
        self.Save()
        print('\n'*50)
        # Call the CAM interpreter to compile the code and return the environment created
        env = CAM.main(self.filePath)


    # Function that creates the find and replace window
    def ReplaceWindow(self, event=None):
        # Create window and add widgets
        replaceWindow = tkinter.Tk()
        replaceWindow.title("Replace...")
        searchLabel = tkinter.Label(replaceWindow, text="Search: ").pack()
        searchTerm = tkinter.Entry(replaceWindow)
        searchTerm.pack()
        replaceLabel = tkinter.Label(replaceWindow, text="Replace: ").pack()
        replaceTerm = tkinter.Entry(replaceWindow)
        replaceTerm.pack()

        # Setup buttons with function calls to Replace with args
        replaceNext = tkinter.Button(replaceWindow, text="Replace Next", command=lambda: self.Replace(searchTerm.get(), replaceTerm.get(), False)).pack()
        replaceAll = tkinter.Button(replaceWindow, text="Replace All", command=lambda: self.Replace(searchTerm.get(), replaceTerm.get(), True)).pack()

        replaceWindow.mainloop()

    # Function for carrying out character/word replacement
    def Replace(self, search, replace, replaceAll):
        # Convert all text into words into a 2d array with lines and then words in each line
        lines = self.textArea.get("1.0", 'end-1c').split('\n')
        words = [line.split(' ') for line in lines]

        indexChecked = ''

        # Loop through each line and word
        for i in range(0, len(words)):
            for k in range(0, len(words[i])):
                # Check to see if the word has just had a replacement
                if (self.LastWord is not None) and not replaceAll and i == self.LastWord[0] and k == self.LastWord[1]:
                    indexChecked = self.LastWord[2]

                # Check for word match
                if search in words[i][k]:
                    # Find all locations of the match in the word
                    indexes = [m.start() for m in re.finditer(search, words[i][k])]

                    # Loop through each location and replace where necessary
                    for index in indexes:
                        if index == indexChecked:
                            continue
                        temp = ""
                        
                        # Loop through each character in the word
                        for l in range(0, len(words[i][k])):
                            # If this is the position of the match then replace
                            if l == index:
                                temp += replace
                                continue
                            
                            # Skip all replcement characters
                            if l < len(search)+index and l > index:
                                continue
                            temp += words[i][k][l]

                        # Change word to new replacement
                        words[i][k] = temp
                        self.Edited = True

                        # Check for type of replacement
                        if not replaceAll:
                            self.LastWord = (i, k, index)
                            self.textArea.delete("1.0", 'end-1c')
                            self.textArea.insert("end", '\n'.join([' '.join(line) for line in words]))
                            break
                        
        # Re-enter all text but with replacements into area
        self.textArea.delete("1.0", 'end-1c')
        self.textArea.insert("end", '\n'.join([' '.join(line) for line in words]))

    # Function for help window that currently only displays shortcuts
    def HelpWindow(self, event=None):
        helpWindow = tkinter.Tk()
        helpWindow.title("Help")
        shortcuts = ["Command/Control key & S --> Save",
                     "CommandControl key & Shift & S --> Save As",
                     "Command/Control key & O --> Open",
                     "Command/Control key & N --> New",
                     "Command/Control key & R --> Run",
                     "Command/Control key & shift & R --> Replace",
                     "Command/Control key & P --> Help"]

        for shortcut in shortcuts:
            lbl = tkinter.Label(helpWindow, text=shortcut).pack()
        helpWindow.mainloop()

    # Function for checking when the text in the widget has been edited to prevent user data loss
    def CheckEdit(self, event=None):
        if event.char != "":
            self.Edited = True
            self.root.title("Pad - " + self.filePath + '*')
        elif event.keycode in [22, 107, 36]: # 22, 107, 36 are the keycodes for delete, return and backspace
            self.Edited = True
            self.root.title("Pad - " + self.filePath + '*')

    # Function for checking a users action, such as closing a window or opening a new file
    def CheckAction(self, action=None):
        # Check if action was quit
        if not self.Edited and action == "quit":
            self.root.destroy()
            return

        # Setup popup window
        popUp = tkinter.Tk()
        popUp.title("Are you sure?")
        popUp.geometry("250x50")
        lbl = tkinter.Label(popUp, text="Do you want to save?").pack()
        self.action = ''

        # Function for saving a choice based on user button press
        def Choice(ac):
            self.action = ac
            if ac == "save":
                self.Save()
                self.action = True
            popUp.quit()
            
        # Setup widgets
        frame = tkinter.Frame(popUp)
        frame.pack(side="bottom")
        yesBtn = tkinter.Button(frame, text="No", command=lambda: Choice(True)).pack(side="right")
        saveBtn = tkinter.Button(frame, text="Save", command=lambda :Choice("save")).pack(side="right")
        noBtn = tkinter.Button(frame, text="Cancel", command=lambda :Choice(False)).pack(side="right")        
        popUp.mainloop()
        
        try:
            popUp.destroy()
        except:
            pass
        
        if action == "quit" and self.action == True:
            self.root.destroy()
        return self.action

# Setup main 'root' window with NotePadClone instance
root = tkinter.Tk()
pad = Pad(root)

# Link app menubar with root
root.config(menu=pad.MenuBar)
root.mainloop()
