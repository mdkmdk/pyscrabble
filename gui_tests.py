#!/usr/bin/python2
# -*- coding: utf-8 -*-

"""
Modest first attempts at designing a GUI around a Scrabble game

"""

from PyQt4 import import QtGui
from first_tests import *

Class guiTile(QtGui.QLabel):
    
    def __init__(self, Tile):
#         super(Button, )
        self.setAcceptDrops(True)
        pass
        
    def dropEvent(self, e):
        # check that space is empty
        # insert tuple text
        pass
    
#     def 

def main():
    pass 
    
    
    
    
    

if __name__ == '__main__':
    main()