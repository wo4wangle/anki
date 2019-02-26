import aqt
import anki


def flipCard():
    if aqt.mw.reviewer.state == "question":
        aqt.mw.reviewer._showAnswerHack()
    elif aqt.mw.reviewer.state == "answer":
        aqt.mw.reviewer._showQuestion()


def keyHandler(self, evt, _old):
    key = unicode(evt.text())
    if key == "0":
        flipCard()
    else:
        return _old(self, evt)


aqt.reviewer.Reviewer._keyHandler = anki.hooks.wrap(
    aqt.reviewer.Reviewer._keyHandler, keyHandler, "around")
