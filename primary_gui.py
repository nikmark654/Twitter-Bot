

"""
Starting GUI app for twitter bot. Bot automates actions related(but not limited) to tweeting.

Algorithm in this script
    [1] root.mainloop will run.
    [2] with mainloop, bot will always check current time and schedule.
    [3] If changes were made, bot will read them after clicking on update button.
    [4] Schedule will be displayed on window.
    [5] TopLevel windows & certain info updates are dealt with in positioning.py
"""

import tkinter as tk
import bot_script as bt
import positioning

bot = bt.botting()

def task(): #Loop calling again and again bot_script, which has methods that check datetime.today. After some conditions -> True, steps run on the background  
    bot.running() #custom method from bot_script
    root.after(10000, task) #Loop back at the top

def updater(): #Button function that calls bot_script methods to read database(.csv) info and update label
    bot.updater() #custom method from bot_script
    displaying()

def displaying(): # Function that is called by updater(). Updates window display after button updater_bt clicked
    # Clean label list
    global schedule
    for i in schedule:
        i.destroy()
    
    schedule = []
    r = 3
    # Refill label list
    for i in bot.todays:
        schedule.append(tk.Label(root, text = i))
        schedule[-1].pack()

# Standard gui commands
root = tk.Tk()
root.title("Twitter - Bot")
root.geometry("300x300")
    
# Buttons
updater_bt = tk.Button(root, text = "Update Schedule", command = lambda: updater(), bg="yellow", height= 3, width=30)
updater_bt.pack()

# side_wind is an object with which we create TopLevel window with positioning.py methods. !Essential! for reasons. Needed for following button.
side_wind = positioning.side_window()

step_but = tk.Button(root, text = "Define Steps", command = lambda: side_wind.main(), bg="red", height= 3, width=30)
step_but.pack()

# test_button calls a bot_script method that force-initialize bot tweet actions. Used for testing correct step positions.
test_button = tk.Button(root, text = "Test", command = bot.Testing_Button, bg = "green", height= 3, width=30)
test_button.pack()

#labels
schedule = []

k = 1

# for loop for an attribute created with bot_script and holds today's schedule. Initial display on main window. Updates with update_bt.
for i in bot.todays:
    schedule.append(tk.Label(root, text = i))
    schedule[-1].pack()
    k = k+1

root.after(1, task)
root.mainloop()