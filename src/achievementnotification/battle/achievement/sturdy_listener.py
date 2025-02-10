import BigWorld

from achievementnotification.battle import BattleListener
from achievementnotification.utils.achievement_registry import AchievementRegistry


class SturdyListener(BattleListener):

    def start(self):
        self.battleSession.onPlayerReceivedDamage += self._handleMedalCondition
        self.battleSession.onPlayerReceivedHit += self._handleMedalCondition

    def stop(self):
        self.battleSession.onPlayerReceivedDamage -= self._handleMedalCondition
        self.battleSession.onPlayerReceivedHit -= self._handleMedalCondition

    def _handleMedalCondition(self):
        if self.hasAlreadyDisplayed(AchievementRegistry.STURDY):
            return

        receivedDamage = self.battleSession.playerReceivedDamage
        remainingPlayerHP = self.player.maxHealth - receivedDamage

        receivedHitEventsOfEnemy = self.battleSession.playerReceivedHitEventsOfEnemy
        lastReceivedHitEvent = receivedHitEventsOfEnemy[-1] if len(receivedHitEventsOfEnemy) > 0 else None

        if lastReceivedHitEvent is None:
            return

        isRicochetOrNonPenetratingNonExternalModuleHit = lastReceivedHitEvent.isBlockedExcludingExternalModules
        isAlive = BigWorld.player().isVehicleAlive

        if (float(remainingPlayerHP) / self.player.maxHealth) < 0.1 \
                and isRicochetOrNonPenetratingNonExternalModuleHit \
                and isAlive:
            self.display(AchievementRegistry.STURDY)
