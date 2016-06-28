# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 09:05:30 2016

@author: Marcel Gangwisch, Ruben Beck
"""
from UI import Main_ui
from PyQt4 import QtGui
import sys



def main():
    if __name__ == '__main__':
        app = QtGui.QApplication(sys.argv)
        window = Main_ui.Main_ui()
        sys.exit(app.exec_())    
    
main()
    
    