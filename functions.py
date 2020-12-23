"""
Author: Imoleayo Abel
Date: April 27, 2011
Program Description: The program contains functions used in the Block and Tetris
                     Classes.
""" 

from block import *
from graphics import *
from math import *

#-----------------------------------------------------#

def getMin(L):
  """
  Returns the minimum value in a list
  """
  
  if len(L) == 0:
    return None
  Min = L[0]
  for i in range(len(L)):
    if L[i] < Min:
      Min = L[i]
  return Min

#-----------------------------------------------------#

def getMax(L):
  """
  Returns the maximum value in a list
  """
  
  if len(L) == 0:
    return None
  Max = L[0]
  for i in range(len(L)):
    if L[i] > Max:
      Max = L[i]
  return Max

#------------------------------------------------------#

def getSides(square):
  """
  Returns a list containing the x-cordinate of the left,
  x-cordinate of the right,, y-cordinate of the top, and
  y-cordinate of the bottom of a rectangle
  """

  p1 = square.getP1()
  p2 = square.getP2()
  X = [p1.getX(),p2.getX()]
  Y = [p1.getY(),p2.getY()]
  sides = [getMin(X),getMax(X),getMin(Y),getMax(Y)]
  return sides

#-------------------------------------------------------#
