import os

from achievementnotification.settings import copy, deleteEmptyFolderSafely, toBool, ConfigException
from achievementnotification.settings.config_file import g_configFiles
from achievementnotification.utils import createLogger


logger = createLogger(__name__)


class ConfigVersion(object):

    V1_0_0 = 1

    CURRENT = V1_0_0


def performConfigMigrations():
    try:
        if not g_configFiles.config.exists():
            return

        configDict = g_configFiles.config.loadConfigDict()

        if isVersion(configDict, ConfigVersion.CURRENT):
            return

        # nothing to migrate yet

        g_configFiles.config.writeConfigDict(configDict)
    except ConfigException:
        logger.error("Failed to perform config file migration.")
        raise
    except Exception:
        logger.error("Failed to perform config file migration.", exc_info=True)
        raise ConfigException("Failed to perform config file migration due to unknown error.\n"
                              "Contact mod developer for further support with provided logs.")


def progressVersion(configDict):
    if "__version__" not in configDict:
        configDict["__version__"] = ConfigVersion.V1_0_0
        return

    configDict["__version__"] = int(configDict["__version__"]) + 1


def isVersion(configDict, version):
    if "__version__" not in configDict:
        return ConfigVersion.V1_0_0 == version

    return int(configDict["__version__"]) == version
