from achievementnotification.battle import BattleListener
from achievementnotification.utils.achievement_registry import AchievementRegistry


class DuelistListener(BattleListener):

    def start(self):
        self.battleSession.onPlayerKill += self._handleMedalCondition
        self.battleSession.onPlayerReceivedDamage += self._handleMedalCondition
        self.battleSession.onPlayerReceivedCrits += self._handleMedalCondition

    def stop(self):
        self.battleSession.onPlayerKill -= self._handleMedalCondition
        self.battleSession.onPlayerReceivedDamage -= self._handleMedalCondition
        self.battleSession.onPlayerReceivedCrits -= self._handleMedalCondition

    def _handleMedalCondition(self):
        if self.hasAlreadyDisplayed(AchievementRegistry.DUELIST):
            return

        vehicleIdsThatDamagedPlayer = set(
            playerReceivedDamageEvent.attacker.vehicleID
            for playerReceivedDamageEvent in self.battleSession.playerReceivedDamageEvents
        )

        vehicleIdsThatCritPlayer = set(
            playerReceivedCritsEvent.attacker.vehicleID
            for playerReceivedCritsEvent in self.battleSession.playerReceivedCritsEvents
        )

        vehicleIdsThatAnyDamagedPlayer = vehicleIdsThatDamagedPlayer | vehicleIdsThatCritPlayer

        playerKillsOfEnemiesThatAnyDamagedPlayer = self.battleSession.playerKillsOfEnemyBy(
            lambda killEvent: killEvent.victim.vehicleID in vehicleIdsThatAnyDamagedPlayer
        )

        if playerKillsOfEnemiesThatAnyDamagedPlayer >= 2:
            self.display(AchievementRegistry.DUELIST)
