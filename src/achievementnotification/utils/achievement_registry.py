from BattleReplay import g_replayCtrl
from helpers import i18n

from achievementnotification.settings.config_param_types import PARAM_REGISTRY


ALL_ACHIEVEMENTS = []


class Achievement(object):

    def __init__(self, key, msaTokenNameToPlay, extended=False, conditional=False,
                 conditionStandardText=None,
                 conditionExtendedText=None):

        self.key = key
        self.msaTokenNameToPlay = msaTokenNameToPlay
        self.extended = extended
        self.conditional = conditional

        self.text = i18n.makeString("#achievements:%s" % key)
        self.descriptionText = i18n.makeString("#achievements:%s_descr" % key)
        self.conditionText = i18n.makeString("#achievements:%s_condition" % key)

        self.descriptionStandardText = None
        self.descriptionExtendedText = None
        if extended:
            self.descriptionStandardText = i18n.makeString("#achievements:%s_standard_descr" % key,
                                                           condition=conditionStandardText)
            self.descriptionExtendedText = i18n.makeString("#achievements:%s_ext_descr" % key,
                                                           condition=conditionExtendedText)

        self.largeIconPath = "img://gui/maps/icons/achievement/big/%s.png" % key

        global ALL_ACHIEVEMENTS
        ALL_ACHIEVEMENTS.append(self)

    def displayAchievement(self, extended=False, forced=False):
        from achievementnotification import g_achievementNotificationMod

        # always allow displaying it from mod configurator
        if forced:
            g_achievementNotificationMod.achievementNotificationFlash.displayAchievement(achievementKey=self.key,
                                                                                         extended=extended)
            return

        achievementDisplayEnabled = PARAM_REGISTRY[self.msaTokenNameToPlay]()
        if not achievementDisplayEnabled:
            return

        # while time warp is being done in replays, do not display achievements as well
        if g_replayCtrl.isTimeWarpInProgress:
            return

        g_achievementNotificationMod.achievementNotificationFlash.displayAchievement(achievementKey=self.key,
                                                                                     extended=extended)


class AchievementRegistry(object):
    ARSONIST = Achievement(
        key="arsonist",
        msaTokenNameToPlay="achievements-arsonist")
    BONE_CRUSHER = Achievement(
        key="bonecrusher",
        msaTokenNameToPlay="achievements-bonecrusher")
    CHARMED = Achievement(
        key="charmed", conditional=True,
        msaTokenNameToPlay="achievements-charmed")
    DEFENDER = Achievement(
        key="defender",
        msaTokenNameToPlay="achievements-defender")
    DEMOLITION = Achievement(
        key="demolition",
        msaTokenNameToPlay="achievements-demolition")
    DUELIST = Achievement(
        key="duelist",
        msaTokenNameToPlay="achievements-duelist")
    EVEN = Achievement(
        key="even",
        msaTokenNameToPlay="achievements-even")
    FIGHTER = Achievement(
        key="fighter",
        msaTokenNameToPlay="achievements-fighter")
    HEROES_OF_RASSENAY = Achievement(
        key="heroesOfRassenay", extended=True,
        conditionStandardText="14" + i18n.makeString("#achievements:heroesOfRassenay_condition_text"),
        conditionExtendedText="21" + i18n.makeString("#achievements:heroesOfRassenay_condition_text"),
        msaTokenNameToPlay="achievements-heroesOfRassenay")
    HUNTSMAN = Achievement(
        key="huntsman",
        msaTokenNameToPlay="achievements-huntsman")
    IMPENETRABLE = Achievement(
        key="impenetrable", conditional=True,
        msaTokenNameToPlay="achievements-impenetrable")
    IRON_MAN = Achievement(
        key="ironMan",
        msaTokenNameToPlay="achievements-ironMan")
    KAMIKAZE = Achievement(
        key="kamikaze",
        msaTokenNameToPlay="achievements-kamikaze")
    MAIN_GUN = Achievement(
        key="mainGun", conditional=True,
        msaTokenNameToPlay="achievements-mainGun")
    MEDAL_ANTI_SPG_FIRE = Achievement(
        key="medalAntiSpgFire", conditional=True,
        msaTokenNameToPlay="achievements-medalAntiSpgFire")
    MEDAL_BURDA = Achievement(
        key="medalBurda",
        msaTokenNameToPlay="achievements-medalBurda")
    MEDAL_COOL_BLOOD = Achievement(
        key="medalCoolBlood", conditional=True,
        msaTokenNameToPlay="achievements-medalCoolBlood")
    MEDAL_DUMITRU = Achievement(
        key="medalDumitru",
        msaTokenNameToPlay="achievements-medalDumitru")
    MEDAL_GORE = Achievement(
        key="medalGore", conditional=True,
        msaTokenNameToPlay="achievements-medalGore")
    MEDAL_HALONEN = Achievement(
        key="medalHalonen",
        msaTokenNameToPlay="achievements-medalHalonen")
    MEDAL_LAFAYETTE_POOL = Achievement(
        key="medalLafayettePool", extended=True,
        conditionStandardText="10-13",
        conditionExtendedText="13-20",
        msaTokenNameToPlay="achievements-medalLafayettePool")
    MEDAL_LEHVASLAIHO = Achievement(
        key="medalLehvaslaiho",
        msaTokenNameToPlay="achievements-medalLehvaslaiho")
    MEDAL_NIKOLAS = Achievement(
        key="medalNikolas",
        msaTokenNameToPlay="achievements-medalNikolas")
    MEDAL_ORLIK = Achievement(
        key="medalOrlik",
        msaTokenNameToPlay="achievements-medalOrlik")
    MEDAL_OSKIN = Achievement(
        key="medalOskin",
        msaTokenNameToPlay="achievements-medalOskin")
    MEDAL_STARK = Achievement(
        key="medalStark", conditional=True,
        msaTokenNameToPlay="achievements-medalStark")
    MEDAL_PASCUCCI = Achievement(
        key="medalPascucci",
        msaTokenNameToPlay="achievements-medalPascucci")
    MEDAL_RADLEY_WALTERS = Achievement(
        key="medalRadleyWalters", extended=True,
        conditionStandardText="8-9",
        conditionExtendedText="10-12",
        msaTokenNameToPlay="achievements-medalRadleyWalters")
    MEDAL_TAMADA_YOSHIO = Achievement(
        key="medalTamadaYoshio", conditional=True,
        msaTokenNameToPlay="achievements-medalTamadaYoshio")
    SCOUT = Achievement(
        key="scout", conditional=True,
        msaTokenNameToPlay="achievements-scout")
    SHOOT_TO_KILL = Achievement(
        key="shootToKill",
        msaTokenNameToPlay="achievements-shootToKill")
    STEEL_WALL = Achievement(
        key="steelwall", conditional=True,
        msaTokenNameToPlay="achievements-steelwall")
    STURDY = Achievement(
        key="sturdy", conditional=True,
        msaTokenNameToPlay="achievements-sturdy")
    SUPPORTER = Achievement(
        key="supporter", conditional=True,
        msaTokenNameToPlay="achievements-supporter")
    WARRIOR = Achievement(
        key="warrior", extended=True,
        conditionStandardText="6" + i18n.makeString("#achievements:warrior_condition_text"),
        conditionExtendedText="8" + i18n.makeString("#achievements:warrior_condition_text"),
        msaTokenNameToPlay="achievements-warrior")

    ALL_ACHIEVEMENTS = ALL_ACHIEVEMENTS

    @staticmethod
    def getAchievementByMsaTokenName(msaTokenName):
        for achievement in AchievementRegistry.ALL_ACHIEVEMENTS:
            if achievement.msaTokenNameToPlay == msaTokenName:
                return achievement

        return None
