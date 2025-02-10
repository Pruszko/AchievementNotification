import BigWorld

from achievementnotification.battle import BattleListener
from achievementnotification.utils.achievement_registry import AchievementRegistry


class CharmedListener(BattleListener):

    def start(self):
        self.battleSession.onPlayerReceivedDamage += self._handleMedalCondition

    def stop(self):
        self.battleSession.onPlayerReceivedDamage -= self._handleMedalCondition

    def _handleMedalCondition(self):
        if self.hasAlreadyDisplayed(AchievementRegistry.CHARMED):
            return

        vehicleIdsThatDealtDamageToPlayer = set(
            receivedDamageEvent.attacker.vehicleID
            for receivedDamageEvent in self.battleSession.playerReceivedDamageEventsOfEnemy
        )

        isAlive = BigWorld.player().isVehicleAlive

        if len(vehicleIdsThatDealtDamageToPlayer) >= 4 and isAlive:
            self.display(AchievementRegistry.CHARMED)
