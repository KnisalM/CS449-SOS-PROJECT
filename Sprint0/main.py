"""This project designed for
UMKC CS449
Sprint 0
Due Date: 09/09/2025
Name: Marshall Knisal
This project was reuploaded to a properly formatted repository on 0/28/2025"""

import tkinter as tk
from functools import partial

window = tk.Tk()

window.title("CS449 Assignment Sprint 0")

v = tk.IntVar()



"""Creates layout of buttons for number pad
At this time, buttons are non functional
Goal: 
--Implement a grid of buttons that can be selected by both player/player or player/computer
Requirements: 
--Buttons must lock in place once selected unless implementing a stealing system
--Must always differentiate between which click is coming from which player or the computer
Questions: 
--How to implement visual lines in the grid manager to create board effect while having the 
    visual of the lines of the game board on screen at the same time"""
btns = tk.Frame(window)
btns.pack()
the_Board = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
for row in range(len(the_Board)):
    for col in range(len(the_Board[row])):
        i = the_Board[row][col]
        b = tk.Button(btns, text=str(i), bd=10)
        b.grid(row=row + 1, column=col, padx=1, pady=1, )

"""Creates the text labels using the Tkinter Library
Labels are then loaded into the correct Frame (btns)"""
l1 = tk.Label(btns, text="Hello! This Window Was Made For CS449 Assignment Sprint 0!")
l2 = tk.Label(btns, text="This Project Was Created by Marshall Knisal using  ")
l3 = tk.Label(btns, text="Resources that Are Documented in the source Code!")

"""Labels are then placed in the appropriate column to create the layout 
--Questions: How to utilize the grid manager to put the text labels off to the side of the 
    grid where the game will take place, play around with placement and take notes"""
l1.grid(row=4, column=1, padx=1, pady=1)
l2.grid(row=5, column=1, padx=1, pady=1)
l3.grid(row=6, column=1, padx=1, pady=1)

"""Radio Buttons are created using the tk.Radiobutton command
Goal:
--Implement Radiobuttons for 2 Player Mode VS Player vs Computer
Requirements:
--Tie radio buttons to a function that differentiates the game logic based on which radio button 
    is selected
--Note that there is a tk.IntVar() associated with the radio buttons
--This allows for them to be selected/deselected, otherwise they are perpetually on
--Loaded into correct frame. btns"""
hooray = tk.Radiobutton(btns, text="I am excited for the course!", variable=v, value=1)
boo = tk.Radiobutton(btns, text="I am NOT excited for the course :(", variable=v, value=2)

"""Placement in grid manager for radio buttons"""
hooray.grid(row=4, column=0, padx=1, pady=1)
boo.grid(row=4, column=2, padx=1, pady=1)

"""Creation of checkboxes
Goal: 
--Tie the checkbox into one of the intended functions of the game
    Ideally, the "show scoreboard" function which will show the 3 highest scores
    Recorded in that Session
Requirement: 
--Tie the checkbox, most likely just one, to a command that will show
--A top 3 scores for that session scoreboard
    The scoreboard will need to be maintained as the session goes on, and must be stored even when
    The checkbox is not currently selected to display it
--Scoreboard data storing will also need to be wiped at end of each session
Note:
"""
cb1 = tk.Checkbutton(btns, text="Hooray!!!", onvalue=1, offvalue=0, )
cb2 = tk.Checkbutton(btns, text="Boooooo", onvalue=1, offvalue=0, )
cb1.grid(row=5, column=0, padx=1, pady=1)
cb2.grid(row=5, column=2, padx=1, pady=1)

"""So far using a canvas is the only way to create lines that I have found using Tkinter
Goal: 
--To implement visual grid lines with selectable buttons to use as the game board
Requirements: 
--Finding a way to place buttons in the canvas not the grid manager
    OR
--Finding a way to create lines as elements and place them in the grid manager"""
canvas = tk.Canvas(btns, width=1000, height=1000, bg="white")

"""Creates Lines in Canvas that make the cross hatch board design"""
canvas.grid(row=7, column=1)
for i in range(0, 1000, 100):
    canvas.create_line(i, 0, i, 1000, fill='black', width=3)
for i in range(0, 1000, 50):
    canvas.create_line(0, i, 1000, i, fill='black', width=3)

"""executes the main window"""
window.mainloop()


"""Notes for Next Assignment/Thoughts going Forward
Potential Features: 
--2 player game mode and a Comp Game Mode (needs minimum computer to play)
--3 Score Scoreboard
--NEED to figure out how to place buttons in the canvas, or place lines in the grid manager

Resources:
https://www.pythonguis.com/tutorials/create-buttons-in-tkinter/
https://pythonbasics.org/tkinter-checkbox/
https://www.tutorialspoint.com/python/tk_grid.htm
https://www.pythonguis.com/tutorials 
"""
