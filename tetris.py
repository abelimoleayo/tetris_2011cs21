"""
Author: Imoleayo Abel

Date: 28th April 2011

Program Description: The program defines a Tetris class that creates a tetris
                     game as well as different operations/methods on the blocks
                     in the game and the game screen. <see Block class> for 
                     more details of block methods
"""

from graphics import *
from random import *
from time import *
from block import *
from math import *
from functions import *

class Tetris(object):

  """
  A class of Tetris objects that creates a game of TETRIS
  Parameters: None
  """

  def __init__(self):
    
    width = 200
    height = 500
    lineColor = 'grey49'  #color of grid-lines
    
    #set instance variables
    self.win = GraphWin("Tetris",width,height)
    self.win.setBackground('grey9')
    self.points = 0
    self.level = 1
    self.squarelist = [] #list of all squares present in the game
    self.lines = [] #list of lists with the j-th list containing the squares in
                    #the j-th row of the window
    for i in range(25):
      self.lines.append([])
    self.time = 0.65

    # draw horizontal part of background grid lines
    for i in range(int(0.1*width),height,int(0.1*width)):
      p1 = Point(0,i)
      p2 = Point(width,i)
      line = Line(p1,p2)
      line.draw(self.win)
      line.setFill(lineColor)

    # draw vertical part of background grid lines
    for j in range(int(0.1*width),width,int(0.1*width)):
      p3 = Point(j,0)
      p4 = Point(j,height)
      line = Line(p3,p4)
      line.draw(self.win)
      line.setFill(lineColor)

    # create and draw score, level and introductory message
    scorePoint = Point(0.15*width,0.15*width)
    self.scoreText = Text(scorePoint,"Score: %d\nLevel: %d" \
        % (self.points,self.level))
    self.scoreText.setFill("yellow")
    self.scoreText.setSize(10)
    self.scoreText.draw(self.win)
    introTextPt = Point(0.5*width,0.4*height)
    text = "Welcome to TETRIS v.1.0.\nsee command line for help"
    text = text + "\nwhen you are ready,...\n click anywhere to continue"
    self.introText = Text(introTextPt,text)
    self.introText.setSize(10)
    self.introText.setFill('yellow')
    self.introText.draw(self.win)

#-----------------------------------------------------------------------------#

  def __str__(self):
    """
    Returns a string of text describing the Tetris object when it is printed
    """

    s = "Current Point: %d" % (self.points)
    s = s + "\nCurrent Level: %d" % (self.level)
    s = s + "\nNumber of Cleared Rows: %d" % (int(0.1*self.points))
    
    counter = 0
    for line in self.lines:
      if len(line) != 0:
        counter += 1

    s = s + "\nCurrent height of Blocks: %d rows" % (counter)
    
    return s

#-----------------------------------------------------------------------------#

  def play(self):
    """
    Runs the game proper with the other defined methods in the class!
    """
    
    self.printHelp() # print instructions on command line
    self.win.getMouse()
    self.introText.undraw()

    BlockTypes = ["flat","box","rightz","leftz","rightl","leftl","tee"]

    while self.topClear(): # game runs till blocks fill up screen
                           # <see topClear method>
      shape = choice(BlockTypes) # make random choice of block type
      block = Block(shape,self.win) # create block <see Block Class>
      click = self.checkClick(block) # see checkClick method
      if click == "Enter": # pause game if user clicks <Enter>
        self.win.getMouse()
      elif click == "ESC": # end game if user presses <Enter>
        break
      sleep(0.1)
      while self.baseClear(block): # move block down as while its base is clear
                                   # of other blocks <see baseClear method>
        block.moveDown()
        click = self.checkClick(block)
        if click == "Return": # pause game if user presses <Enter>
          self.introText.setText('game paused...\nclick any key to continue')
          self.introText.draw(self.win)
          self.win.getKey()
          self.introText.undraw()
        elif click == "ESC": # break out of loop if user presses <ESC>
          break
        sleep(self.time)
      if click == "ESC": #end game if user pressed <ESC> in the prior loop
        break

      # add all squares in block to the list of all squares
      for square in block.getBlock():
        self.squarelist.append(square)
      self.addToLine(block) # add each square in block to its appropriate line
      A = self.checkLines(block)
      self.points += A #update points
      self.updateScore()  #print new score on window
      if self.points > 0 and self.points%100 == 0 and A != 0:
        self.time *= 0.9  # increase block speed
        self.level = self.level + 1 # increase level
        self.updateScore()  #print new level on screen
        if self.points == 2000:
          break # end game at 1000 points
    
    self.fareWell()

#-----------------------------------------------------------------------------#

  def updateScore(self):
    """
    This method updates the score and level display on the screen
    """

    self.scoreText.setText("Score: %d\nLevel: %d" % (self.points,self.level))

#-----------------------------------------------------------------------------#

  def fareWell(self):
    """
    This method prints the final game message
    """

    fareWell = "Game Over!\nYou had %d points.\nClick anywhere" % (self.points)
    fareWell = fareWell + " to quit."
    self.introText.setText(fareWell)
    self.introText.draw(self.win)
    self.win.getMouse()
    self.win.close()

#-----------------------------------------------------------------------------#

  def printHelp(self):
    """
    This method prints the instruction on the command line
    """

    print '*'*80
    intro = "\nWelcome to TETRIS v.1.0.\nBelow are the playing instructions:\n"
    intro = intro + "CONTROLS:\n========\n-->  Move Right\n<--  Move Left\n"
    intro = intro + "<Down Arrow>  Move Two Steps at a Time\n<Up Arrow>  "
    intro = intro + "Rotate Block\n\nPOINTS:\n======\n* Every complete line "
    intro = intro + "earns you 10 points\n* Every ten completed lines (100 poi"
    intro = intro + "nts) cause the blocks to drop faster\n* 200 completed lines"
    intro = intro + " (2000 points) ends the game which means..\n\nYou WON!\n\n"
    intro = intro + "You can press <ESC> at anytime to QUIT the game\nYou "
    intro = intro + "can press <ENTER> at anytime to pause the game\nENJOY..."
    intro = intro + "\n"
    print intro
    print '*'*80

#-----------------------------------------------------------------------------#

  def checkClick(self,block):
    """
    This method checks for user click
    Parameter(s): Block Object
    """

    click = self.win.checkKey()
    if click != None:  # if there was a user click
      # if user presses left arrow key and the leftside of block is clear
      # <see allLeftClear method>
      if click == "Left" and self.allLeftClear(block):
        block.moveLeft()
      # if user presses right arrow key and the rightside of block is clear
      # <see allRightClear method>
      elif click == "Right" and self.allRightClear(block):
        block.moveRight()
      # if user presses down arrow key and the base of block is clear
      elif click == "Down" and self.baseClear(block):
        block.moveDown()
      elif click == "Up": # rotate block if user presses up arrow key
        block.spin()
      elif click == "Escape": # if user presses <ESC> button
        return "ESC"
      elif click == "Return": # if user presses <ENTER>/<RETURN>
        return "Return"

#-----------------------------------------------------------------------------#

  def addToLine(self,block):
    """
    This method adds all the squares in a block to their respective list of
    lines.
    Parameter(s): Block Object
    """
    
    width = self.win.getWidth()
    for square in block.getBlock():
      squaresides = getSides(square)  # see <getSides function> in functions.py
      bottom = squaresides[-1]

      # add square to the appropriate list of lines
      for i in range(25):
        if int(bottom) == int((25-i)*0.1*width):
          self.lines[i].append(square)
    
#-----------------------------------------------------------------------------#

  def topClear(self):
    """
    This method checks if blocks have piled up to the top of the window.
    """

    for square in self.squarelist:
      sides = getSides(square) # get boundaries of square
      if int(sides[2]) <= 0:  # if top of any block is at the top of window
        return False
    
    return True

#-----------------------------------------------------------------------------#

  def baseClear(self,block):
    """
    This method checks if the base of a block is clear of any other block or if
    the block is at the bottom of the screen
    Parameter(s): Block Object
    """
   
    boundaries = block.getBoundaries()  # get coordinate boundaries of block
    bottom = int(boundaries[3])
    if bottom == self.win.getHeight():  # if block is at the base of window
      return False
    result = 0
    for square in block.getBlock():
      squaresides = getSides(square)  # get square boundaries
      for box in self.squarelist:
        boxsides = getSides(box)  # get box boundaries

        # check if base of square and top of box share the same y-coordinate and
        # if they share either the same left or right x-coordinate
        if int(squaresides[3]) == int(boxsides[2]) and \
            (int(squaresides[1]) == int(boxsides[1]) or \
            int(squaresides[0]) == int(boxsides[0])):
              result += 1
              # return False if any one such pair of square and box is found
              if result != 0:
                return False

    return True
        

#-----------------------------------------------------------------------------#

  def allLeftClear(self,block):
    """
    This method checks if the left side of a block is free of other blocks or
    the left side of the window
    Parameter(s): Block Object
    """
    
    # check if block is at the left end of window
    boundaries = block.getBoundaries()
    left = boundaries[0]
    #left = int(boundaries[0])
    if left <= 0:
      return False

    # check if the left side of block is clear of other blocks
    result = 0
    for square in block.getBlock():
      squaresides = getSides(square)
      for box in self.squarelist:
        boxsides = getSides(box)
        # check if the left side of square and the right side of box share the 
        # same x-coordinate and if they share the same top y-coordinate
        #if squaresides[0] <= boxsides[1] and squaresides[2] >= boxsides[2]:
        if int(squaresides[0]) == int(boxsides[1]) and \
            int(squaresides[2]) == int(boxsides[2]):
          result += 1
          if result != 0: # break loop and return False if any pair is found
            return False

    return True

#-----------------------------------------------------------------------------#

  def allRightClear(self,block):
    """
    This method checks if the right side of a block is free of other blocks or
    the right side of the window
    Parameter(s): Block Object
    """

    # check if block is at the right end of window
    boundaries = block.getBoundaries()
    right = int(boundaries[1])
    if right >= self.win.getWidth():
      return False

    # check if the right side of block is clear of other blocks
    result = 0
    for square in block.getBlock():
      squaresides = getSides(square)
      for box in self.squarelist:
        boxsides = getSides(box)
        # check if the right side of square and the left side of box share the 
        # same x-coordinate and if they share the same top y-coordinate
        #if squaresides[1] >= boxsides[0] and squaresides[2] == boxsides[2]:
        if int(squaresides[1]) == int(boxsides[0]) and \
            int(squaresides[2]) == int(boxsides[2]):
          result += 1
          if result != 0: # break loop and return False if any pair is found
            return False

    return True

#-----------------------------------------------------------------------------#

  def checkLines(self,block):
    """
    This method checks if any row of the window is filled with squares
    Parameter(s): Block Object
    Returns: Number of points earned (10 points per completed row)
    """
    
    if self.baseClear(block) == False: # check rows only when block stops moving
      completeLines = 0  # initiate number of complete rows
      i = 0
      while i <= 24:  # check all until the last (top) row
        line = self.lines[i]
        if len(line) == 10: # 10 squares fill a row on the window
          completeLines += 1

          # set color of all squares in completed row to grey
          for m in range(len(line)):
            square = line[m]
            square.setFill('grey')
          
          sleep(0.5)

          # undraw and remove all squares in the row from the general list of
          # all squares
          for n in range(len(line)):
            square = line[n]
            self.squarelist.remove(square)
            square.undraw()
            sleep(0.05)
          
          sleep(0.7)

          # create a list of all lists (rows) above the completed row
          aboveLine = self.lines[(i+1):]
          # move all squares above completed row one step down
          for lines in aboveLine:
            if len(lines) != 0:
              for squares in lines:
                squares.move(0,0.1*self.win.getWidth())
          
          self.lines.remove(line)  # delete list correponding to completed row
          self.lines.append([]) # add a new empty list as the topmost row since
                                # all rows above completed row are now one step
                                # down (index-wise) due to the removal of the
                                # full list (completed row).
          # the counter i is not increased here because if for example, the i-th
          # and (i+1)th rows are filled; the i-th row is removed, then the
          # (i+1)th row moves down and becomes the new i-th row, thus the i-th 
          # row has to be checked again.
        else: # if line is not full, move to next line (next list)
          i = i + 1
    
    points = completeLines*10 # calculate points earned
    
    return points
  
#-----------------------------------------------------------------------------#

def main():
  """
  Test program to run Game
  """

  game = Tetris()
  print game
  game.play()
  print game

#-----------------------------------------------------------------------------#
if __name__ == "__main__": main()
