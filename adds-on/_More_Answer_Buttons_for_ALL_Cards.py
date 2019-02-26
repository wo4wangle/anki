﻿# -*- mode: Python ; coding: utf-8 -*-
# • More Answer Buttons for ALL Cards
# https://ankiweb.net/shared/info/755044381
# https://github.com/ankitest/anki-musthave-addons-by-ankitest
# -- tested with Anki 2.0.44 under Windows 7 SP1
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016-2017 Dmitry Mikheev, http://finpapa.ucoz.net/
# No support. Use it AS IS on your own risk.
"""
 Adds 1-4 (4 by default) extra answer buttons with regular intervals.
  No answer on that card will be given, just setup additional interval.

 You can assign you own intervals, labels.
  Hotkeys are 6, 7, 8, 9.
 You can use intervals as button labels
  View - Answer buttons without labels or Ctrl+Alt+Shift+L

 On Cards - Later, Not Now menu click (Escape hotkey):
 No answer will be given, next card will be shown.
 Card stays on its place in queue,
 you'll see it next time you study the deck.
"""
from __future__ import division
from __future__ import unicode_literals
import os
import sys
import datetime
import random
import json

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import anki.hooks
import anki.utils
import aqt.main
import aqt.reviewer
import aqt.utils

# Get language class
import anki.lang
lang = anki.lang.getLang()

MSG = {
    'en': {
        'later': _('later'),
        'not now': _('not now'),
        'Cards': _('&Cards'),
        'View': _('&View'),
        'Later, not now': _('&Later, not now'),
        'no_labels': _('&Answer buttons without labels'),
        },
    'ru': {
        'later': 'позже',
        'not now': 'не сейчас',
        'Cards': '&Карточки',
        'View': '&Вид',
        'Later, not now': 'Позж&е, не сейчас',
        'no_labels': '&Кнопки оценок - без меток',
        },
    }

try:
    MSG[lang]
except KeyError:
    lang = 'en'

HOTKEY = {
    'no_labels': QKeySequence('Ctrl+Alt+Shift+L'),
    'later_not_now': 'Escape',
    }

# Anki uses a single digit to track which button has been clicked.
NOT_NOW_BASE = 5

# We will use shortcut number from the first extra button
#  and above to track the extra buttons.
INTERCEPT_EASE_BASE = 6

extra_buttons = [  # should start from 6 anyway
    {'Description': '5-7d', 'Label': '!!!',
        'ShortCut': '6', 'ReschedMin': 5, 'ReschedMax': 7},
    {'Description': '8-15d', 'Label': 'Veni',
        'ShortCut': '7', 'ReschedMin': 8, 'ReschedMax': 15},
    {'Description': '3-4w', 'Label': 'Vidi',
        'ShortCut': '8', 'ReschedMin': 15, 'ReschedMax': 30},
    {'Description': '2-3mo', 'Label': 'Vici',
        'ShortCut': '9', 'ReschedMin': 31, 'ReschedMax': 90},
]

# Must be four or less
assert len(extra_buttons) <= 4

SWAP_TAG = False
# SWAP_TAG = datetime.datetime.now().strftime(
#    'rescheduled::re-%Y-%m-%d::re-card')
# SWAP_TAG = datetime.datetime.now().strftime('re-%y-%m-%d-c')

USE_INTERVALS_AS_LABELS = False  # True #

"""
Adds extra buttons to the reviewer window for new cards
https://ankiweb.net/shared/info/468253198

Copyright: Steve AW <steveawa@gmail.com>
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

Modified by Glutanimate, 2016

WARNING: this addon uses private methods to achieve its goals. Use at your
own risk and keep backups.

What it does: Adds anywhere between 1 to 4 new buttons to the review window
when reviewing a new card. The new buttons function like the existing "Easy"
button, but in addition, they reschedule the card to different interval,
 which is randomly assigned between a lower and upper limit that is preset
  by the user (see below).

By default 3 buttons are added, with intervals: "3-4d" , "5-7d" , "8-15d"
This can be changed below.

I wanted this addon because many of my new cards do not need to be
"Learned" as I created and added them myself, typically an hour or so before
my first review session. I often add around 100-200 new cards per day, all on
a related topic, and this addon allows me to spread the next review
 of the new cards that don't need learning out in time.

How it works: This addon works by intercepting the creation of the reviewer
  buttons and adds up to 4 extra buttons to the review window.
   The answer function
  is wrapped and the ease parameter is checked to see if it one of the new
  buttons. If it is, the standard answer function is used to add the card
  as an easy card, and then the browser 'reschedCards' function is used
  to reschedule it to the desired interval.

In summary, this functions as if you click the "Easy" button on a new card,
  and then go to the browser and reschedule the card.

Warning: This completely replaces the Reviewer._answerButtons fn,
 so any changes
   to that function in future updates will be lost. Could ask for a hook?
Warning: buyer beware ... The author is not a python, nor a qt programmer

Support: None. Use at your own risk. If you do find a problem please email me
at steveawa@gmail.com

Setup data
List of dicts, where each item of the list (a dict) is the data
for a new button.
This can be edited to suit, but there can not be more than 4 buttons.

Description ... appears above the button
Label ... the label of the button
ShortCut ... the shortcut key for the button

ReschedMin ... same as the lower number
    in the Browser's "Edit/Rescedule" command
ReschedMax ... same as the higher number
    in the Browser's "Edit/Rescedule" command
"""

__addon__ = "'" + __name__.replace('_', ' ')
__version__ = "2.0.44a"

old_addons = (
    'Answer_Key_Remap.py',
    'Bigger_Show_Answer_Button.py',
    'Button_Colours_Good_Again.py',
    'Bigger_Show_All_Answer_Buttons.py',
    'More_Answer_Buttons_for_New_Cards.py',
    '_Again_Hard.py',
    '_Again_Hard_Good_Easy_wide_big_buttons.py',
    '_Later_not_now_button.py',
)

old_addons2delete = ''
for old_addon in old_addons:
    if len(old_addon) > 0:
        old_filename = os.path.join(aqt.mw.pm.addonFolder(), old_addon)
        if os.path.exists(old_filename):
            old_addons2delete += old_addon[:-3] + ' \n'

if old_addons2delete != '':
    if lang == 'ru':
        aqt.utils.showText(
            'В каталоге\n\n ' + aqt.mw.pm.addonFolder() +
            '\n\nнайдены дополнения, которые уже включены в дополнение\n' +
            ' More Answer Buttons for ALL Cards  \n' +
            'и поэтому будут конфликтовать с ним.\n\n' +
            old_addons2delete +
            '\nУдалите эти дополнения и перезапустите Anki.')
    else:
        aqt.utils.showText(
            '<big>There are some add-ons in the folder <br>\n<br>\n' +
            ' &nbsp; ' + aqt.mw.pm.addonFolder() +
            '<pre>' + old_addons2delete + '</pre>' +
            'They are already part of<br>\n' +
            ' <b> &nbsp; ~ More Answer Buttons for ALL Cards</b>' +
            ' addon.<br>\n' +
            'Please, delete them and restart Anki.</big>', type="html")

##


def _bottomTime(self, i):
    if not self.mw.col.conf['estTimes']:
        return '&nbsp;'
    txt = self.mw.col.sched.nextIvlStr(self.card, i, True) or '&nbsp;'
    return txt

# todo: brittle. Replaces existing function


def _reschedCards(self, ids, imin, imax, indi=2500):
    "Put cards in review queue with a new interval in days (min, max)."
    d = []
    t = self.today
    mod = anki.utils.intTime()
    for id in ids:
        r = random.randint(imin, imax)
        d.append(dict(id=id, due=r + t, ivl=max(1, r), mod=mod,
                      usn=self.col.usn(), fact=indi))
    self.remFromDyn(ids)
    self.col.db.executemany("""
update cards set type=2,queue=2,ivl=:ivl,due=:due,odue=0,
usn=:usn,mod=:mod,factor=:fact where id=:id""", d)
    self.col.log(ids)


def _answerButtons(self, _old):
    _old(self)

    times = []
    default = self._defaultEase()

    def but(i, label):
        if i == default:
            extra = 'id=defease'
        else:
            extra = ''
        if USE_INTERVALS_AS_LABELS:
            due = _bottomTime(self, i)
            return '''
<td align=center class="but but%s"><span class=nobold>&nbsp;</span><br>
<button %s title="%s" onclick="py.link('ease%d');">\
%s</button></td>''' % (i, extra, _('Shortcut key: %s') % i, i, due)
        else:
            due = self._buttonTime(i)
            return '''
<td align=center class="but but%s">%s<button %s title="%s"
onclick="py.link('ease%d');">\
%s</button></td>''' % (i, due, extra, _('Shortcut key: %s') % i, i, label)

    buf = '''<style>
body { overflow: hidden; }
.but,.but button{color:#c33;}'''
    if 2 == default:
        buf += '''
.but2,.but2 button{color:#090;}
.but3,.but3 button{color:#66f;}'''
    else:
        buf += '''
.but2,.but2 button{color:darkgoldenrod;}
.but3,.but3 button{color:#090;}
.but4,.but4 button{color:#66f;}'''
    buf += '''
.but,.but button { font-weight: bold; }
</style><center><table cellpading=0 cellspacing=0><tbody><tr>'''
    if USE_INTERVALS_AS_LABELS:
        buf += '''
<td align=center><span class=nobold>&nbsp;</span><br><button
 title="Short key: %s" onclick="py.link('ease%d');">\
%s</button></td><td>&nbsp;</td>''' % (
            'Escape', NOT_NOW_BASE, MSG[lang]['later'])
    else:
        buf += '''
<td align=center><span class=nobold>%s</span><br><button
title="Short key: %s" onclick="py.link('ease%d');">\
%s</button></td><td>&nbsp;</td>''' % (
            MSG[lang]['later'],
            'Escape', NOT_NOW_BASE, MSG[lang]['not now'])

    for ease, label in self._answerButtonList():
        buf += but(ease, label)
        # swAdded start ====>
    # Only for cards in the new queue
    if self.card.type in (0, 1, 2, 3):  # New, Learn, Day learning
        # Check that the number of answer buttons is as expected.
        #  assert self.mw.col.sched.answerButtons(self.card) == 3
        # python lists are 0 based
        for i, buttonItem in enumerate(extra_buttons):
            if USE_INTERVALS_AS_LABELS:
                buf += '''
<td align=center><span class=nobold>&nbsp;</span><br>
<button title="%s" onclick="py.link('ease%d');">\
%s</button></td>''' % (_('Shortcut key: %s') % buttonItem['ShortCut'],
                       i + INTERCEPT_EASE_BASE, buttonItem['Description'])
            else:
                buf += '''
<td align=center><span class=nobold>%s</span><br><button title="%s"
onclick="py.link('ease%d');">\
%s</button></td>''' % (
                    buttonItem['Description'], _('Shortcut key: %s') % (
                        buttonItem['ShortCut']),
                    i + INTERCEPT_EASE_BASE, buttonItem['Label'])
            # swAdded end
    buf += '</tr></tbody></table>'
    script = "<script>$(function () { $('#defease').focus(); });</script>"
    return buf + script

# This wraps existing Reviewer._answerCard function.


def answer_card_intercepting(self, actual_ease, _old):
    ease = actual_ease
    if actual_ease == NOT_NOW_BASE:
        self.nextCard()
        return True
    else:
        ease = actual_ease
        was_new_card = self.card.type in (0, 1, 2, 3)
        is_extra_button = was_new_card and actual_ease >= INTERCEPT_EASE_BASE
        if is_extra_button:
            # Make sure this is as expected.
            # assert self.mw.col.sched.answerButtons(self.card) == 3
            # So this is one of our buttons.
            # First answer the card as if 'Easy' clicked.
            ease = 3
            # We will need this to reschedule it.
            prev_card_id = self.card.id
            prev_card_factor = self.card.factor
            #
            buttonItem = extra_buttons[actual_ease - INTERCEPT_EASE_BASE]
            # Do the reschedule.
            self.mw.checkpoint(_('Reschedule card'))
            # self.mw.col.sched.reschedCards([prev_card_id],
            #   buttonItem['ReschedMin'], buttonItem['ReschedMax'])
            _reschedCards(self.mw.col.sched, [prev_card_id],
                          buttonItem['ReschedMin'], buttonItem['ReschedMax'],
                          indi=prev_card_factor)
            aqt.utils.tooltip('<center>Rescheduled:' + '<br>' +
                    buttonItem['Description'] + '</center>')

            SwapTag = SWAP_TAG
            if SwapTag:
                SwapTag += unicode(self.mw.reviewer.card.ord + 1)
                note = self.mw.reviewer.card.note()
                if not note.hasTag(SwapTag):
                    note.addTag(SwapTag)
                    note.flush()  # never forget to flush

            self.mw.reset()
            return True
        else:
            ret = _old(self, ease)
            return ret

# Handle the shortcut. Used changekeys.py addon as a guide


def keyHandler(self, evt, _old):
    key = unicode(evt.text())
    if self.state == 'answer':
        for i, buttonItem in enumerate(extra_buttons):
            if key == buttonItem['ShortCut']:
                # early exit ok in python?
                return self._answerCard(i + INTERCEPT_EASE_BASE)
    return _old(self, evt)


def more_proc():
    global USE_INTERVALS_AS_LABELS
    if more_action.isChecked():
        USE_INTERVALS_AS_LABELS = True
    else:
        USE_INTERVALS_AS_LABELS = False
    rst = aqt.mw.reviewer.state == 'answer'
    aqt.mw.reset()
    if rst:
        aqt.mw.reviewer._showAnswerHack()


def newRemaining(self):
    if not self.mw.col.conf['dueCounts']:
        return 0
    idx = self.mw.col.sched.countIdx(self.card)
    if self.hadCardQueue:
        # if it's come from the undo queue, don't count it separately
        counts = list(self.mw.col.sched.counts())
    else:
        counts = list(self.mw.col.sched.counts(self.card))
    return (idx == 0 and counts[0] < 1)


def _showAnswerButton(self, _old):
    _old(self)

    if newRemaining(self):
        self.mw.moveToState('overview')
    self._bottomReady = True
    if not self.typeCorrect:
        self.bottom.web.setFocus()

    buf = '''
<td align=center class=stat2><span class=stattxt>%s</span><br>
<button title="Short key: %s" onclick="py.link('ease%d');">\
%s</button></td><td>&nbsp;</td>''' % (
        MSG[lang]['later'],
        'Escape', NOT_NOW_BASE,
        MSG[lang]['not now'])

    middle = '''<table cellpadding=0><tbody>
<tr>%s<td class=stat2 align=center>
<span class=stattxt>%s</span><br>
<button %s id=ansbut style="display:inline-block;width:%s;%s"
onclick="py.link('ans');">%s</button>
    </td></tr></tbody></table>
''' % (buf, self._remaining(),
        ' title=" ' + (_('Shortcut key: %s') % _('Space')) + ' "',
        '99%', '', _('Show Answer'))

    if self.card.shouldShowTimer():
        maxTime = self.card.timeLimit() / 1000
    else:
        maxTime = 0
    self.bottom.web.eval('showQuestion(%s,%d);' % (
        json.dumps(middle), maxTime))
    return True

if old_addons2delete == '':
    try:
        aqt.mw.addon_view_menu
    except AttributeError:
        aqt.mw.addon_view_menu = QMenu(MSG[lang]['View'], aqt.mw)
        aqt.mw.form.menubar.insertMenu(
            aqt.mw.form.menuTools.menuAction(), aqt.mw.addon_view_menu)

    more_action = QAction(MSG[lang]['no_labels'], aqt.mw)
    more_action.setShortcut(HOTKEY['no_labels'])
    more_action.setCheckable(True)
    more_action.setChecked(USE_INTERVALS_AS_LABELS)
    aqt.mw.connect(more_action, SIGNAL('triggered()'), more_proc)
    aqt.mw.addon_view_menu.addAction(more_action)

    aqt.reviewer.Reviewer._keyHandler = anki.hooks.wrap(
        aqt.reviewer.Reviewer._keyHandler, keyHandler, 'around')

    aqt.reviewer.Reviewer._answerButtons = anki.hooks.wrap(
        aqt.reviewer.Reviewer._answerButtons, _answerButtons, 'around')

    aqt.reviewer.Reviewer._answerCard = anki.hooks.wrap(
        aqt.reviewer.Reviewer._answerCard, answer_card_intercepting, 'around')

    #

    def onEscape():
        aqt.mw.reviewer.nextCard()

    try:
        aqt.mw.addon_cards_menu
    except AttributeError:
        aqt.mw.addon_cards_menu = QMenu(MSG[lang]['Cards'], aqt.mw)
        aqt.mw.form.menubar.insertMenu(
            aqt.mw.form.menuTools.menuAction(), aqt.mw.addon_cards_menu)

    escape_action = QAction(aqt.mw)
    escape_action.setText(MSG[lang]['Later, not now'])
    escape_action.setShortcut(HOTKEY['later_not_now'])
    escape_action.setEnabled(False)
    aqt.mw.connect(escape_action, SIGNAL('triggered()'), onEscape)

    # aqt.mw.addon_cards_menu.addSeparator()
    aqt.mw.addon_cards_menu.addAction(escape_action)
    # aqt.mw.addon_cards_menu.addSeparator()

    aqt.mw.deckBrowser.show = anki.hooks.wrap(
        aqt.mw.deckBrowser.show, lambda: escape_action.setEnabled(False))
    aqt.mw.overview.show = anki.hooks.wrap(
        aqt.mw.overview.show, lambda: escape_action.setEnabled(False))
    aqt.mw.reviewer.show = anki.hooks.wrap(
        aqt.mw.reviewer.show, lambda: escape_action.setEnabled(True))

    #

    aqt.reviewer.Reviewer._showAnswerButton = anki.hooks.wrap(
        aqt.reviewer.Reviewer._showAnswerButton, _showAnswerButton, 'around')
