import subprocess
import os, sys
from random import *
import tkinter
import traceback
import json
from timeit import default_timer as time
from math import floor, ceil

if len(sys.argv) != 3:
    print("usage: %s map.gif data.json" % sys.argv[0])
    sys.exit(-1)
    
_, MAP_FILENAME, DATA_FILENAME = sys.argv
PATH =  os.getcwd()

master = tkinter.Tk()

map_image = tkinter.PhotoImage(file=MAP_FILENAME)
image_width = map_image.width()
image_height = map_image.height()

canvas = tkinter.Canvas(master, width=image_width, height=image_height)
canvas.pack()

data = None
timestep = 1

def last_timestep(event):
    global timestep
    if timestep > 1:
        timestep -= 1
        start_time = time()
        # Move the character circles incrementally
        while time() - start_time < 1:
            last_time = timestep+1
            animate(last_time, 1 - (time() - start_time))
        redraw()

def next_timestep(event):
    global timestep
    global data
    if timestep < data["discover time"]:
        timestep += 1
        start_time = time()
        # Move the character circles incrementally
        while time() - start_time < 1:
            last_time = timestep-1
            animate(last_time, 1 - (time() - start_time))
        redraw()

def animate(last_time, progress):
    global data
    global timestep
    canvas.delete(tkinter.ALL)
    canvas.create_image((0,0), anchor=tkinter.NW, image=map_image)
    canvas.create_text(30, 30, text=round(timestep + progress * (last_time-timestep), 1))
    
    # Render a circle for each character
    offset = 0
    for person in data["people"]:
        move_from = None
        move_to = None
        for room in data["positions"][person]:
            if move_from != None and move_to != None:
                break
            if last_time in data["positions"][person][room]:
                move_from = room
            if timestep in data["positions"][person][room]:
                move_to = room
        if move_from is not None and move_to is not None:
            x_pos = data["rooms"][move_to]["coords"][0] + progress * (data["rooms"][move_from]["coords"][0] - data["rooms"][move_to]["coords"][0])
            y_pos = data["rooms"][move_to]["coords"][1] + progress * (data["rooms"][move_from]["coords"][1] - data["rooms"][move_to]["coords"][1])
            canvas.create_oval(x_pos-5,y_pos-5-offset,x_pos+5,y_pos+5-offset,outline=data["people"][person])
        offset += 2
    master.update()
    
def redraw():
    global data
    global timestep
    canvas.delete(tkinter.ALL)
    canvas.create_image((0,0), anchor=tkinter.NW, image=map_image)
    canvas.create_text(30, 30, text=float(timestep))
    
    # Render a circle for each character
    offset = 0
    for person in data["people"]:
        for room in data["positions"][person]:
            if timestep in data["positions"][person][room]:
                x_pos = data["rooms"][room]["coords"][0]
                y_pos = data["rooms"][room]["coords"][1]
                canvas.create_oval(x_pos-5,y_pos-5-offset,x_pos+5,y_pos+5-offset,outline=data["people"][person])
        offset += 2
    
    # Draw character dots

def write_instance():
    """ Read in input from data.txt and convert it to a problem instance

    Args:
        None
    """
    print("Generating problem instance...")
    global data
    # Load data.json
    data = json.load(open(DATA_FILENAME))
    # Open ins.lp
    f = open('ins.lp', 'w')
    # Write key info
    f.write("murdertime(" + str(data["murder time"]) + ").\n")
    f.write("discovertime(" + str(data["discover time"]) + ").\n")
    f.write("murderer(" + data["murderer"] + ").\n")
    f.write("victim(" + data["victim"] + ").\n\n")
    # Write people
    for person in data["people"]:
        f.write("person(" + person + ").\n")
    f.write("\n")
    # Write rooms
    for room in data["rooms"]:
        mintime = data["rooms"][room]["min"]
        maxtime = data["rooms"][room]["max"]
        f.write("room(" + room + ").\n")
        f.write("mintime(" + room + "," + str(mintime) + ").\n")
        f.write("maxtime(" + room + "," + str(maxtime) + ").\n")
    f.write("\n")
    # Write room connections
    for room in data["rooms"]:
        if room in data["connections"].keys():
            for next_room in data["connections"][room]:
                f.write("adj(" + room + "," + next_room + ").\n")
    f.write("\n")
    # Write room vision
    for room in data["rooms"]:
        if room in data["vision"].keys():
            for next_room in data["vision"][room]:
                f.write("vision(" + room + "," + next_room + ").\n")
    f.write("\n")
    # Write blocks
    for person in data["people"]:
        if person in data["block"].keys():
            for room in data["block"][person].keys():
                for next_room in data["block"][person][room]:
                    f.write("block(" + person + "," + room + "," + next_room + ").\n")
    f.write("\n")
    # Write pre-authored position data
    for person in data["people"]:
        if person in data["positions"].keys():
            for room in data["positions"][person].keys():
                for time in data["positions"][person][room]:
                    f.write("pre(" + str(time) + "," + person + "," + room + ").\n")
    f.write("\n")

def run_clingo():
    """ Run clingo and save the answer set to results.txt

    Args:
        None
    """
    print("Finding a solution...")
    # Let clingo do its thing
    command = 'clingo ins.lp enc.lp > results.txt'
    os.system(command)

def read_results():
    """ Read in the results from results.txt

    Args:
        None
    """
    print("Loading results...")
    global data
    # Open results.txt and skip the first four lines
    f = open('results.txt', 'r')
    for i in range(0,4):
        f.readline()
    # Get results string
    results = f.readline()
    # If the problem instance is satisfiable, append the results to the data dictionary
    satisfiable = f.read(11)
    f.close()
    if satisfiable == "SATISFIABLE":
        tokens = results.split()
        for token in tokens:
            token = token.replace("gen(","")
            token = token.replace(")","")
            time, person, room = token.split(",")
            if person not in data["positions"].keys():
                data["positions"][person] = {}
            if room not in data["positions"][person].keys():
                data["positions"][person][room] = []
            data["positions"][person][room].append(int(time))
    # Otherwise exit
    else:
        print("ERROR: The problem instance has no solutions.")
        sys.exit(-1)

if __name__ == '__main__':
    write_instance()
    run_clingo()
    read_results()
    redraw()
    
canvas.bind('<Button-1>', last_timestep)
canvas.bind('<Button-3>', next_timestep)
master.mainloop()