import os

from achievementnotification.settings import copy, deleteEmptyFolderSafely, toBool, ConfigException
from achievementnotification.settings.config_file import g_configFiles
from achievementnotification.utils import createLogger


logger = createLogger(__name__)


class ConfigVersion(object):

    V1_0_X = 1
    V1_1_X = 2

    CURRENT = V1_1_X


def performConfigMigrations():
    try:
        if not g_configFiles.config.exists():
            return

        configDict = g_configFiles.config.loadConfigDict()

        if isVersion(configDict, ConfigVersion.CURRENT):
            return

        v1_1_0_addScalePositionAndCompactMode(configDict)

        g_configFiles.config.writeConfigDict(configDict)
    except ConfigException:
        logger.error("Failed to perform config file migration.")
        raise
    except Exception:
        logger.error("Failed to perform config file migration.", exc_info=True)
        raise ConfigException("Failed to perform config file migration due to unknown error.\n"
                              "Contact mod developer for further support with provided logs.")


def v1_1_0_addScalePositionAndCompactMode(configDict):
    if not isVersion(configDict, ConfigVersion.V1_0_X):
        return

    logger.info("Migrating config file from version 1.0.x to 1.1.x ...")

    configDict["scale"] = 1.0
    configDict["display-mode"] = "detailed"
    configDict["vertical-position"] = 0.8

    progressVersion(configDict)

    logger.info("Migration finished.")


def progressVersion(configDict):
    if "__version__" not in configDict:
        configDict["__version__"] = ConfigVersion.V1_0_X
        return

    configDict["__version__"] = int(configDict["__version__"]) + 1


def isVersion(configDict, version):
    if "__version__" not in configDict:
        return ConfigVersion.V1_0_X == version

    return int(configDict["__version__"]) == version
