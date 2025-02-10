import BigWorld

from achievementnotification.battle import BattleListener, VehicleClass
from achievementnotification.utils.achievement_registry import AchievementRegistry


class MedalStarkListener(BattleListener):

    def start(self):
        self.battleSession.onPlayerKill += self._handleMedalCondition
        self.battleSession.onPlayerReceivedDamage += self._handleMedalCondition
        self.battleSession.onPlayerReceivedHit += self._handleMedalCondition
        self.battleSession.onPlayerBlockedDamage += self._handleMedalCondition

    def stop(self):
        self.battleSession.onPlayerKill -= self._handleMedalCondition
        self.battleSession.onPlayerReceivedDamage -= self._handleMedalCondition
        self.battleSession.onPlayerReceivedHit -= self._handleMedalCondition
        self.battleSession.onPlayerBlockedDamage -= self._handleMedalCondition

    def _handleMedalCondition(self):
        if self.player.vehicleClass != VehicleClass.SPG:
            return

        if self.hasAlreadyDisplayed(AchievementRegistry.MEDAL_STARK):
            return

        killsCount = self.battleSession.playerKillsOfEnemy

        receivedAnyDamageDealtOrBlockedHitsCount = self.battleSession.playerReceivedHitsOfEnemyBy(
            lambda receivedHitEvent: receivedHitEvent.isBlocked or receivedHitEvent.isDamageDealt
        )
        blockedDamage = self.battleSession.playerBlockedDamageOfEnemy
        receivedDamage = self.battleSession.playerReceivedDamageOfEnemy
        isAlive = BigWorld.player().isVehicleAlive

        if killsCount >= 2 \
                and receivedAnyDamageDealtOrBlockedHitsCount >= 2 \
                and (blockedDamage + receivedDamage) >= (self.player.maxHealth * 2.0 / 3.0) \
                and isAlive \
                and not self.battleSession.hasPlayerKilledAlly:
            self.display(AchievementRegistry.MEDAL_STARK)
