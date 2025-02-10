import BigWorld

from achievementnotification.battle import BattleListener, VehicleClass
from achievementnotification.utils.achievement_registry import AchievementRegistry


class CommonKillListener(BattleListener):

    def start(self):
        self.battleSession.onPlayerKill += self._onVehicleKilledByPlayer

    def stop(self):
        self.battleSession.onPlayerKill -= self._onVehicleKilledByPlayer

    def _onVehicleKilledByPlayer(self):
        self._handleStandardKill()

        self._handleLightTankKillingHigherTierNonSpg()
        self._handleLightTankKillingHigherTierSpg()
        self._handleMediumTankKillingHigherTierNonSpg()
        self._handleTankDestroyerKillingHigherTierBy2NonSpg()

        self._handleNonSpgKillingSpg()
        self._handleNonSpgKillingHigherTierSpg()

    def _handleStandardKill(self):
        kills = self.battleSession.playerKillsOfEnemy

        if self.isGrandBattle():
            if not self.hasAlreadyDisplayed(AchievementRegistry.WARRIOR):
                if kills >= 8:
                    self.display(AchievementRegistry.WARRIOR, extended=True)

            if not self.hasAlreadyDisplayed(AchievementRegistry.MEDAL_RADLEY_WALTERS):
                if 10 <= kills <= 12 and self.battleSession.player.vehicleLevel >= 5:
                    self.display(AchievementRegistry.MEDAL_RADLEY_WALTERS, extended=True)
            elif not self.hasAlreadyDisplayed(AchievementRegistry.MEDAL_LAFAYETTE_POOL):
                if 13 <= kills <= 20 and self.battleSession.player.vehicleLevel >= 5:
                    self.display(AchievementRegistry.MEDAL_LAFAYETTE_POOL, extended=True)
            elif not self.hasAlreadyDisplayed(AchievementRegistry.HEROES_OF_RASSENAY):
                if kills >= 21:
                    self.display(AchievementRegistry.HEROES_OF_RASSENAY, extended=True)
        else:
            if not self.hasAlreadyDisplayed(AchievementRegistry.WARRIOR):
                if kills >= 6:
                    self.display(AchievementRegistry.WARRIOR)

            if not self.hasAlreadyDisplayed(AchievementRegistry.FIGHTER):
                if 4 <= kills <= 5:
                    self.display(AchievementRegistry.FIGHTER)
            elif not self.hasAlreadyDisplayed(AchievementRegistry.MEDAL_RADLEY_WALTERS):
                if 8 <= kills <= 9 and self.battleSession.player.vehicleLevel >= 5:
                    self.display(AchievementRegistry.MEDAL_RADLEY_WALTERS)
            elif not self.hasAlreadyDisplayed(AchievementRegistry.MEDAL_LAFAYETTE_POOL):
                if 10 <= kills <= 13 and self.battleSession.player.vehicleLevel >= 5:
                    self.display(AchievementRegistry.MEDAL_LAFAYETTE_POOL)
            elif not self.hasAlreadyDisplayed(AchievementRegistry.HEROES_OF_RASSENAY):
                if kills >= 14:
                    self.display(AchievementRegistry.HEROES_OF_RASSENAY)

    def _handleLightTankKillingHigherTierNonSpg(self):
        if self.battleSession.player.vehicleClass != VehicleClass.LIGHT_TANK:
            return

        killsOfHigherTierNonSpg = self.battleSession.playerKillsOfEnemyBy(
            lambda killEvent: killEvent.victim.vehicleLevel > killEvent.killer.vehicleLevel and
                              killEvent.victim.vehicleClass != VehicleClass.SPG
        )

        if not self.hasAlreadyDisplayed(AchievementRegistry.MEDAL_ORLIK):
            if killsOfHigherTierNonSpg >= 2:
                self.display(AchievementRegistry.MEDAL_ORLIK)

    def _handleLightTankKillingHigherTierSpg(self):
        if self.battleSession.player.vehicleClass != VehicleClass.LIGHT_TANK:
            return

        killsOfHigherTierSpg = self.battleSession.playerKillsOfEnemyBy(
            lambda killEvent: killEvent.victim.vehicleLevel > killEvent.killer.vehicleLevel and
                              killEvent.victim.vehicleClass == VehicleClass.SPG
        )

        isAlive = BigWorld.player().isVehicleAlive

        if not self.hasAlreadyDisplayed(AchievementRegistry.MEDAL_TAMADA_YOSHIO):
            if killsOfHigherTierSpg >= 2 and isAlive:
                self.display(AchievementRegistry.MEDAL_TAMADA_YOSHIO)

    def _handleMediumTankKillingHigherTierNonSpg(self):
        if self.player.vehicleClass != VehicleClass.MEDIUM_TANK:
            return

        killsOfHigherTierNonSpg = self.battleSession.playerKillsOfEnemyBy(
            lambda killEvent: killEvent.victim.vehicleLevel > killEvent.killer.vehicleLevel and
                              killEvent.victim.vehicleClass != VehicleClass.SPG
        )

        if not self.hasAlreadyDisplayed(AchievementRegistry.MEDAL_LEHVASLAIHO):
            if killsOfHigherTierNonSpg >= 2:
                self.display(AchievementRegistry.MEDAL_LEHVASLAIHO)
        if not self.hasAlreadyDisplayed(AchievementRegistry.MEDAL_OSKIN):
            if killsOfHigherTierNonSpg >= 3:
                self.display(AchievementRegistry.MEDAL_OSKIN)
        if not self.hasAlreadyDisplayed(AchievementRegistry.MEDAL_NIKOLAS):
            if killsOfHigherTierNonSpg >= 4:
                self.display(AchievementRegistry.MEDAL_NIKOLAS)

    def _handleTankDestroyerKillingHigherTierBy2NonSpg(self):
        if self.player.vehicleClass != VehicleClass.TANK_DESTROYER:
            return

        killsOfHigherTierBy2NonSpg = self.battleSession.playerKillsOfEnemyBy(
            lambda killEvent: killEvent.victim.vehicleLevel >= killEvent.killer.vehicleLevel + 2 and
                              killEvent.victim.vehicleClass != VehicleClass.SPG
        )

        if not self.hasAlreadyDisplayed(AchievementRegistry.MEDAL_HALONEN):
            if killsOfHigherTierBy2NonSpg >= 2:
                self.display(AchievementRegistry.MEDAL_HALONEN)

    def _handleNonSpgKillingSpg(self):
        if self.player.vehicleClass == VehicleClass.SPG:
            return

        killsOfSpg = self.battleSession.playerKillsOfEnemyBy(
            lambda killEvent: killEvent.victim.vehicleClass == VehicleClass.SPG
        )

        if not self.hasAlreadyDisplayed(AchievementRegistry.MEDAL_PASCUCCI):
            if killsOfSpg >= 2:
                self.display(AchievementRegistry.MEDAL_PASCUCCI)
        if not self.hasAlreadyDisplayed(AchievementRegistry.MEDAL_DUMITRU):
            if killsOfSpg >= 3:
                self.display(AchievementRegistry.MEDAL_DUMITRU)

    def _handleNonSpgKillingHigherTierSpg(self):
        if self.player.vehicleClass == VehicleClass.SPG:
            return

        killsOfHigherTierSpg = self.battleSession.playerKillsOfEnemyBy(
            lambda killEvent: killEvent.victim.vehicleLevel > killEvent.killer.vehicleLevel and
                              killEvent.victim.vehicleClass == VehicleClass.SPG
        )

        if not self.hasAlreadyDisplayed(AchievementRegistry.MEDAL_BURDA):
            if killsOfHigherTierSpg >= 3:
                self.display(AchievementRegistry.MEDAL_BURDA)
