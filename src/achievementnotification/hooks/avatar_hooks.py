import Event
from Avatar import Avatar
from constants import BigWorld

from achievementnotification import createLogger
from achievementnotification.utils import overrideIn

logger = createLogger(__name__)

onPlayerHit = Event.Event()


# this exact hook is the most reliable way to obtain individual player hits at other targets, because:
# * we get vehicleID
# * isPierced and isDamaging flags needed for some medals
# * works during replay time warp (both backward and forward) so we don't lose stats
#
# it's basically responsible for sound effect or messages about hits (for ex. hit an ally)
# but gives an absurdly detailed info about type of hit for that (literally 26 possible types, lmao)
#
# we do it with this override instead of Vehicle.showDamageFromShot,
# because here we will also get results for arty shots,
# and Vehicle.showDamageFromShot receives only direct hits
#
# we could use Vehicle.showDamageFromExplosion as well, but why complicate stuff?
@overrideIn(Avatar)
def showShotResults(func, self, shotResults):
    func(self, shotResults)

    try:
        for showResult in shotResults:
            vehicleID = showResult & 4294967295L
            flags = showResult >> 32 & 4294967295L

            onPlayerHit(vehicleID, flags)
    except:
        logger.error("Error occurred while handling shot results", exc_info=1)
