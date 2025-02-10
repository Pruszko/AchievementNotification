from achievementnotification.battle import BattleListener
from achievementnotification.utils.achievement_registry import AchievementRegistry


class BoneCrusherListener(BattleListener):

    def start(self):
        self.battleSession.onPlayerDealingCrits += self._handleMedalCondition

    def stop(self):
        self.battleSession.onPlayerDealingCrits -= self._handleMedalCondition

    def _handleMedalCondition(self):
        if self.hasAlreadyDisplayed(AchievementRegistry.BONE_CRUSHER):
            return

        if self.battleSession.playerCritsOfEnemy >= 5:
            self.display(AchievementRegistry.BONE_CRUSHER)
