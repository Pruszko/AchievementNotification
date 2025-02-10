from achievementnotification.battle import BattleListener
from achievementnotification.utils.achievement_registry import AchievementRegistry


class DefenderListener(BattleListener):

    def start(self):
        self.battleSession.onPlayerCaptureDrop += self._onPlayerCaptureDrop

    def stop(self):
        self.battleSession.onPlayerCaptureDrop -= self._onPlayerCaptureDrop

    def _onPlayerCaptureDrop(self):
        if self.hasAlreadyDisplayed(AchievementRegistry.DEFENDER):
            return

        if self.battleSession.playerCaptureDropsSum >= 70:
            self.display(AchievementRegistry.DEFENDER)
