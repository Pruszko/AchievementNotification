import BigWorld

from achievementnotification.battle.achievement import BattleListener
from achievementnotification.utils.achievement_registry import AchievementRegistry


class ImpenetrableListener(BattleListener):

    def start(self):
        self.battleSession.onPlayerBlockedDamage += self._onPlayerBlockedDamage

    def stop(self):
        self.battleSession.onPlayerBlockedDamage -= self._onPlayerBlockedDamage

    def _onPlayerBlockedDamage(self):
        if self.hasAlreadyDisplayed(AchievementRegistry.IMPENETRABLE):
            return

        isAlive = BigWorld.player().isVehicleAlive
        if self.battleSession.playerBlockedDamageOfEnemy > self.battleSession.player.maxHealth \
                and isAlive:
            self.display(AchievementRegistry.IMPENETRABLE)
