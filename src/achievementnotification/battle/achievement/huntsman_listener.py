from achievementnotification.battle import BattleListener, VehicleClass
from achievementnotification.utils.achievement_registry import AchievementRegistry


class HuntsmanListener(BattleListener):

    def start(self):
        self.battleSession.onPlayerKill += self._handleMedalCondition

    def stop(self):
        self.battleSession.onPlayerKill -= self._handleMedalCondition

    def _handleMedalCondition(self):
        if self.hasAlreadyDisplayed(AchievementRegistry.HUNTSMAN):
            return

        killsOfLightTank = self.battleSession.playerKillsOfEnemyBy(
            lambda killEvent: killEvent.victim.vehicleClass == VehicleClass.LIGHT_TANK
        )

        lightTankCount = self.battleSession.playerDatasCountOfEnemyBy(
            lambda playerData: playerData.vehicleClass == VehicleClass.LIGHT_TANK
        )

        if killsOfLightTank == lightTankCount and lightTankCount >= 3:
            self.display(AchievementRegistry.HUNTSMAN)
