# import the main window object (mw) from aqt
from aqt import mw #wm.col tool
# import the "show info" tool from utils.py
from aqt.utils import showInfo # show box
# import all of the Qt GUI library
from aqt.qt import * ##q related fuc must import

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

def testFunction():
    # get the number of cards in the current collection, which is stored in
    # the main window
    cardCount = mw.col.cardCount() #count cards nums and give a var
    # show a message box
    showInfo("cardnum: %d" % cardCount) #give a window with words

# create a new menu item, "test"
action = QAction("wangle", mw) #non chinese character in note,action name
# set it to call testFunction when it's clicked
action.triggered.connect(testFunction) #to stat the fuc
# and add it to the tools menu
mw.form.menuTools.addAction(action) #add button in tool menu