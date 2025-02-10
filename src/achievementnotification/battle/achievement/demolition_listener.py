from achievementnotification.battle import BattleListener
from achievementnotification.utils.achievement_registry import AchievementRegistry


class DemolitionListener(BattleListener):

    def start(self):
        self.battleSession.onPlayerKill += self._handleMedalCondition

    def stop(self):
        self.battleSession.onPlayerKill -= self._handleMedalCondition

    def _handleMedalCondition(self):
        if self.hasAlreadyDisplayed(AchievementRegistry.DEMOLITION):
            return

        killsByAmmoRack = self.battleSession.playerKillsOfEnemyBy(
            lambda killEvent: killEvent.hasAmmoRackExploded
        )

        if killsByAmmoRack > 0:
            self.display(AchievementRegistry.DEMOLITION)
