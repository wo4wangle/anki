# Anki add-on "Multiple 'Add' and 'Browser' Windows"
# Filename: Multiple_Add_and_Browser_Windows.py
# Version: 1.1
# Developed by webventure.com.au
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Release notes:
#  1.0 20160614
#      - Initial release
#  1.1 20161204
#      - Allow multiple instances of all dialog types, not just AddCards.
#      - Prevent change of note type in one dialog from interfering with other dialogs

import aqt

class MultipleAddCardWindows_DialogManager(object):

	def __init__(self):
		self._singleInstanceDialogNames={} # List of dialog names that allow only a single instance. Possible values "AddCards", "Browser", "EditCurrent". This empty list means all dialogs allow multiple instances.
		self._openInstances=[]
		# Keep the same _dialogs name and structure as the original because other add-ons break python conventions and access it directly. (e.g. advanced browser)
		originalDialogManager=aqt.dialogs
		self._dialogs = originalDialogManager._dialogs

	def _getCreator(self, name):
		return self._dialogs[name][0]

	def open(self, name, *args):
		if name in self._singleInstanceDialogNames:
			# We could just look up the instance using self._dialogs[name][1] but we're only really maintaining that in case badly behaved add-ons use it, so look for an existing instance using the new data structure.
			for instance in self._openInstances:
				if name==instance._dialogName:
					instance.setWindowState(instance.windowState() | Qt.WindowActive)
					instance.activateWindow()
					instance.raise_()
					return instance
		creator=self._getCreator(name)
		instance=creator(*args)
		instance._dialogName=name
		self._openInstances.append(instance)
		self._dialogs[name][1]=instance
		return instance

	def close(self, name):
		# This method should be avoided as there's no way to know which instance to close. Use closeInstance instead.
		# Only removes the first instance of the specified name.
		for instance in self._openInstances:
			if name==instance._dialogName:
				self._openInstances.remove(instance)
				self._dialogs[name][1]=None
				return

	def closeInstance(self, instance):
		# Have to check if it's in the list first otherwise closeAll sometimes throws exceptions saying instance isn't in the list. Not sure how it happens though.
		if instance in self._openInstances:
			self._openInstances.remove(instance)
			self._dialogs[instance._dialogName][1]=None

	def closeAll(self):
		"True if all closed successfully."
		copyOfOpenInstances=list(self._openInstances)
		for instance in copyOfOpenInstances: # we're removing instances from self._openInstances as we go which causes problems if we don't iterate on a copy
			if not instance.canClose():
				return False
			instance.forceClose = True
			instance.close()
			self.closeInstance(instance)
		return True

aqt.dialogs = MultipleAddCardWindows_DialogManager()


# The following code prevents a change of note type in one AddCards dialog from affecting others.
# No idea why everything was coded to use global hooks in the first place, 
# or what repercussions there are for removing the reset hooks from AddCards and ModelChooser.
# It seems to work which is the main thing!

from aqt.addcards import AddCards

AddCards_onModelChangeMethodName='onModelChange' # Anki version 2.1+
try:
	AddCards.onModelChange # doesn't call it, just throws an error if it doesn't exist
except AttributeError:
	AddCards_onModelChangeMethodName='onReset' # Anki version 2.0
	# Patch the AddCards class to make onModelChange an alias for onReset so we can refer to it consistently in the code below.
	AddCards.onModelChange=AddCards.onReset

from anki.hooks import remHook

original_AddCards_init=AddCards.__init__
def modified_AddCards_init(self,mw):
	original_AddCards_init(self,mw)
	self.modelChooser.addCards=self
	#aqt.utils.showInfo("removing hook %s" % getattr(self,AddCards_onModelChangeMethodName))
	remHook('currentModelChanged',getattr(self,AddCards_onModelChangeMethodName))
	remHook('reset',self.onReset)
	remHook('reset',self.modelChooser.onReset)
AddCards.__init__=modified_AddCards_init

from aqt.modelchooser import ModelChooser

original_ModelChooser_onModelChange=ModelChooser.onModelChange
def modified_ModelChooser_onModelChange(self):
	original_ModelChooser_onModelChange(self)
	self.updateModels()
	addCards=getattr(self,'addCards',None)
	if addCards:
		addCards.onModelChange()
ModelChooser.onModelChange=modified_ModelChooser_onModelChange
