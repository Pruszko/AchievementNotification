from achievementnotification.settings.config_param_types import *


class ConfigParams(object):

    def __init__(self):
        self.enabled = BooleanParam(
            path=["enabled"],
            defaultValue=True, disabledValue=False
        )

        # common settings
        self.firstDisplayTime = SliderParam(
            path=["first-display-time"],
            castFunction=float,
            minValue=0.5, step=0.1, maxValue=10.0,
            defaultValue=5.0
        )
        self.consecutiveDisplayTime = SliderParam(
            path=["consecutive-display-time"],
            castFunction=float,
            minValue=0.5, step=0.1, maxValue=10.0,
            defaultValue=3.0
        )

        # achievement settings
        self.achievements_arsonist = BooleanParam(
            path=["achievements", "arsonist"],
            defaultValue=True,
            playable=True
        )
        self.achievements_bonecrusher = BooleanParam(
            path=["achievements", "bonecrusher"],
            defaultValue=True,
            playable=True
        )
        self.achievements_charmed = BooleanParam(
            path=["achievements", "charmed"],
            defaultValue=True,
            playable=True
        )
        self.achievements_defender = BooleanParam(
            path=["achievements", "defender"],
            defaultValue=True,
            playable=True
        )
        self.achievements_demolition = BooleanParam(
            path=["achievements", "demolition"],
            defaultValue=True,
            playable=True
        )
        self.achievements_duelist = BooleanParam(
            path=["achievements", "duelist"],
            defaultValue=True,
            playable=True
        )
        self.achievements_even = BooleanParam(
            path=["achievements", "even"],
            defaultValue=True,
            playable=True
        )
        self.achievements_fighter = BooleanParam(
            path=["achievements", "fighter"],
            defaultValue=True,
            playable=True
        )
        self.achievements_heroesOfRassenay = BooleanParam(
            path=["achievements", "heroesOfRassenay"],
            defaultValue=True,
            playable=True
        )
        self.achievements_huntsman = BooleanParam(
            path=["achievements", "huntsman"],
            defaultValue=True,
            playable=True
        )
        self.achievements_impenetrable = BooleanParam(
            path=["achievements", "impenetrable"],
            defaultValue=True,
            playable=True
        )
        self.achievements_ironMan = BooleanParam(
            path=["achievements", "ironMan"],
            defaultValue=True,
            playable=True
        )
        self.achievements_kamikaze = BooleanParam(
            path=["achievements", "kamikaze"],
            defaultValue=True,
            playable=True
        )
        self.achievements_mainGun = BooleanParam(
            path=["achievements", "mainGun"],
            defaultValue=True,
            playable=True
        )
        self.achievements_medalAntiSpgFire = BooleanParam(
            path=["achievements", "medalAntiSpgFire"],
            defaultValue=True,
            playable=True
        )
        self.achievements_medalBurda = BooleanParam(
            path=["achievements", "medalBurda"],
            defaultValue=True,
            playable=True
        )
        self.achievements_medalCoolBlood = BooleanParam(
            path=["achievements", "medalCoolBlood"],
            defaultValue=True,
            playable=True
        )
        self.achievements_medalDumitru = BooleanParam(
            path=["achievements", "medalDumitru"],
            defaultValue=True,
            playable=True
        )
        self.achievements_medalGore = BooleanParam(
            path=["achievements", "medalGore"],
            defaultValue=True,
            playable=True
        )
        self.achievements_medalHalonen = BooleanParam(
            path=["achievements", "medalHalonen"],
            defaultValue=True,
            playable=True
        )
        self.achievements_medalLafayettePool = BooleanParam(
            path=["achievements", "medalLafayettePool"],
            defaultValue=True,
            playable=True
        )
        self.achievements_medalLehvaslaiho = BooleanParam(
            path=["achievements", "medalLehvaslaiho"],
            defaultValue=True,
            playable=True
        )
        self.achievements_medalNikolas = BooleanParam(
            path=["achievements", "medalNikolas"],
            defaultValue=True,
            playable=True
        )
        self.achievements_medalOrlik = BooleanParam(
            path=["achievements", "medalOrlik"],
            defaultValue=True,
            playable=True
        )
        self.achievements_medalOskin = BooleanParam(
            path=["achievements", "medalOskin"],
            defaultValue=True,
            playable=True
        )
        self.achievements_medalStark = BooleanParam(
            path=["achievements", "medalStark"],
            defaultValue=True,
            playable=True
        )
        self.achievements_medalPascucci = BooleanParam(
            path=["achievements", "medalPascucci"],
            defaultValue=True,
            playable=True
        )
        self.achievements_medalRadleyWalters = BooleanParam(
            path=["achievements", "medalRadleyWalters"],
            defaultValue=True,
            playable=True
        )
        self.achievements_medalTamadaYoshio = BooleanParam(
            path=["achievements", "medalTamadaYoshio"],
            defaultValue=True,
            playable=True
        )
        self.achievements_scout = BooleanParam(
            path=["achievements", "scout"],
            defaultValue=True,
            playable=True
        )
        self.achievements_shootToKill = BooleanParam(
            path=["achievements", "shootToKill"],
            defaultValue=True,
            playable=True
        )
        self.achievements_steelwall = BooleanParam(
            path=["achievements", "steelwall"],
            defaultValue=True,
            playable=True
        )
        self.achievements_sturdy = BooleanParam(
            path=["achievements", "sturdy"],
            defaultValue=True,
            playable=True
        )
        self.achievements_supporter = BooleanParam(
            path=["achievements", "supporter"],
            defaultValue=True,
            playable=True
        )
        self.achievements_warrior = BooleanParam(
            path=["achievements", "warrior"],
            defaultValue=True,
            playable=True
        )

    @staticmethod
    def items():
        return PARAM_REGISTRY.items()


g_configParams = ConfigParams()
