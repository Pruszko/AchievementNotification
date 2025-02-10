from achievementnotification.battle import BattleListener
from achievementnotification.utils.achievement_registry import AchievementRegistry


class IronManListener(BattleListener):

    def start(self):
        self.battleSession.onPlayerReceivedHit += self._handleMedalCondition

    def stop(self):
        self.battleSession.onPlayerReceivedHit -= self._handleMedalCondition

    def _handleMedalCondition(self):
        if self.hasAlreadyDisplayed(AchievementRegistry.IRON_MAN):
            return

        longestConsecutiveNonDamagingReceivedHits = 0

        currentConsecutiveNonDamagingReceivedHits = 0
        for receivedHitEvent in self.battleSession.playerReceivedHitEventsOfEnemy:
            if receivedHitEvent.isBlocked:
                currentConsecutiveNonDamagingReceivedHits += 1
            else:
                currentConsecutiveNonDamagingReceivedHits = 0

            if longestConsecutiveNonDamagingReceivedHits < currentConsecutiveNonDamagingReceivedHits:
                longestConsecutiveNonDamagingReceivedHits = currentConsecutiveNonDamagingReceivedHits

        if longestConsecutiveNonDamagingReceivedHits >= 10:
            self.display(AchievementRegistry.IRON_MAN)
