import BigWorld
import Event
from Vehicle import Vehicle

from achievementnotification.utils import overrideIn, createLogger


logger = createLogger(__name__)

onPlayerReceivedHit = Event.Event()


# we cannot simply listen to vehicle feedback event with some eventIDs
# because we won't receive those events during replay time warp
# mainly - provided points are valid, but decoding them results in empty list
# mostly due to self.appearance.collisions not being present during time warp,
#
# but we only care for maxHitEffectCode stored in points
# which are easy to decode based on VehicleEffects.DamageFromShotDecoder
#
# it is generally the most precise place to collect direct hits from enemies I've found
# however - Czech light tank guns have rapid RoF
# and game - despite calling that method very often -  is not registering every individual received hit from them
# but rather "aggregates" similar hit results as one (or just skipping them, who knows)
# for example, for 9 individual non-piercing shots we may have received only 4 hit results
# which makes few medals not to display despite meeting requirements on battle results
#
# is there anything more precise?
# tested hooks around damage indicator, but it was even worse and had even less info
@overrideIn(Vehicle)
def showDamageFromShot(func, self, attackerID, points, effectsIndex, damage, damageFactor, lastMaterialIsShield):
    func(self, attackerID, points, effectsIndex, damage, damageFactor, lastMaterialIsShield)

    try:
        if not self.isStarted:
            return

        if self.id != BigWorld.player().playerVehicleID:
            return

        if not self.isAlive():
            return

        decodedEffectCodes = decodeEffectCodes(points)

        if not decodedEffectCodes:
            return

        maxHitEffectCode = decodedEffectCodes[(-1)]

        onPlayerReceivedHit(attackerID, maxHitEffectCode, damage, damageFactor, lastMaterialIsShield)
    except:
        logger.error("Error occurred while handling damage from shot", exc_info=1)


# based on VehicleEffects.DamageFromShotDecoder
def decodeEffectCodes(points):
    return [
        int(segment & 255) for segment in points
    ]
