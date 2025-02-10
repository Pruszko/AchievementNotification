from achievementnotification.battle import BattleListener
from achievementnotification.utils.achievement_registry import AchievementRegistry


class ScoutListener(BattleListener):

    def start(self):
        self.battleSession.onPlayerSpottedEnemy += self._onPlayerSpottedEnemy

    def stop(self):
        self.battleSession.onPlayerSpottedEnemy -= self._onPlayerSpottedEnemy

    def _onPlayerSpottedEnemy(self):
        if self.hasAlreadyDisplayed(AchievementRegistry.SCOUT):
            return

        if self.battleSession.playerSpottedEnemyCount >= 9:
            self.display(AchievementRegistry.SCOUT)
