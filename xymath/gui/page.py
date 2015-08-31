
from Tkinter import *

class TabPage(object):
    
    def leavePageCallback(self):
        '''When leaving page, tidy up any issues.'''
        print 'Leaving TabPage'
        
    def selectPageCallback(self):
        '''When entering page, do a little setup'''
        print 'Entering TabPage'
            
    def __init__(self, guiObj, pageFrame):
        
        
        self.guiObj = guiObj
        self.pageFrame = pageFrame
