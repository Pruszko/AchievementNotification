from achievementnotification.settings.config_param_types import *


class ConfigParams(object):

    def __init__(self):
        self.enabled = BooleanParam(
            path=["enabled"],
            defaultValue=True, disabledValue=False
        )

        # common settings
        self.scale = SliderParam(
            path=["scale"],
            castFunction=float,
            minValue=0.2, step=0.05, maxValue=4.0,
            defaultValue=1.0
        )
        self.displayMode = OptionsParam(
            path=["display-mode"],
            options=[
                Option(DisplayMode.COMPACT, msaValue=0, displayName=Tr.DISPLAY_MODE_OPTION_COMPACT),
                Option(DisplayMode.DETAILED, msaValue=1, displayName=Tr.DISPLAY_MODE_OPTION_DETAILED),
            ],
            defaultValue=DisplayMode.DETAILED
        )
        self.verticalPosition = SliderParam(
            path=["vertical-position"],
            castFunction=float,
            minValue=0.0, step=0.01, maxValue=1.0,
            defaultValue=0.8
        )
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
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_bonecrusher = BooleanParam(
            path=["achievements", "bonecrusher"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_charmed = BooleanParam(
            path=["achievements", "charmed"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_defender = BooleanParam(
            path=["achievements", "defender"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_demolition = BooleanParam(
            path=["achievements", "demolition"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_duelist = BooleanParam(
            path=["achievements", "duelist"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_even = BooleanParam(
            path=["achievements", "even"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_fighter = BooleanParam(
            path=["achievements", "fighter"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_heroesOfRassenay = BooleanParam(
            path=["achievements", "heroesOfRassenay"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_huntsman = BooleanParam(
            path=["achievements", "huntsman"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_impenetrable = BooleanParam(
            path=["achievements", "impenetrable"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_ironMan = BooleanParam(
            path=["achievements", "ironMan"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_kamikaze = BooleanParam(
            path=["achievements", "kamikaze"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_mainGun = BooleanParam(
            path=["achievements", "mainGun"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_medalAntiSpgFire = BooleanParam(
            path=["achievements", "medalAntiSpgFire"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_medalBurda = BooleanParam(
            path=["achievements", "medalBurda"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_medalCoolBlood = BooleanParam(
            path=["achievements", "medalCoolBlood"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_medalDumitru = BooleanParam(
            path=["achievements", "medalDumitru"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_medalGore = BooleanParam(
            path=["achievements", "medalGore"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_medalHalonen = BooleanParam(
            path=["achievements", "medalHalonen"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_medalLafayettePool = BooleanParam(
            path=["achievements", "medalLafayettePool"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_medalLehvaslaiho = BooleanParam(
            path=["achievements", "medalLehvaslaiho"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_medalNikolas = BooleanParam(
            path=["achievements", "medalNikolas"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_medalOrlik = BooleanParam(
            path=["achievements", "medalOrlik"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_medalOskin = BooleanParam(
            path=["achievements", "medalOskin"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_medalStark = BooleanParam(
            path=["achievements", "medalStark"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_medalPascucci = BooleanParam(
            path=["achievements", "medalPascucci"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_medalRadleyWalters = BooleanParam(
            path=["achievements", "medalRadleyWalters"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_medalTamadaYoshio = BooleanParam(
            path=["achievements", "medalTamadaYoshio"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_scout = BooleanParam(
            path=["achievements", "scout"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_shootToKill = BooleanParam(
            path=["achievements", "shootToKill"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_steelwall = BooleanParam(
            path=["achievements", "steelwall"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_sturdy = BooleanParam(
            path=["achievements", "sturdy"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_supporter = BooleanParam(
            path=["achievements", "supporter"],
            defaultValue=True, disabledValue=False,
            playable=True
        )
        self.achievements_warrior = BooleanParam(
            path=["achievements", "warrior"],
            defaultValue=True, disabledValue=False,
            playable=True
        )

    @staticmethod
    def items():
        return PARAM_REGISTRY.items()


g_configParams = ConfigParams()
