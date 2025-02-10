from achievementnotification.battle import BattleListener
from achievementnotification.utils.achievement_registry import AchievementRegistry


class KamikazeListener(BattleListener):

    def start(self):
        self.battleSession.onPlayerKill += self._handleMedalCondition

    def stop(self):
        self.battleSession.onPlayerKill -= self._handleMedalCondition

    def _handleMedalCondition(self):
        if self.hasAlreadyDisplayed(AchievementRegistry.KAMIKAZE):
            return

        killsOfHigherTierByRamming = self.battleSession.playerKillsOfEnemyBy(
            lambda killEvent: killEvent.isAttackReasonRam and
                              killEvent.killer.vehicleLevel < killEvent.victim.vehicleLevel
        )

        if killsOfHigherTierByRamming > 0:
            self.display(AchievementRegistry.KAMIKAZE)
