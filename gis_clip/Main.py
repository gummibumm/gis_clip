# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 09:05:30 2016

@author: Marcel Gangwisch, Ruben Beck
"""

from UI import Main_ui
from PyQt4 import QtGui
import sys

# define main entry point for program
def main():
    if __name__ == '__main__':
        # start a new QtGui Application
        app = QtGui.QApplication(sys.argv)
        # open new ui main window
        main_window = Main_ui.Main_ui()
        # close program on window shutdown
        sys.exit(app.exec_())    
    
main()
    
    