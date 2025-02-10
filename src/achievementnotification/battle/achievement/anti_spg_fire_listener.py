from achievementnotification.battle import BattleListener, VehicleClass
from achievementnotification.utils.achievement_registry import AchievementRegistry


class AntiSpgFireListener(BattleListener):

    def start(self):
        self.battleSession.onPlayerKill += self._handleMedalCondition

    def stop(self):
        self.battleSession.onPlayerKill -= self._handleMedalCondition

    def _handleMedalCondition(self):
        if self.player.vehicleClass != VehicleClass.SPG:
            return

        if self.hasAlreadyDisplayed(AchievementRegistry.MEDAL_ANTI_SPG_FIRE):
            return

        killsOfSpg = self.battleSession.playerKillsOfEnemyBy(
            lambda killEvent: killEvent.victim.vehicleClass == VehicleClass.SPG
        )

        spgCount = self.battleSession.playerDatasCountOfEnemyBy(
            lambda playerData: playerData.vehicleClass == VehicleClass.SPG
        )

        if killsOfSpg == spgCount and spgCount >= 2 and not self.battleSession.hasPlayerKilledAlly:
            self.display(AchievementRegistry.MEDAL_ANTI_SPG_FIRE)
