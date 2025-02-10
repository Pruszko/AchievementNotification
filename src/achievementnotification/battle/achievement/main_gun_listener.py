from achievementnotification.battle.achievement import BattleListener
from achievementnotification.utils.achievement_registry import AchievementRegistry


class MainGunListener(BattleListener):

    def start(self):
        self.battleSession.onPlayerDealingDamage += self._handleMainGunCondition

    def stop(self):
        self.battleSession.onPlayerDealingDamage -= self._handleMainGunCondition

    def _handleMainGunCondition(self):
        if self.hasAlreadyDisplayed(AchievementRegistry.MAIN_GUN):
            return

        enemyMaxHP = self.battleSession.getEnemyMaxHP()
        damageDealt = self.battleSession.playerDamageDealtOfEnemy

        if damageDealt >= 0.2 * enemyMaxHP \
                and damageDealt >= 1000 \
                and not self.battleSession.hasPlayerHitAlly:
            self.display(AchievementRegistry.MAIN_GUN)
