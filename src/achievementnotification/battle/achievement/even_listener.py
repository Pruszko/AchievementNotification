from achievementnotification.battle import BattleListener
from achievementnotification.utils.achievement_registry import AchievementRegistry


class EvenListener(BattleListener):

    def start(self):
        self.battleSession.onPlayerKill += self._handleMedalCondition
        self.battleSession.onVehicleDead += self._handleMedalCondition

    def stop(self):
        self.battleSession.onPlayerKill -= self._handleMedalCondition
        self.battleSession.onVehicleDead -= self._handleMedalCondition

    def _handleMedalCondition(self):
        if self.hasAlreadyDisplayed(AchievementRegistry.EVEN):
            return

        vehicleIdsKilledByPlayer = set(
            killEvent.victim.vehicleID for killEvent in self.battleSession.playerKillEventsOfEnemy
        )
        vehicleIdsThatKilledPlayer = set(
            vehicleDeadEvent.attacker.vehicleID for vehicleDeadEvent in self.battleSession.vehicleDeadEvents
            if vehicleDeadEvent.victim.vehicleID == self.player.vehicleID
        )

        vehicleIdsThatEvenedWithPlayer = vehicleIdsKilledByPlayer & vehicleIdsThatKilledPlayer

        if len(vehicleIdsThatEvenedWithPlayer) > 0:
            self.display(AchievementRegistry.EVEN)
