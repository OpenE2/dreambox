from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.config import config, ConfigSubsection, ConfigSelection, ConfigIP, ConfigEnableDisable, getConfigListEntry, ConfigText, ConfigInteger
from Components.ConfigList import ConfigListScreen

config.plugins.DMC = ConfigSubsection()
config.plugins.DMC.enable = ConfigEnableDisable(default = False)
config.plugins.DMC.host = ConfigText(default = 'open-dreambox.org', fixed_size = False)
config.plugins.DMC.port = ConfigInteger(default = 8184)
config.plugins.DMC.url = ConfigText(default = 'http://open-dreambox.org/dms/DreamboxMessageServer?action=receiver', fixed_size = False)
config.plugins.DMC.password = ConfigText(default = "", fixed_size = False)
config.plugins.DMC.timeout = ConfigInteger(default = 60, limits = (0,3660))
config.plugins.DMC.notify_state = ConfigEnableDisable(default = False)
