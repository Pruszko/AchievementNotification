from achievementnotification.battle import BattleListener, VehicleClass
from achievementnotification.utils.achievement_registry import AchievementRegistry


class MedalGoreListener(BattleListener):

    def start(self):
        self.battleSession.onPlayerDealingDamage += self._handleMedalCondition

    def stop(self):
        self.battleSession.onPlayerDealingDamage -= self._handleMedalCondition

    def _handleMedalCondition(self):
        if self.hasAlreadyDisplayed(AchievementRegistry.MEDAL_GORE):
            return

        if self.player.vehicleClass != VehicleClass.SPG:
            return

        damageDealt = self.battleSession.playerDamageDealtOfEnemy
        if damageDealt >= 2000 and damageDealt >= (self.player.maxHealth * 8) \
                and not self.battleSession.hasPlayerKilledAlly:
            self.display(AchievementRegistry.MEDAL_GORE)
