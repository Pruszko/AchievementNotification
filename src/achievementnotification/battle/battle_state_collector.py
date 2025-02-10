import logging

import BigWorld
import constants
from BattleFeedbackCommon import BATTLE_EVENT_TYPE
from ClientArena import ClientArena
from Math import Matrix
from PlayerEvents import g_playerEvents
from typing import List, Optional

from gui.battle_control import BattleSessionProvider
from gui.battle_control.battle_constants import FEEDBACK_EVENT_ID
from gui.battle_control.controllers.feedback_adaptor import BattleFeedbackAdaptor
from gui.battle_control.controllers.feedback_events import PlayerFeedbackEvent, _DamageExtra, _CritsExtra, \
    _VisibilityExtra
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider

from achievementnotification import createLogger
from achievementnotification.battle import KillEvent, DamageEvent, BattleSession, BlockedDamageEvent, HitEvent, \
    VehicleDeadEvent, ReceivedHitEvent, CritsEvent, CaptureDropEvent, SpottedEnemyEvent
from achievementnotification.hooks import avatar_hooks, vehicle_hooks
from achievementnotification.utils import IS_DEBUG

logger = createLogger(__name__)


def eventNameBy(eventID, eventClass):
    for name in dir(eventClass):
        attrValue = getattr(eventClass, name)

        # there are no duplicates, don't check for that
        if isinstance(attrValue, int) and attrValue == eventID:
            return name
    return None


# more descriptive event names for debugging
if IS_DEBUG:
    FEEDBACK_EVENT_ID_TO_NAME = {
        feedbackEventID: eventNameBy(feedbackEventID, FEEDBACK_EVENT_ID)
        for feedbackEventID in range(1, 80)
    }
    BATTLE_EVENT_TYPE_TO_NAME = {
        battleEventID: eventNameBy(battleEventID, BATTLE_EVENT_TYPE)
        for battleEventID in range(0, 25)
    }


class BattleStateCollector(object):
    _battleSessionProvider = dependency.descriptor(IBattleSessionProvider)  # type: BattleSessionProvider

    battleSession = None  # type: Optional[BattleSession]

    def __init__(self):
        self.battleSession = None

        self._prevArenaPeriod = constants.ARENA_PERIOD.IDLE
        self._arenaPeriod = constants.ARENA_PERIOD.IDLE

        g_playerEvents.onAvatarBecomePlayer += self._onAvatarBecomePlayer
        g_playerEvents.onAvatarBecomeNonPlayer += self._onAvatarBecomeNonPlayer

        self._battleSessionProvider.onBattleSessionStart += self._onBattleSessionStart
        self._battleSessionProvider.onBattleSessionStop += self._onBattleSessionStop

    def _onAvatarBecomePlayer(self):
        # we don't need to unregister events, because arena unregisters it itself
        # also, it's even hard to unregister them,
        # because onAvatarBecomeNonPlayer event is called AFTER arena is destroyed
        # not cool
        arena = BigWorld.player().arena  # type: ClientArena
        if arena.guiType in constants.ARENA_GUI_TYPE.RANDOM_RANGE:
            arena.onVehicleKilled += self._onVehicleKilled
            arena.onPeriodChange += self._onPeriodChange

    def _onAvatarBecomeNonPlayer(self):
        try:
            if self.battleSession is not None:
                self._endBattleStats()
        except:
            logger.error("Error occurred while finishing collecting battle statistics", exc_info=1)

    def _onBattleSessionStart(self):
        try:
            feedback = self._battleSessionProvider.shared.feedback  # type: BattleFeedbackAdaptor
            if feedback is None:
                return

            arena = BigWorld.player().arena  # type: ClientArena

            if arena.guiType in constants.ARENA_GUI_TYPE.RANDOM_RANGE:
                feedback.onPlayerFeedbackReceived += self._onPlayerFeedbackReceived

                avatar_hooks.onPlayerHit += self._onPlayerHit
                vehicle_hooks.onPlayerReceivedHit += self._onPlayerReceivedHit
        except:
            logger.error("Error occurred on starting battle session", exc_info=1)

    def _onBattleSessionStop(self):
        # (me few hours ago)
        # WG code for some reason always checks if feedback is not None in battle session start/stop
        # should I be concerned?
        #
        # (me now)
        # well, now I know - for some reason it is called even outside a battle
        # even in a fucking login screen
        # ???
        # noticed it when mod crashed on player arena access because there was no player
        #
        # most likely listeners are called when battle session provider is being finalized
        # but why calling it as a finalizer?
        # this "shared.X is not None" check in WG code probably prevents
        # collapsing of entire battle code (or at least my code)
        # because "shared" repository is empty when battle session is finalized,
        # so it won't trigger actual listener code twice
        try:
            feedback = self._battleSessionProvider.shared.feedback  # type: BattleFeedbackAdaptor
            if feedback is None:
                return

            arena = BigWorld.player().arena  # type: ClientArena

            if arena.guiType in constants.ARENA_GUI_TYPE.RANDOM_RANGE:
                feedback.onPlayerFeedbackReceived -= self._onPlayerFeedbackReceived

                avatar_hooks.onPlayerHit -= self._onPlayerHit
                vehicle_hooks.onPlayerReceivedHit -= self._onPlayerReceivedHit
        except:
            logger.error("Error occurred on stopping battle session", exc_info=1)

    # player arena vehicles are not immediately ready,
    # and I'm too lazy to hook into waiting to load all of them,
    # because I don't really know how many players will be in a battle
    # so ... wait for battle start, they will be all present for sure
    def _onPeriodChange(self, period, *args, **kwargs):
        try:
            self._prevArenaPeriod = self._arenaPeriod
            self._arenaPeriod = period

            if self._prevArenaPeriod < self._arenaPeriod == constants.ARENA_PERIOD.BATTLE:
                self._startBattleStats()
        except:
            logger.error("Error occurred on period change", exc_info=1)

    def _startBattleStats(self):
        logger.debug("Starting state")

        self._prevArenaPeriod = constants.ARENA_PERIOD.IDLE
        self._arenaPeriod = constants.ARENA_PERIOD.IDLE

        self.battleSession = BattleSession()
        self.battleSession.startListeners()

    def _endBattleStats(self):
        logger.debug("Ending state")

        self._prevArenaPeriod = constants.ARENA_PERIOD.IDLE
        self._arenaPeriod = constants.ARENA_PERIOD.IDLE

        self.battleSession.stopListeners()
        self.battleSession = None

    # note to myself
    #
    # battle events that we can listen to
    # BattleFeedbackCommon.BATTLE_EVENT_TYPE
    #
    # mapping of them to feedback events
    # feedback_events._BATTLE_EVENT_TO_PLAYER_FEEDBACK_EVENT
    #
    # extra data can be deducted by
    # feedback_events._PLAYER_FEEDBACK_EXTRA_DATA_CONVERTERS
    def _onPlayerFeedbackReceived(self, playerFeedbackEvents):
        playerFeedbackEvents = playerFeedbackEvents  # type: List[PlayerFeedbackEvent]

        try:
            logger.debug("__onPlayerFeedbackReceived(len: %s)", len(playerFeedbackEvents))
            for playerFeedbackEvent in playerFeedbackEvents:
                targetID = playerFeedbackEvent.getTargetID()
                battleEventType = playerFeedbackEvent.getBattleEventType()

                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug("__onPlayerFeedbackReceived"
                                 "(type: %s, targetID: %s, battleEventType: %s, role: %s, count: %s, extra: %s)",
                                 FEEDBACK_EVENT_ID_TO_NAME[playerFeedbackEvent.getType()],
                                 targetID,
                                 BATTLE_EVENT_TYPE_TO_NAME[battleEventType],
                                 playerFeedbackEvent.getRole(),
                                 playerFeedbackEvent.getCount(),
                                 playerFeedbackEvent.getExtra())

                if battleEventType == BATTLE_EVENT_TYPE.DAMAGE:
                    damageExtra = playerFeedbackEvent.getExtra()  # type: _DamageExtra
                    self._onPlayerDealingDamage(targetID, damageExtra)
                elif battleEventType == BATTLE_EVENT_TYPE.CRIT:
                    critsExtra = playerFeedbackEvent.getExtra()  # type: _CritsExtra
                    self._onPlayerDealingCrits(targetID, critsExtra)
                elif battleEventType == BATTLE_EVENT_TYPE.RECEIVED_DAMAGE:
                    damageExtra = playerFeedbackEvent.getExtra()  # type: _DamageExtra
                    self._onPlayerReceivedDamage(targetID, damageExtra)
                elif battleEventType == BATTLE_EVENT_TYPE.RECEIVED_CRIT:
                    critsExtra = playerFeedbackEvent.getExtra()  # type: _CritsExtra
                    self._onPlayerReceivedCrits(targetID, critsExtra)
                elif battleEventType == BATTLE_EVENT_TYPE.TANKING:
                    damageExtra = playerFeedbackEvent.getExtra()  # type: _DamageExtra
                    self._onPlayerBlockedDamage(targetID, damageExtra)
                elif battleEventType == BATTLE_EVENT_TYPE.BASE_CAPTURE_DROPPED:
                    captureDropCount = playerFeedbackEvent.getExtra()  # type: int
                    self._onPlayerCaptureDrop(targetID, captureDropCount)
                elif battleEventType == BATTLE_EVENT_TYPE.SPOTTED:
                    visibilityExtra = playerFeedbackEvent.getExtra()  # type: _VisibilityExtra
                    self._onPlayerSpottedEnemy(targetID, visibilityExtra)
        except:
            logger.error("Error occurred while handling player feedback event", exc_info=1)

    def _onPlayerDealingDamage(self, targetID, damageExtra):
        victimBattleData = self.battleSession.playerDatas.get(targetID, None)
        if victimBattleData is None:
            logger.warning("_onPlayerDealingDamage: targetID %s is not recognized in registry, "
                           "this should not happen",
                           targetID)
            return

        damageDealt = damageExtra.getDamage()
        attackReasonID = damageExtra.getAttackReasonID()

        damageEvent = DamageEvent(self.battleSession.player, victimBattleData, damageDealt, attackReasonID)

        logger.debug("_onPlayerDealingDamage %s", damageEvent)
        self.battleSession.playerDamageEvents.append(damageEvent)
        self.battleSession.onPlayerDealingDamage()

    def _onPlayerDealingCrits(self, targetID, critsExtra):
        victimBattleData = self.battleSession.playerDatas.get(targetID, None)
        if victimBattleData is None:
            logger.warning("_onPlayerDealingDamage: targetID %s is not recognized in registry, "
                           "this should not happen",
                           targetID)
            return

        critsCount = critsExtra.getCritsCount()
        attackReasonID = critsExtra._CritsExtra__attackReasonID

        critsEvent = CritsEvent(self.battleSession.player, victimBattleData, critsCount, attackReasonID)

        logger.debug("_onPlayerDealingCrit %s", critsEvent)
        self.battleSession.playerCritsEvents.append(critsEvent)
        self.battleSession.onPlayerDealingCrits()

    def _onPlayerReceivedDamage(self, targetID, damageExtra):
        attackerBattleData = self.battleSession.playerDatas.get(targetID, None)
        if attackerBattleData is None:
            logger.warning("_onPlayerReceivedDamage: targetID %s is not recognized in registry, "
                           "this should not happen",
                           targetID)
            return

        damageDealt = damageExtra.getDamage()
        attackReasonID = damageExtra.getAttackReasonID()

        damageEvent = DamageEvent(attackerBattleData, self.battleSession.player, damageDealt, attackReasonID)

        logger.debug("_onPlayerReceivedDamage %s", damageEvent)
        self.battleSession.playerReceivedDamageEvents.append(damageEvent)
        self.battleSession.onPlayerReceivedDamage()

    def _onPlayerReceivedCrits(self, targetID, critsExtra):
        attackerBattleData = self.battleSession.playerDatas.get(targetID, None)
        if attackerBattleData is None:
            logger.warning("_onPlayerReceivedDamage: targetID %s is not recognized in registry, "
                           "this should not happen",
                           targetID)
            return

        critsCount = critsExtra.getCritsCount()
        attackReasonID = critsExtra._CritsExtra__attackReasonID

        critsEvent = CritsEvent(attackerBattleData, self.battleSession.player, critsCount, attackReasonID)

        logger.debug("_onPlayerReceivedCrits %s", critsEvent)
        self.battleSession.playerReceivedCritsEvents.append(critsEvent)
        self.battleSession.onPlayerReceivedCrits()

    def _onPlayerBlockedDamage(self, targetID, damageExtra):
        attackerBattleData = self.battleSession.playerDatas.get(targetID, None)
        if attackerBattleData is None:
            logger.warning("_onPlayerBlockedDamage: targetID %s is not recognized in registry, "
                           "this should not happen",
                           targetID)
            return

        damageBlocked = damageExtra.getDamage()
        blockedDamageEvent = BlockedDamageEvent(attackerBattleData, damageBlocked)

        logger.debug("_onPlayerBlockedDamage %s", blockedDamageEvent)
        self.battleSession.playerBlockedDamageEvents.append(blockedDamageEvent)
        self.battleSession.onPlayerBlockedDamage()

    def _onPlayerCaptureDrop(self, targetID, captureDropCount):
        captureDropEvent = CaptureDropEvent(captureDropCount)
        logger.debug("_onPlayerCaptureDrop %s", captureDropEvent)

        self.battleSession.playerCaptureDropEvents.append(captureDropEvent)
        self.battleSession.onPlayerCaptureDrop()

    def _onPlayerSpottedEnemy(self, targetID, visibilityExtra):
        victimBattleData = self.battleSession.playerDatas.get(targetID, None)
        if victimBattleData is None:
            logger.warning("_onPlayerSpottedEnemy: targetID %s is not recognized in registry, "
                           "this should not happen",
                           targetID)
            return

        spottedEnemyEvent = SpottedEnemyEvent(victimBattleData)
        logger.debug("_onPlayerSpottedEnemy %s", spottedEnemyEvent)

        self.battleSession.playerSpottedEnemyEvents.append(spottedEnemyEvent)
        self.battleSession.onPlayerSpottedEnemy()

    def _onPlayerHit(self, vehicleID, hitFlags):
        if vehicleID == BigWorld.player().playerVehicleID:
            return

        victimBattleData = self.battleSession.playerDatas.get(vehicleID, None)

        if victimBattleData is None:
            logger.warning("_onPlayerHit: vehicleID %s is not recognized in registry, "
                           "this should not happen",
                           vehicleID)
            return

        hitEvent = HitEvent(self.player, victimBattleData, hitFlags)
        logger.debug("_onPlayerHit %s", hitEvent)

        self.battleSession.playerHitEvents.append(hitEvent)
        self.battleSession.onPlayerHit()

    def _onPlayerReceivedHit(self, attackerID, maxHitEffectCode,
                             damage, damageFactor, lastMaterialIsShield):
        attackerBattleData = self.battleSession.playerDatas.get(attackerID, None)

        if attackerBattleData is None:
            logger.warning("_onPlayerReceivedHit: attackerID %s is not recognized in registry, "
                           "this should not happen",
                           attackerID)
            return

        receivedHitEvent = ReceivedHitEvent(attackerBattleData, maxHitEffectCode,
                                            damage, damageFactor, lastMaterialIsShield)

        logger.debug("_onPlayerReceivedHit %s", receivedHitEvent)
        self.battleSession.playerReceivedHitEvents.append(receivedHitEvent)
        self.battleSession.onPlayerReceivedHit()

    def _onVehicleKilled(self, victimID, killerID, equipmentID, reasonID, numVehiclesAffected):
        try:
            victimBattleData = self.battleSession.playerDatas.get(victimID, None)
            if victimBattleData is None:
                logger.warning("_onVehicleKilled: victimID %s is not recognized in registry, "
                               "this should not happen",
                               victimID)
                return

            if killerID == BigWorld.player().playerVehicleID:
                self._onVehicleKilledByPlayer(victimBattleData, reasonID)

            killerBattleData = self.battleSession.playerDatas.get(killerID, None)
            if killerBattleData is None:
                logger.warning("_onVehicleKilled: killerID %s is not recognized in registry, "
                               "this should not happen",
                               killerID)
                return

            self._onVehicleDead(victimBattleData, killerBattleData, reasonID)
        except:
            logger.error("Error occurred while handling vehicle being destroyed", exc_info=1)

    def _onVehicleKilledByPlayer(self, victimBattleData, reasonID):
        playerEntity = BigWorld.player()
        victimEntity = BigWorld.entity(victimBattleData.vehicleID)

        killDistance = None
        isAmmoRackKill = False
        if victimEntity is not None:
            playerPos = Matrix(playerEntity.matrix).translation
            victimPos = Matrix(victimEntity.matrix).translation

            killDistance = (playerPos - victimPos).length
            isAmmoRackKill = constants.SPECIAL_VEHICLE_HEALTH.IS_AMMO_BAY_DESTROYED(victimEntity.health)

        killEvent = KillEvent(self.player, victimBattleData, killDistance, isAmmoRackKill, reasonID)
        logger.debug("_onVehicleKilledByPlayer %s", killEvent)

        self.battleSession.playerKillEvents.append(killEvent)
        self.battleSession.onPlayerKill()

    def _onVehicleDead(self, victimBattleData, killerBattleData, reasonID):
        vehicleDeadEvent = VehicleDeadEvent(victimBattleData, killerBattleData, reasonID)
        logger.debug("_onVehicleDead %s", vehicleDeadEvent)

        self.battleSession.vehicleDeadEvents.append(vehicleDeadEvent)
        self.battleSession.onVehicleDead()

    @property
    def player(self):
        return self.battleSession.player


g_battleStateCollector = BattleStateCollector()
