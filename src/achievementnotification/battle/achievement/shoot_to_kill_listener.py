from achievementnotification.battle import VehicleClass
from achievementnotification.battle.achievement import BattleListener
from achievementnotification.utils.achievement_registry import AchievementRegistry


class ShootToKillListener(BattleListener):

    def start(self):
        self.battleSession.onPlayerDealingDamage += self._onPlayerDealingDamage

    def stop(self):
        self.battleSession.onPlayerDealingDamage -= self._onPlayerDealingDamage

    def _onPlayerDealingDamage(self):
        if self.player.vehicleClass == VehicleClass.SPG:
            return

        if self.hasAlreadyDisplayed(AchievementRegistry.SHOOT_TO_KILL):
            return

        if self.battleSession.playerDamageDealtOfEnemy > self.player.maxHealth:
            self.display(AchievementRegistry.SHOOT_TO_KILL)
