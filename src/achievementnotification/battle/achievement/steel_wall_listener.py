import BigWorld

from achievementnotification.battle import BattleListener
from achievementnotification.utils.achievement_registry import AchievementRegistry


class SteelWallListener(BattleListener):

    def start(self):
        self.battleSession.onPlayerBlockedDamage += self._handleMedalCondition
        self.battleSession.onPlayerReceivedDamage += self._handleMedalCondition
        self.battleSession.onPlayerReceivedHit += self._handleMedalCondition

    def stop(self):
        self.battleSession.onPlayerBlockedDamage -= self._handleMedalCondition
        self.battleSession.onPlayerReceivedDamage -= self._handleMedalCondition
        self.battleSession.onPlayerReceivedHit -= self._handleMedalCondition

    def _handleMedalCondition(self):
        if self.hasAlreadyDisplayed(AchievementRegistry.STEEL_WALL):
            return

        blockedDamage = self.battleSession.playerBlockedDamageOfEnemy
        receivedDamage = self.battleSession.playerReceivedDamageOfEnemy
        receivedHits = self.battleSession.playerReceivedHitsOfEnemy
        isAlive = BigWorld.player().isVehicleAlive

        if receivedHits >= 11 and (blockedDamage + receivedDamage) >= 1000 and isAlive:
            self.display(AchievementRegistry.STEEL_WALL)
