# Date:     January 27, 2016
# Author:   Benjamin Gray
# File:     Quick_Reschedule.py
# Purpose:  Quickly reschedule cards in anki to a user specified interval using sched.reschedCards()
# Version:  0.2

reschedule_shortcut = '.'
reschedule_four_weeks = 'm'
reschedule_tomorrow = 'q'

from aqt import mw
from aqt.utils import tooltip, getText
from aqt.reviewer import Reviewer

# prompt for new interval, and set it

def promptNewInterval(self, card):

    dayString = getText("Number of days until next review: ")
    try:
        days = int(dayString[0])
    except ValueError:
        return

    if days > 0:
        mw.col.sched.reschedCards( [card.id], days, days )
        tooltip('Rescheduled for review in ' + str(days) + ' days'  )
        mw.reset()

# replace _keyHandler in reviewer.py to add a keybinding

def newKeyHandler(self, evt):
    key = unicode(evt.text())
    card = mw.reviewer.card
    if key == reschedule_shortcut:
        mw.checkpoint(_("Reschedule card"))
        promptNewInterval(self, card)
    elif key == reschedule_four_weeks:
        mw.checkpoint(_("Reschedule card"))
        mw.col.sched.reschedCards( [card.id], 21, 42 )
        tooltip('Rescheduled for review in 3-6 weeks'  )
        mw.reset()
    elif key == reschedule_tomorrow:
        mw.checkpoint(_("Reschedule card"))
        mw.col.sched.reschedCards( [card.id], 1, 1 )
        tooltip('Rescheduled for review tomorrow'  )
        mw.reset()
    else:
        origKeyHandler(self, evt)

origKeyHandler = Reviewer._keyHandler
Reviewer._keyHandler = newKeyHandler

