"""
Author: Imoleayo Abel

Date: 27th April 2011

Program Description: The program defines a Block class that creates different
                     TETRIS blocks and defines various operations/methods on the
                     block like moving, spinning, changing color and many more.
                     <see Tetris class> for usage of blocks in a TETRIS game.
"""
 
from graphics import *
from random import *
from time import *
from math import *
from functions import *

class Block(object):

  """
  A class of block objects that creates different forms of TETRIS blocks.
  Parameters: A window, and the preferred block type (shape).
  """

  def __init__(self,shape,win):
    
    # set instance variables
    self.win = win
    self.color = choice(['red','yellow','blue'])
    w = win.getWidth()
    l = 0.1*w  #length of side of building squares that make up each block
    self.dx = self.dy = l
    self.shape = shape
    self.spinned = 0
    
    # set all possible points and rectangles required to build any TETRIS block
    # form
    p1 = Point(0.5*w,0)
    p2 = Point(0.4*w,l)
    p3 = Point(0.6*w,l)
    p4 = Point(0.3*w,2*l)
    p5 = Point(0.5*w,2*l)
    p6 = Point(0.7*w,2*l)

    r2 = Rectangle(p1,p2)
    r3 = Rectangle(p1,p3)
    r5 = Rectangle(p2,p4)
    r6 = Rectangle(p2,p5)
    r7 = Rectangle(p3,p5)
    r8 = Rectangle(p3,p6)

    self.block = None

    # choose and save in a list, squares that correspond to each block type
    if shape.lower() == "flat":
      self.block = [r5,r6,r7,r8]
    elif shape.lower() == "box":
      self.block = [r2,r3,r6,r7]
    elif shape.lower() == "rightz":
      self.block = [r2,r3,r7,r8]
    elif shape.lower() == "leftz":
      self.block = [r2,r3,r5,r6]
    elif shape.lower() == "rightl":
      self.block = [r2,r6,r7,r8]
    elif shape.lower() == "leftl":
      self.block = [r3,r5,r6,r7]
    elif shape.lower() == "tee":
      self.block = [r2,r5,r6,r7]
    
    # draw and fill squares
    for square in self.block:
      square.draw(win)
      square.setFill(self.color)
    
#-----------------------------------------------------------------------------#

  def __str__(self):
    """
    Returns a string of text describing a block when it is printed
    Parameter: None
    """

    s = "Block Type: %s" % (self.shape)
    s = s + "\nColor: %s" % (self.color)

    return s

#-----------------------------------------------------------------------------#
 
  def setColor(self,color):
    """
    Changes color of block
    Parameter: Desired color
    """

    for square in self.block:
      square.setFill(color)
        
#-----------------------------------------------------------------------------#
  
  def getBlock(self):
    """
    Returns list of squares that make up the block
    """

    return self.block

#-----------------------------------------------------------------------------#

  def getShape(self):
    """
    Returns the shape of the block
    """

    return self.shape.lower()

#-----------------------------------------------------------------------------#

  def isSpinned(self):
    """
    Returns integer that tells if block is in its original orientation or has
    been spinned
    """

    if self.spinned % 2 == 0: # blocks return to original orientation after
                              # two spins
      return False
    return True

#-----------------------------------------------------------------------------#
  
  def getBoundaries(self):
    """a
    Returns leftmost and rightmost x-coordinates of squares that make up the
    block as well as the topmost and lowest y-coordinates
    Parameters: None
    """

    allX = []
    allY = []
    
    for square in self.block:
      allX.append(square.getP1().getX())
      allX.append(square.getP2().getX())
      allY.append(square.getP1().getY())
      allY.append(square.getP2().getY())
      
    leftMost = getMin(allX)  #see functions.py for getMin and getMax functions
    rightMost = getMax(allX)
    topMost = getMin(allY)
    bottomMost = getMax(allY)

    return [leftMost,rightMost,topMost,bottomMost]

#-----------------------------------------------------------------------------#

  def moveLeft(self):
    """
    Moves block leftwards within the window
    """

    boundaries = self.getBoundaries()

    #check if block is beyond the left end or at the bottom of the window
    if int(boundaries[0]) >= self.dx and \
        int(boundaries[3]) <= self.win.getHeight():
      
      #move block leftwards
      for square in self.block: 
        square.move(-self.dx,0)

#-----------------------------------------------------------------------------#

  def moveRight(self):
    """
    Moves block rightwards within the window
    """

    boundaries = self.getBoundaries()

    #check if block is beyond the riht or at the bottom of the window
    if int(boundaries[1]) <= (self.win.getWidth() - self.dx) and \
        int(boundaries[3]) != self.win.getHeight():
      
      #move block rightwards
      for square in self.block:
        square.move(self.dx,0)

#-----------------------------------------------------------------------------#

  def moveDown(self):
    """
    Moves block downwards within the window
    """

    boundaries = self.getBoundaries()

    #check if block is one-squareside-length above the bottom of the window
    if int(boundaries[3]) <= (self.win.getHeight() - self.dy):
      
      #move block downwards
      for square in self.block:
        square.move(0,self.dy)

#-----------------------------------------------------------------------------#
    
  def spin(self):
    """
    Spins block over an angle of -90 degrees
    """
    
    l = 0.1*self.win.getWidth()  # length of square sides
    angle = -0.5*pi
    boundaries = self.getBoundaries()
    pivot = Point(int(boundaries[1]),int(boundaries[3]))
    
    #check is block is above the base of window
    if int(boundaries[3]) < self.win.getHeight():

      #spin every square in block
      for square in self.block:
        p1, p2 = square.getP1(), square.getP2()
        centerX = 0.5*(p1.getX() + p2.getX()) # x cordinate of square's center
        centerY = 0.5*(p1.getY() + p2.getY()) # y cordinate of square's center
        dx = centerX - boundaries[1]
        dy = centerY - boundaries[2]
        mx = (dx * (cos(angle) - 1)) - (dy * sin(angle))
        my = (dx * sin(angle)) + (dy * (cos(angle) - 1))
        square.move(mx,my)
      
      boundaries = self.getBoundaries() #get new boundaries of block

      #move block appropriately to account for the horizontal displacement due
      #to rotating
      if boundaries[0] > 2*l:
        for square in self.block:
          if self.shape == "box":
            square.move(-2*l,0)
          else:
            square.move(-3*l,0)
      elif boundaries[0] == 2*l:
        for square in self.block:
          square.move(-2*l,0)
      elif boundaries[0] == l:
        for square in self.block:
          square.move(-l,0)
      elif boundaries[0] == -l:
        for square in self.block:
          square.move(l,0)
      elif boundaries[0] == -2*l:
        for square in self.block:
          square.move(2*l,0)

    self.spinned += 1

#-----------------------------------------------------------------------------#
