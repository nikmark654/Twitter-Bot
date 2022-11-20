import pyautogui as pg
import tkinter as tk
from tkinter.ttk import *
import pandas as pd
from os import path
from tkinter import Toplevel as TopLevel

"""
    [1] __init__(self) finds the path. To be replaced/dropped. Useless.
    [2] self.main(self) is called by primary gui script to update steps. Calls self.window(self) method. Reason need this has to do with primary_gui.py
    [3] self.window(self) opens TopLevel() window for step recording. Listens key('q') and holds buttons & labels. Calls self.submit(), self.to_csv() & self.cleaning. Frame obj listens key
        3.1 self.Keydown(self,e) checks if key pressed is Q
        3.2 self.submit(self, position) opens TopLevel() window for user to input options info. Submit button calls self.numeric method
            3.2.1 self.numeric(self, positions, windows) integrates position and options data. Destroyes self.submit() TopLevel window, updates steps list & diplay.
        3.3 self.clearing(self) Clears inputs and permits user to start recording again.
        3.4 self.to_csv(self) Inputs step positions to file positions.csv
"""

class side_window(tk.Toplevel):

    def __init__(self):
        self.path = path.dirname(__file__) #Getting the path. Was used for othe things - now is used just to initialize object.
    
    def main(self): # Is called from primary gui script. Initializes window method.
        self.window()

    def window(self): # Creates TopLevel window, with buttons ect.

        # Essential object attribute lists that are used from methods of this class
        self.position = []
        self.steps = []
        self.current_steps = []

        self.window = TopLevel() #TopLevel window
        
        # Buttons & Labels #

        # Label with instructions.
        help = tk.Label(self.window, text = "Position your cursor \nat the position where \nnext step is & press Q")
        help.grid(row = 1, column = 0)

        # Submiting current position button
        button = tk.Button(self.window, text = "Submit", command = lambda: self.submit(self.position))
        button.grid(row = 2, column = 0)
        
        # Cleaning submitions button
        button1 = tk.Button(self.window, text = "Clean Submitions", command = self.clearing)
        button1.grid(row = 3, column = 0)

        # Save in file button
        button2 = tk.Button(self.window, text = "Save in file", command = self.to_csv)
        button2.grid(row = 4, column = 0)

        # Current Position Label
        self.current_pos = tk.Label(self.window, text = self.position)
        self.current_pos.grid(row = 5, column = 0)

        # Current steps list
        self.current_steps.append(tk.Label(self.window, text = self.steps))
        for i in self.current_steps:
            i.grid(row = 6, column = 0)

        #listener for key Q
        frame = tk.Frame(self.window, width=1, height=1)
        frame.bind("<KeyPress>", self.keydown)
        frame.grid(row = 0, column = 0)
        frame.focus_set()

    def keydown(self, e): #Listening to cursor position on demand
        if e.char == "q" or e.char == "Q" or e.char == ";" or e.char == ":": # ; and : are for greek keyboard mode.
            x, y= pg.position()
            self.position = [x,y]
            self.current_pos.destroy()
            self.current_pos = tk.Label(self.window, text = "Current Position = " + str(self.position))
            self.current_pos.grid(row = 5, column = 0)

    def submit(self, position): # Creates TopLevel window for user to input mode and action options. Options are passed to numeric fuction which integrates coordinates and options.
        windows = tk.Toplevel()
        windows.geometry("400x500")

        # Labels with info and names of options.
        label_1 = Label(windows, text = ("Current position is :", position))
        label_1.grid(row = 0, column = 1)

        label0 = Label(windows, text = "Delay")
        label0.grid(row=1, column = 0)
        
        label1 = Label(windows, text = "Action")
        label1.grid(row=2, column = 0)

        # Options options.
        options_list1 = ["0", "1", "2"]
        value_inside1 = tk.StringVar(windows)
        value_inside1.set("Choose one of the following options")
        question_menu1 = OptionMenu(windows, value_inside1, *options_list1)
        question_menu1.grid(row = 1, column = 1)

        options_list2 = ["0", "1", "2", "3"]
        value_inside2 = tk.StringVar(windows)
        value_inside2.set("Choose on of the following options")
        question_menu2 = OptionMenu(windows, value_inside2, *options_list2)
        question_menu2.grid(row = 2, column = 1)

        # Submit option button.
        button = Button(windows, text = "Submit", command = lambda: self.numeric([position[0], position[1], value_inside1.get(), value_inside2.get()], windows))
        button.grid(row = 3, column = 1)

        # Label with instructions.
        description = Label(windows, text = """Delay: \n
        2 = delay of 2~2.5 seconds\n
        1 = delay of 20~25 seconds\n
        0 = no delay\n\n
        Action:\n
        3 = 2 clicks\n
        2 = Text input only (tweet)\n
        1 = Text input & enter pressing (username & password) \n
        0 = 1 click \n
        """)
        description.grid(row = 4, column = 1)

    def numeric(self, positions, windows): # Destroys TopLevel window of submit method, integrates position & options by steps passed processes. Updates step list displayed to be saved in file 
        windows.destroy()
        self.steps.append(positions)
        k = 0
        for i in self.current_steps:
            i.destroy()
        for i in self.steps:
            k = k+1
            self.current_steps.append(Label(self.window, text = f"{k} step is : {i}"))
            self.current_steps[-1].grid(row = k+5, column = 0)

    
    def clearing(self): # Cleans step list. User may start record steps again.
        self.current_pos.destroy()
        self.steps = []
        for i in self.current_steps:
            i.destroy()
            
    
    def to_csv(self): # Writes integrated position & options data to .csv
        positions = pd.DataFrame(self.steps, columns = ["X", "Y", "mode", "action"])
        print(positions)
        positions.to_csv("positions.csv", mode="w", index = False)
        self.window.destroy()

    

    