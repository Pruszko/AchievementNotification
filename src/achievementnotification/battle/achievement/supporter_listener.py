from achievementnotification.battle import BattleListener
from achievementnotification.utils.achievement_registry import AchievementRegistry


class SupporterListener(BattleListener):

    def start(self):
        self.battleSession.onVehicleDead += self._checkMedalCondition
        self.battleSession.onPlayerHit += self._checkMedalCondition

    def stop(self):
        self.battleSession.onVehicleDead -= self._checkMedalCondition
        self.battleSession.onPlayerHit -= self._checkMedalCondition

    def _checkMedalCondition(self):
        if self.hasAlreadyDisplayed(AchievementRegistry.SUPPORTER):
            return

        vehicleIdsPiercedAndDamagedOrCritedByPlayer = set(
            hitEvent.victim.vehicleID for hitEvent in self.battleSession.playerHitEventsOfEnemy
            if hitEvent.isPierced and hitEvent.isDamaging
        )

        vehiclesIdsSupportedByPlayerButNotKilledByPlayer = len(set(
            vehicleDeadEvent.victim.vehicleID for vehicleDeadEvent in self.battleSession.vehicleDeadEvents
            if vehicleDeadEvent.victim.vehicleID in vehicleIdsPiercedAndDamagedOrCritedByPlayer
            and vehicleDeadEvent.attacker.vehicleID != self.player.vehicleID
        ))

        if vehiclesIdsSupportedByPlayerButNotKilledByPlayer >= 6:
            self.display(AchievementRegistry.SUPPORTER)
