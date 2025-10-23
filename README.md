# Lanx's Nonogram

My iteration of Nonogram, a game I quite enjoy playing on my spare time

# Objective

The objective of this game is to fill all the squares on the board using clues provided on the sides of the board. 

# Gameplay

The numbers on the side provide information about the number of groups and its amount of crosses on a particular line.
For instance, the number ```2, 3``` tells you that a group of 2 X's and 3 X's should exist on that line.
The game concludes when the player successfully fills the board with the correct tiles without dying.

# Controls

Note that the numbers count the crosses (X)

| Control | Action | 
| :------- | ------: |
| LMB | Places an X | 
| RMB | Places a black box|

# Run

To run with the default configuration, simply run the script.

For customs configuration, cd to the directory and run:
```python main.py [width] [height] [lives]```


# Developer notes

During the initialization process, I reckoned that adding some sort of weightage would help setting a fairer game by clumping up X's more frequently.
The way I implement it is to keep a list of floating numbers [0.15, 0.5, 0.7, 0.91] and select one of them at random for each row to dictate the chances of
spawning the X on that particular box. 
Though, I realize it would result in the game generating more frequent 'easy' rows, i.e. a row full of X's or blanks.
Due to this I changed the weightage implementation to a dynamic range-based, though I haven't tested out its performance.
