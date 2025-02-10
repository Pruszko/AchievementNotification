from achievementnotification.battle import BattleListener
from achievementnotification.utils.achievement_registry import AchievementRegistry


class ArsonistListener(BattleListener):

    def start(self):
        self.battleSession.onPlayerKill += self._handleMedalCondition

    def stop(self):
        self.battleSession.onPlayerKill -= self._handleMedalCondition

    def _handleMedalCondition(self):
        if self.hasAlreadyDisplayed(AchievementRegistry.ARSONIST):
            return

        killsByFire = self.battleSession.playerKillsOfEnemyBy(
            lambda killEvent: killEvent.isAttackReasonFire
        )

        if killsByFire > 0:
            self.display(AchievementRegistry.ARSONIST)
