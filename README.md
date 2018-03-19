**Murder Mystery Movement Generator**
by Shayne Hayes and Jesse Fischbeck

Although murder mysteries are immensely popular, facts related to the crime are almost always hand-authored rather than computer-generated. Our program seeks to automate the process of designing spatial facts.
Given high-level information about a mystery, our Murder Mystery Movement Generator generates positions for all characters at each timestep such that all innocent characters have ironclad alibis.

**Value:**

Consistency is immensely important in murder mysteries, where entire plots are built around untangling webs of deception by finding inconsistencies. Facts related to characters’ positions and movements (their “opportunity”) are particularly tedious to author and difficult to keep consistent, especially in the context of a game where the player may interrogate suspects freely. Our program guarantees that the mystery is solvable and that spatial facts are consistent, and aids the writer in deciding where characters go during less important parts of the story.

This could save murder mystery writers hours of design work. To test the utility of our program, we used it to generate character movements for our game [Murder at the Murder Mystery Convention](http://www.shaynehayes.net/convention/play.html). With our program’s help, we managed to write 8 pages of character dialogue in 3 days flat!


**Usage:**
* Try running the provided scenario (data.JSON) by executing run.py from the command line. You will need to have Python installed.
  * The program expects two arguments: the filename of your setting's map (as a GIF) and the filename of the JSON file containing information about your mystery.
* When run correctly the program will launch a playback program showing the results of the rather boring example scenario. Right click to advance to the next timestep and left click to go back.
* Now that you know how to run the program, copy the JSON file and enter the data for your mystery. You may supply the following information:
  * "murder time": when the murder takes place
  * "discover time": when the body is discovered
  * "people": characters and their corresponding color for playback
  * "victim": the murder victim
  * "murderer": the murderer
  * "rooms": the rooms that make up your setting. All rooms contain the following three properties:
    * "min": the minimum amount of time a person may spend in this room
    * "max": the maximum amount of time a person may spend in this room (note: this does not apply to the victim)
    * "coords": the x and y coordinates of the room for playback
  * "connections": used to specify how the rooms are connected, like directed edges on a graph
  * "vision": used to specify which rooms are visible from other rooms
  * "block": used to block certain characters from using certain room connections. Useful for secret passages
  * "positions": optional data specifying where characters are at certain times in the story
* Run the program with your new JSON file.
  * If the program prints "ERROR: The problem instance has no solutions." then the program cannot generate movements for your characters in a way that guarantees solvability. This usually means that your authored "positions" data is inconsistent with the rules the program uses to generate spatial data. A full list of these rules may be found below.
  * Pro Tip: It helps to specify as little spatial data as possible. The more you author, the more likely it will be for the program to find your scenario unsolvable.
  * If the playback opens that means movements for your characters have been generated successfully. If the movements are to your liking, you can start writing your murder mystery!
  
  
**Rules used to generate movements:**
* Characters may only move to adjacent rooms
* Characters cannot move more than one room per timestep
* Characters cannot move down paths blocked for them
* Characters may not stay in a room for longer than its max time limit (except for the victim)
* Characters may not stay in a room for shorter than its min time limit
* All innocent characters must be seen at each timestep (note: the victim's vision does not count)
* The murderer must be with the victim at the time of the crime
* The murderer must not be with the victim at the time of discovery
* The victim may not move after the murder
* The victim must not be seen during or after the murder by any innocent before the time of discovery
* The victim must be discovered at the time of discovery

This project was made possible by [Potassco](http://potassco.sourceforge.net/), a collection of tools for Answer Set Programming.
Special thanks to Daniel Shapiro, our AI professor, as well as Adam Smith for providing helpful feedback on our project proposal.
