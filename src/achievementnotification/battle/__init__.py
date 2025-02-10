import BigWorld
import Event
import constants
from ClientArena import ClientArena
from VehicleEffects import DamageFromShotDecoder

from constants import VEHICLE_CLASSES, ATTACK_REASON_INDICES, ATTACK_REASON, VEHICLE_HIT_EFFECT
from soft_exception import SoftException
from typing import Dict, List, Set

from achievementnotification import createLogger
from achievementnotification.battle.achievement import BattleListener
from achievementnotification.utils import PrintableMixin

logger = createLogger(__name__)


class VehicleClass(object):
    LIGHT_TANK = "lightTank"
    MEDIUM_TANK = "mediumTank"
    HEAVY_TANK = "heavyTank"
    SPG = "SPG"
    TANK_DESTROYER = "AT-SPG"

    # based on vehicles.__getClassFromTags()
    @staticmethod
    def fromVehicleDescriptor(vehicleDescriptor):
        classes = [classTag for classTag in VEHICLE_CLASSES if classTag in vehicleDescriptor.type.tags]
        if len(classes) > 1:
            raise SoftException("There are several classes for vehicle '%s': '%s'" % (vehicleDescriptor.name, classes))
        return classes[0]


class BattleSession(object):

    onPlayerKill = Event.Event()
    onPlayerDealingDamage = Event.Event()
    onPlayerDealingCrits = Event.Event()
    onPlayerHit = Event.Event()

    onPlayerReceivedDamage = Event.Event()
    onPlayerReceivedCrits = Event.Event()
    onPlayerBlockedDamage = Event.Event()
    onPlayerReceivedHit = Event.Event()

    onPlayerCaptureDrop = Event.Event()
    onPlayerSpottedEnemy = Event.Event()
    onVehicleDead = Event.Event()

    playerDatas = None  # type: Dict[int, PlayerBattleData]
    player = None  # type: PlayerBattleData
    displayedAchievementKeys = None  # type: Set[str]

    playerKillEvents = None  # type: List[KillEvent]
    playerDamageEvents = None  # type: List[DamageEvent]
    playerCritsEvents = None  # type: List[CritsEvent]
    playerHitEvents = None  # type: List[HitEvent]

    playerReceivedDamageEvents = None  # type: List[DamageEvent]
    playerReceivedCritsEvents = None  # type: List[CritsEvent]
    playerBlockedDamageEvents = None  # type: List[BlockedDamageEvent]
    playerReceivedHitEvents = None  # type: List[ReceivedHitEvent]

    playerCaptureDropEvents = None  # type: List[CaptureDropEvent]
    playerSpottedEnemyEvents = None  # type: List[SpottedEnemyEvent]
    vehicleDeadEvents = None  # type: List[VehicleDeadEvent]

    _listeners = None  # type: List[BattleListener]

    def __init__(self):
        self.playerDatas = {}
        self.displayedAchievementKeys = set()

        self.playerKillEvents = []
        self.playerDamageEvents = []
        self.playerCritsEvents = []
        self.playerHitEvents = []

        self.playerReceivedDamageEvents = []
        self.playerReceivedCritsEvents = []
        self.playerBlockedDamageEvents = []
        self.playerReceivedHitEvents = []

        self.playerCaptureDropEvents = []
        self.playerSpottedEnemyEvents = []
        self.vehicleDeadEvents = []

        arena = BigWorld.player().arena  # type: ClientArena
        for vehicleID, arenaVehicle in arena.vehicles.iteritems():
            # arenaVehicle is a dict with small info, but enough for our use case
            # especially useful, because we preemptively know something about all players in a battle
            #
            # it's better than listening for Vehicle.onEnterWorld
            # because ... most vehicles are not in render distance
            self.playerDatas[vehicleID] = PlayerBattleData(
                vehicleID=vehicleID,
                name=arenaVehicle["name"],
                vehicleTypeDescriptor=arenaVehicle["vehicleType"],
                team=arenaVehicle["team"],
                maxHealth=arenaVehicle["maxHealth"])

        playerVehicleID = BigWorld.player().playerVehicleID
        self.player = self.playerDatas[playerVehicleID]

        enemyMaxHP = self.getEnemyMaxHP()
        logger.debug("Enemy max HP: %s (%s for high caliber)", enemyMaxHP, 0.2 * enemyMaxHP)

        from achievementnotification.battle.achievement.anti_spg_fire_listener import AntiSpgFireListener
        from achievementnotification.battle.achievement.arsonist_listener import ArsonistListener
        from achievementnotification.battle.achievement.bonecrusher_listener import BoneCrusherListener
        from achievementnotification.battle.achievement.charmed_listener import CharmedListener
        from achievementnotification.battle.achievement.common_kill_listener import CommonKillListener
        from achievementnotification.battle.achievement.cool_blood_listener import CoolBloodListener
        from achievementnotification.battle.achievement.defender_listener import DefenderListener
        from achievementnotification.battle.achievement.demolition_listener import DemolitionListener
        from achievementnotification.battle.achievement.duelist_listener import DuelistListener
        from achievementnotification.battle.achievement.even_listener import EvenListener
        from achievementnotification.battle.achievement.huntsman_listener import HuntsmanListener
        from achievementnotification.battle.achievement.impenetrable_listener import ImpenetrableListener
        from achievementnotification.battle.achievement.iron_man_listener import IronManListener
        from achievementnotification.battle.achievement.kamikaze_listener import KamikazeListener
        from achievementnotification.battle.achievement.main_gun_listener import MainGunListener
        from achievementnotification.battle.achievement.medal_gore_listener import MedalGoreListener
        from achievementnotification.battle.achievement.medal_stark_listener import MedalStarkListener
        from achievementnotification.battle.achievement.scout_listener import ScoutListener
        from achievementnotification.battle.achievement.shoot_to_kill_listener import ShootToKillListener
        from achievementnotification.battle.achievement.steel_wall_listener import SteelWallListener
        from achievementnotification.battle.achievement.sturdy_listener import SturdyListener
        from achievementnotification.battle.achievement.supporter_listener import SupporterListener

        self._listeners = [
            AntiSpgFireListener(self),
            ArsonistListener(self),
            BoneCrusherListener(self),
            CharmedListener(self),
            CommonKillListener(self),
            CoolBloodListener(self),
            DefenderListener(self),
            DemolitionListener(self),
            DuelistListener(self),
            EvenListener(self),
            HuntsmanListener(self),
            ImpenetrableListener(self),
            IronManListener(self),
            KamikazeListener(self),
            MainGunListener(self),
            MedalGoreListener(self),
            MedalStarkListener(self),
            ScoutListener(self),
            ShootToKillListener(self),
            SteelWallListener(self),
            SturdyListener(self),
            SupporterListener(self),
        ]

    def startListeners(self):
        for listener in self._listeners:
            listener.start()

    def stopListeners(self):
        for listener in self._listeners:
            listener.stop()

    def getEnemyMaxHP(self):
        return sum(
            enemyVehicle.maxHealth
            for enemyVehicle in self.playerDatas.values()
            if enemyVehicle.team != BigWorld.player().team
        )

    @property
    def playerDatasOfEnemy(self):
        return [playerData for playerData in self.playerDatas.values()
                if playerData.team != self.player.team]

    @property
    def playerDatasOfAlly(self):
        return [playerData for playerData in self.playerDatas.values()
                if playerData.team == self.player.team]

    def playerDatasCountOfEnemyBy(self, conditionFn):
        return len(filter(
            lambda playerData: conditionFn(playerData),
            self.playerDatasOfEnemy
        ))

    @property
    def playerKillEventsOfEnemy(self):
        return [
            killEvent for killEvent in self.playerKillEvents
            if killEvent.victim.team != self.player.team
        ]

    @property
    def playerKillEventsOfAlly(self):
        return [
            killEvent for killEvent in self.playerKillEvents
            if killEvent.victim.team == self.player.team
        ]

    @property
    def playerDamageEventsOfEnemy(self):
        return [
            damageEvent for damageEvent in self.playerDamageEvents
            if damageEvent.victim.team != self.player.team
        ]

    @property
    def playerDamageEventsOfAlly(self):
        return [
            damageEvent for damageEvent in self.playerDamageEvents
            if damageEvent.victim.team == self.player.team
        ]

    @property
    def playerCritsEventsOfEnemy(self):
        return [
            critsEvent for critsEvent in self.playerCritsEvents
            if critsEvent.victim.team != self.player.team
        ]

    @property
    def playerCritsEventsOfAlly(self):
        return [
            critsEvent for critsEvent in self.playerCritsEvents
            if critsEvent.victim.team == self.player.team
        ]

    @property
    def playerHitEventsOfEnemy(self):
        return [
            hitEvent for hitEvent in self.playerHitEvents
            if hitEvent.victim.team != self.player.team
        ]

    @property
    def playerHitEventsOfAlly(self):
        return [
            hitEvent for hitEvent in self.playerHitEvents
            if hitEvent.victim.team == self.player.team
        ]

    @property
    def playerReceivedDamageEventsOfEnemy(self):
        return [
            damageEvent for damageEvent in self.playerReceivedDamageEvents
            if damageEvent.attacker.team != self.player.team
        ]

    @property
    def playerReceivedDamageEventsOfAlly(self):
        return [
            damageEvent for damageEvent in self.playerReceivedDamageEvents
            if damageEvent.attacker.team == self.player.team
        ]

    @property
    def playerReceivedCritsEventsOfEnemy(self):
        return [
            critsEvent for critsEvent in self.playerReceivedCritsEvents
            if critsEvent.attacker.team != self.player.team
        ]

    @property
    def playerReceivedCritsEventsOfAlly(self):
        return [
            critsEvent for critsEvent in self.playerReceivedCritsEvents
            if critsEvent.attacker.team == self.player.team
        ]

    @property
    def playerReceivedHitEventsOfEnemy(self):
        return [
            receivedHitEvent for receivedHitEvent in self.playerReceivedHitEvents
            if receivedHitEvent.attacker.team != self.player.team
        ]

    @property
    def playerReceivedHitEventsOfAlly(self):
        return [
            receivedHitEvent for receivedHitEvent in self.playerReceivedHitEvents
            if receivedHitEvent.attacker.team == self.player.team
        ]

    @property
    def playerBlockedDamageEventsOfEnemy(self):
        return [
            blockedDamageEvent for blockedDamageEvent in self.playerBlockedDamageEvents
            if blockedDamageEvent.attacker.team != self.player.team
        ]

    @property
    def playerBlockedDamageEventsOfAlly(self):
        return [
            blockedDamageEvent for blockedDamageEvent in self.playerBlockedDamageEvents
            if blockedDamageEvent.attacker.team == self.player.team
        ]

    @property
    def vehicleDeadEventsOfEnemy(self):
        return [
            vehicleDeadEvent for vehicleDeadEvent in self.vehicleDeadEvents
            if vehicleDeadEvent.attacker.team != self.player.team
        ]

    @property
    def vehicleDeadEventsOfAlly(self):
        return [
            vehicleDeadEvent for vehicleDeadEvent in self.vehicleDeadEvents
            if vehicleDeadEvent.attacker.team == self.player.team
        ]

    @property
    def playerKillsOfEnemy(self):
        return len(self.playerKillEventsOfEnemy)

    def playerKillsOfEnemyBy(self, conditionFn):
        return len(filter(
            lambda killEvent: conditionFn(killEvent),
            self.playerKillEventsOfEnemy
        ))

    @property
    def hasPlayerKilledAlly(self):
        return len(self.playerKillEventsOfAlly) > 0

    @property
    def playerDamageDealtOfEnemy(self):
        return sum(
            damageEvent.damageDealt
            for damageEvent in self.playerDamageEventsOfEnemy
        )

    def playerDamageDealtOfEnemyBy(self, conditionFn):
        return sum(damageEvent.damageDealt for damageEvent in filter(
            lambda damageEvent: conditionFn(damageEvent),
            self.playerDamageEventsOfEnemy
        ))

    @property
    def playerCritsOfEnemy(self):
        return sum(critsEvent.critCount for critsEvent in self.playerCritsEventsOfEnemy)

    @property
    def hasPlayerHitAlly(self):
        return len(self.playerHitEventsOfAlly) > 0

    @property
    def playerReceivedDamage(self):
        return sum(
            receivedDamageEvent.damageDealt for receivedDamageEvent in self.playerReceivedDamageEvents
        )

    @property
    def playerReceivedDamageOfEnemy(self):
        return sum(
            receivedDamageEvent.damageDealt for receivedDamageEvent in self.playerReceivedDamageEventsOfEnemy
        )

    @property
    def playerBlockedDamageOfEnemy(self):
        return sum(
            blockedDamageEvent.damageBlocked for blockedDamageEvent in self.playerBlockedDamageEventsOfEnemy
        )

    @property
    def playerReceivedHitsOfEnemy(self):
        return len(self.playerReceivedHitEventsOfEnemy)

    def playerReceivedHitsOfEnemyBy(self, conditionFn):
        return len(filter(
            lambda receivedHitEvent: conditionFn(receivedHitEvent),
            self.playerReceivedHitEventsOfEnemy
        ))

    @property
    def playerCaptureDropsSum(self):
        return sum(playerCaptureDrop.captureDropCount for playerCaptureDrop in self.playerCaptureDropEvents)

    @property
    def playerSpottedEnemyCount(self):
        return len(self.playerSpottedEnemyEvents)


class PlayerBattleData(PrintableMixin, object):

    def __init__(self, vehicleID, name, vehicleTypeDescriptor, team, maxHealth):
        super(PlayerBattleData, self).__init__()

        self.vehicleID = vehicleID
        self.name = name
        self.vehicleClass = VehicleClass.fromVehicleDescriptor(vehicleTypeDescriptor)
        self.vehicleLevel = vehicleTypeDescriptor.type.level
        self.team = team
        self.maxHealth = maxHealth


class AttackReasonEventMixin(object):

    attackReasonID = None

    @property
    def isAttackReasonFire(self):
        return self.attackReasonID == ATTACK_REASON_INDICES[ATTACK_REASON.FIRE]

    @property
    def isAttackReasonRam(self):
        return self.attackReasonID == ATTACK_REASON_INDICES[ATTACK_REASON.RAM]


class KillEvent(AttackReasonEventMixin, PrintableMixin, object):

    def __init__(self, killerPlayerData, victimPlayerData, distance, hasAmmoRackExploded, attackReasonID):
        super(KillEvent, self).__init__()

        self.killer = killerPlayerData
        self.victim = victimPlayerData
        self.distance = distance
        self.hasAmmoRackExploded = hasAmmoRackExploded
        self.attackReasonID = attackReasonID


class DamageEvent(AttackReasonEventMixin, PrintableMixin, object):

    def __init__(self, attacker, victim, damageDealt, attackReasonID):
        super(DamageEvent, self).__init__()

        self.attacker = attacker
        self.victim = victim
        self.damageDealt = damageDealt
        self.attackReasonID = attackReasonID


class CritsEvent(AttackReasonEventMixin, PrintableMixin, object):

    def __init__(self, attacker, victim, critCount, attackReasonID):
        super(CritsEvent, self).__init__()

        self.attacker = attacker
        self.victim = victim
        self.critCount = critCount
        self.attackReasonID = attackReasonID


class BlockedDamageEvent(PrintableMixin, object):

    def __init__(self, attacker, damageBlocked):
        super(BlockedDamageEvent, self).__init__()

        self.attacker = attacker
        self.damageBlocked = damageBlocked


class HitEvent(PrintableMixin, object):

    def __init__(self, attacker, victim, hitFlags):
        super(HitEvent, self).__init__()

        self.attacker = attacker
        self.victim = victim
        self.hitFlags = hitFlags

    @property
    def isPierced(self):
        return bool(self.hitFlags & constants.VEHICLE_HIT_FLAGS.IS_ANY_PIERCING_MASK)

    @property
    def isDamaging(self):
        return bool(self.hitFlags & constants.VEHICLE_HIT_FLAGS.IS_ANY_DAMAGE_MASK)


class ReceivedHitEvent(PrintableMixin, object):

    def __init__(self, attacker, maxHitEffectCode,
                 damage, damageFactor, lastMaterialIsShield):
        super(ReceivedHitEvent, self).__init__()

        self.attacker = attacker
        self.maxHitEffectCode = maxHitEffectCode
        self.damage = damage
        self.damageFactor = damageFactor
        self.lastMaterialIsShield = lastMaterialIsShield

    @property
    def isDamageDealt(self):
        return self.damageFactor > 0

    @property
    def isBlocked(self):
        return not self.damageFactor

    @property
    def isBlockedExcludingExternalModules(self):
        return self.isBlocked and self.maxHitEffectCode in (VEHICLE_HIT_EFFECT.INTERMEDIATE_RICOCHET,
                                                            VEHICLE_HIT_EFFECT.FINAL_RICOCHET,
                                                            VEHICLE_HIT_EFFECT.ARMOR_NOT_PIERCED)


class VehicleDeadEvent(AttackReasonEventMixin, PrintableMixin, object):

    def __init__(self, victim, attacker, attackReasonID):
        super(VehicleDeadEvent, self).__init__()

        self.victim = victim
        self.attacker = attacker
        self.attackReasonID = attackReasonID


class CaptureDropEvent(PrintableMixin, object):

    def __init__(self, captureDropCount):
        super(CaptureDropEvent, self).__init__()

        self.captureDropCount = captureDropCount


class SpottedEnemyEvent(PrintableMixin, object):

    def __init__(self, victim):
        super(SpottedEnemyEvent, self).__init__()

        self.victim = victim
