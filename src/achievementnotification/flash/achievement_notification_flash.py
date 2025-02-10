import GUI
import SCALEFORM
from gui import DEPTH_OF_Battle, g_guiResetters

from gui.Scaleform.daapi.view.external_components import ExternalFlashComponent, ExternalFlashSettings
from gui.Scaleform.flash_wrapper import InputKeyMode
from gui.Scaleform.framework.entities.BaseDAAPIModule import BaseDAAPIModule

from achievementnotification import createLogger
from achievementnotification.settings.config import g_config
from achievementnotification.settings.config_param import g_configParams
from achievementnotification.utils.achievement_registry import AchievementRegistry

logger = createLogger(__name__)


class AchievementNotificationFlashMeta(BaseDAAPIModule):

    def as_applyAchievementRegistry(self, serializedAchievementRegistry):
        if self._isDAAPIInited():
            self.flashObject.as_applyAchievementRegistry(serializedAchievementRegistry)

    def as_applyConfig(self, serializedConfig):
        if self._isDAAPIInited():
            self.flashObject.as_applyConfig(serializedConfig)

    def as_onRecreateDevice(self, screenWidth, screenHeight):
        if self._isDAAPIInited():
            self.flashObject.as_onRecreateDevice(screenWidth, screenHeight)

    def as_displayAchievement(self, achievementKey, extended):
        if self._isDAAPIInited():
            return self.flashObject.as_displayAchievement(achievementKey, extended)


class AchievementNotificationFlash(ExternalFlashComponent, AchievementNotificationFlashMeta):

    def __init__(self):
        super(AchievementNotificationFlash, self).__init__(
            ExternalFlashSettings("AchievementNotificationFlash",
                                  "AchievementNotificationFlash.swf",
                                  "root", None)
        )
        self.createExternalComponent()
        self._configureApp()

        self._onRecreateDevice()
        g_guiResetters.add(self._onRecreateDevice)

        self._initializeAchievementRegistry()

        self._onConfigReload()
        g_config.onConfigReload += self._onConfigReload

    def close(self):
        g_config.onConfigReload -= self._onConfigReload
        g_guiResetters.remove(self._onRecreateDevice)
        super(AchievementNotificationFlash, self).close()

    def _onConfigReload(self):
        self.as_applyConfig({
            "first-display-time": g_configParams.firstDisplayTime(),
            "consecutive-display-time": g_configParams.consecutiveDisplayTime(),
        })

    def _onRecreateDevice(self):
        screenWidth, screenHeight = GUI.screenResolution()[:2]
        self.as_onRecreateDevice(screenWidth, screenHeight)

    def _configureApp(self):
        # this is needed, otherwise everything will be white
        self.movie.backgroundAlpha = 0.0

        # scales the app to match 1:1 pixels of app to screen
        self.movie.scaleMode = SCALEFORM.eMovieScaleMode.NO_SCALE

        # it must be exactly like that, because:
        # - InputKeyMode.DEFAULT kinda breaks keyboard outside our app (who knows what more)
        # - InputKeyMode.NO_HANDLE basically breaks most click/down/up mouse based events in our app
        self.component.wg_inputKeyMode = InputKeyMode.IGNORE_RESULT

        # depth sorting, required to be placed properly between other apps
        self.component.position.z = DEPTH_OF_Battle + 0.02

        # don't capture focus
        self.component.focus = False
        self.component.moveFocus = False
        self.component.dragFocus = False

    def _initializeAchievementRegistry(self):
        self.as_applyAchievementRegistry({
            achievement.key: {
                "key": achievement.key,
                "extended": achievement.extended,
                "conditional": achievement.conditional,
                "text": achievement.text,
                "descriptionText": achievement.descriptionText,
                "descriptionStandardText": achievement.descriptionStandardText,
                "descriptionExtendedText": achievement.descriptionExtendedText,
                "conditionText": achievement.conditionText,
                "largeIconPath": achievement.largeIconPath
            } for achievement in AchievementRegistry.ALL_ACHIEVEMENTS
        })

    def displayAchievement(self, achievementKey, extended=False):
        self.as_displayAchievement(achievementKey, extended)
