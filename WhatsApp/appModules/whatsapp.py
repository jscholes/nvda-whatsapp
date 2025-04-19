from enum import Enum
import addonHandler
import appModuleHandler
from controlTypes import Role
from logHandler import log


addonHandler.initTranslation()


class WAAutomationID(Enum):
	CHAT_LIST = 'ChatList'

	def __str__(self):
		return self.value


CHAT_LIST_SUFFIX = ' list'

def trimChatListName(obj):
	obj.name = obj.name.removesuffix(CHAT_LIST_SUFFIX)


_automationIDTransforms = {
	WAAutomationID.CHAT_LIST: frozenset({trimChatListName}),
}


class AppModule(appModuleHandler.AppModule):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		log.info('WhatsApp::WhatsApp add-on initialised.')

	def event_NVDAObject_init(self, obj):
		try:
			automationID = WAAutomationID(obj.UIAAutomationId)
		except ValueError:
			automationID = None

		if automationID:
			for transform in _automationIDTransforms.get(automationID, set()):
				try:
					transform(obj)
				except Exception:
					log.exception('WhatsApp::Error while applying transform %r for obj with automation ID "%s".', transform, automationID)
					continue

		uiaElement = getattr(obj, 'UIAElement')
		if (
			uiaElement and
			obj.role == Role.WINDOW and
			uiaElement.cachedClassName == 'Windows.UI.Core.CoreWindow'
		):
			obj.name = ''
