from achievementnotification.utils import createLogger

logger = createLogger(__name__)


class AchievementNotificationMod(object):

    @property
    def achievementNotificationFlash(self):
        return self.__achievementNotificationFlash

    @property
    def isModsSettingsApiPresent(self):
        return self.__isModsSettingsApiPresent

    def __init__(self):
        self.__isModsSettingsApiPresent = False
        self.__achievementNotificationFlash = None

    def init(self):
        # try-except with logged exception here is more than important, because
        # when mod is initialized and some incompatibility occurs, it may break this (or other) mods
        # mainly because:
        # - AttributeError is silently ignored by mod loading code
        #   what can lead to very weird "lack of errors" where game state is corrupted
        #   due to unexpected module loading errors
        # - other exceptions may basically break loading of other mods
        #
        # by this, at least we will see what is broken
        try:
            logger.info("Initializing AchievementNotification mod ...")

            # it is good to know from the logs which client may have compatibility problems
            # it's not obviously logged anywhere by any client, or I am just blind
            from achievementnotification.utils import getClientType
            logger.info("Client type: %s", getClientType())

            # load translations as early as possible
            from achievementnotification.settings import translations
            translations.loadTranslations()

            # make sure to invoke all hooks
            import achievementnotification.hooks

            # handle all soft dependencies
            self.__resolveSoftDependenciesSafely()
            if self.isModsSettingsApiPresent:
                from achievementnotification.support import mods_settings_api_support

                mods_settings_api_support.registerSoftDependencySupport()

            # load config
            from achievementnotification.settings.config import g_config
            g_config.reloadSafely()

            # instantiate flash app - it can be present entire game
            from achievementnotification.flash.achievement_notification_flash import AchievementNotificationFlash
            self.__achievementNotificationFlash = AchievementNotificationFlash()
            self.__achievementNotificationFlash.active(True)

            # trigger event listening for battle stats collector
            # because otherwise it is not referenced anywhere
            from achievementnotification.battle import battle_state_collector

            logger.info("AchievementNotification mod initialized")
        except Exception:
            logger.error("Error occurred while initializing AchievementNotification mod", exc_info=True)

            from achievementnotification.utils import displayDialog
            displayDialog("Error occurred while initializing AchievementNotification mod.\n"
                          "Contact mod developer with error logs for further support.")

    def __resolveSoftDependenciesSafely(self):
        try:
            from gui.modsSettingsApi import g_modsSettingsApi

            # if something crashed in ModsSettingsAPI, then singleton may be None
            self.__isModsSettingsApiPresent = g_modsSettingsApi is not None

            if not self.isModsSettingsApiPresent:
                logger.warn("Error probably occurred in ModsSettingsAPI because it is None, ignore its presence.")
        except ImportError:
            self.__isModsSettingsApiPresent = False
        except Exception:
            logger.warn("Error occurred in ModsSettingsAPI, ignore its presence.", exc_info=True)
            self.__isModsSettingsApiPresent = False

    def fini(self):
        self.__achievementNotificationFlash.close()
        self.__achievementNotificationFlash = None


g_achievementNotificationMod = AchievementNotificationMod()
