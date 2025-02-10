from achievementnotification.battle import BattleListener, VehicleClass
from achievementnotification.utils.achievement_registry import AchievementRegistry


class CoolBloodListener(BattleListener):

    def start(self):
        self.battleSession.onPlayerKill += self._handleMedalCondition

    def stop(self):
        self.battleSession.onPlayerKill -= self._handleMedalCondition

    def _handleMedalCondition(self):
        if self.player.vehicleClass != VehicleClass.SPG or self.player.vehicleLevel < 4:
            return

        if self.hasAlreadyDisplayed(AchievementRegistry.MEDAL_COOL_BLOOD):
            return

        killsOfLightThatWereVeryClose = self.battleSession.playerKillsOfEnemyBy(
            lambda killEvent: killEvent.victim.vehicleClass == VehicleClass.LIGHT_TANK and
                              killEvent.distance is not None and
                              killEvent.distance <= 100
        )

        if killsOfLightThatWereVeryClose >= 2 and not self.battleSession.hasPlayerKilledAlly:
            self.display(AchievementRegistry.MEDAL_COOL_BLOOD)
