from achievementnotification.settings.translations import Tr
from achievementnotification.settings.config import g_config
from achievementnotification.settings.config_param import g_configParams, createTooltip
from achievementnotification.utils import ObservingSemaphore, displayDialog, createLogger

from gui.modsSettingsApi import g_modsSettingsApi

from achievementnotification.utils.achievement_registry import AchievementRegistry


logger = createLogger(__name__)


modLinkage = "com.github.pruszko.achievementnotification"


def registerSoftDependencySupport():
    template = {
        "modDisplayName": Tr.MODNAME,
        "enabled": g_configParams.enabled.defaultMsaValue,
        "column1":
            _createIntroPart() +
            _endSection() +
            _createCommonPart(),
        "column2":
            _createAchievementsSettings()
    }

    # we purposely ignore ModsSettingsAPI capability of saving mod configuration
    # due to config file being "master" configuration
    #
    # also, I don't like going against "standard setup" of ModsSettingsAPI support, but
    # we still treat it only as a GUI, not a configuration framework
    #
    # so we also purposely always call setModTemplate instead of registerCallback
    # to keep always updated GUI template
    g_modsSettingsApi.setModTemplate(modLinkage, template, onModSettingsChanged, onModSettingsButtonClick)


# we cannot update ModsSettingsAPI settings without triggering onModSettingsChanged callback,
# so we will use "semaphore" to control when we want to ignore it
settingsChangedSemaphore = ObservingSemaphore()


# this is called only on manual config reload
def onConfigFileReload():
    msaSettings = {}

    for tokenName, param in g_configParams.items():
        msaSettings[tokenName] = param.msaValue

    logger.info("Synchronizing config file -> ModsSettingsAPI")
    g_modsSettingsApi.updateModSettings(modLinkage, newSettings=msaSettings)


@settingsChangedSemaphore.withIgnoringLock(returnForIgnored=None)
def onModSettingsChanged(linkage, newSettings):
    if linkage != modLinkage:
        return

    try:
        serializedSettings = {}
        for tokenName, param in g_configParams.items():
            if tokenName not in newSettings:
                continue

            value = param.fromMsaValue(newSettings[tokenName])
            jsonValue = param.toJsonValue(value)

            serializedSettings[param.tokenName] = jsonValue

        logger.info("Synchronizing ModsSettingsAPI -> config file")
        g_config.updateConfigSafely(serializedSettings)
    except Exception:
        logger.error("Error occurred while ModsSettingsAPI settings change.", exc_info=True)


def onModSettingsButtonClick(linkage, clickedTokenName, value):
    if linkage != modLinkage:
        return

    try:
        achievement = AchievementRegistry.getAchievementByMsaTokenName(clickedTokenName)
        if achievement is not None:
            achievement.displayAchievement(forced=True)
        else:
            logger.error("Couldn't find achievement to preview by tokenName %s.",
                         clickedTokenName, exc_info=1)
            displayDialog("Failed to display achievement preview.\n"
                          "Contact mod developer for further support with provided logs.")
    except:
        logger.error("Failed to display achievement preview by tokenName %s.",
                     clickedTokenName, exc_info=1)
        displayDialog("Failed to display achievement preview.\n"
                      "Contact mod developer for further support with provided logs.")


def _endSection():
    return _emptyLine() + _horizontalLine()


def _innerSectionSeparator():
    return _emptyLine(4)


def _emptyLine(count=1):
    return [
        {
            "type": "Empty"
        }
    ] * count


def _horizontalLine():
    return [
        {
            "type": "Label",
            "text": "________________________________________"
        }
    ]


def _createIntroPart():
    return [
        {
            "type": "Label",
            "text": Tr.INTRO_LABEL,
            "tooltip": createTooltip(
                header=Tr.INTRO_HEADER,
                body=Tr.INTRO_BODY + "\n",
                note=Tr.INTRO_NOTE
            )
        }
    ]


def _createCommonPart():
    return [{
        "type": "Label",
        "text": Tr.COMMON_SETTINGS_LABEL
    }] + _emptyLine(2) + [
        g_configParams.scale.renderParam(
            header=Tr.SCALE_LABEL,
            body=Tr.SCALE_BODY
        ),
        g_configParams.displayMode.renderParam(
            header=Tr.DISPLAY_MODE_LABEL,
            body=Tr.DISPLAY_MODE_BODY
        ),
        g_configParams.verticalPosition.renderParam(
            header=Tr.VERTICAL_POSITION_LABEL,
            body=Tr.VERTICAL_POSITION_BODY
        ),
        g_configParams.firstDisplayTime.renderParam(
            header=Tr.FIRST_DISPLAY_TIME_LABEL,
            body=Tr.FIRST_DISPLAY_TIME_BODY
        ),
        g_configParams.consecutiveDisplayTime.renderParam(
            header=Tr.CONSECUTIVE_DISPLAY_TIME_LABEL,
            body=Tr.CONSECUTIVE_DISPLAY_TIME_BODY
        )
    ]


def _createAchievementsSettings():
    return [{
        "type": "Label",
        "text": Tr.ACHIEVEMENTS_SETTINGS_LABEL
    }] + _emptyLine(2) + [
        g_configParams.achievements_arsonist.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.ARSONIST.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_bonecrusher.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.BONE_CRUSHER.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_charmed.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.CHARMED.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_defender.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.DEFENDER.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_demolition.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.DEMOLITION.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_duelist.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.DUELIST.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_even.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.EVEN.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_fighter.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.FIGHTER.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_heroesOfRassenay.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.HEROES_OF_RASSENAY.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_huntsman.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.HUNTSMAN.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_impenetrable.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.IMPENETRABLE.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_ironMan.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.IRON_MAN.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_kamikaze.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.KAMIKAZE.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_mainGun.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.MAIN_GUN.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_medalAntiSpgFire.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.MEDAL_ANTI_SPG_FIRE.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_medalBurda.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.MEDAL_BURDA.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_medalCoolBlood.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.MEDAL_COOL_BLOOD.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_medalDumitru.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.MEDAL_DUMITRU.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_medalGore.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.MEDAL_GORE.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_medalHalonen.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.MEDAL_HALONEN.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_medalLafayettePool.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.MEDAL_LAFAYETTE_POOL.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_medalLehvaslaiho.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.MEDAL_LEHVASLAIHO.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_medalNikolas.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.MEDAL_NIKOLAS.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_medalOrlik.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.MEDAL_ORLIK.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_medalOskin.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.MEDAL_OSKIN.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_medalStark.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.MEDAL_STARK.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_medalPascucci.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.MEDAL_PASCUCCI.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_medalRadleyWalters.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.MEDAL_RADLEY_WALTERS.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_medalTamadaYoshio.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.MEDAL_TAMADA_YOSHIO.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_scout.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.SCOUT.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_shootToKill.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.SHOOT_TO_KILL.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_steelwall.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.STEEL_WALL.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_sturdy.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.STURDY.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_supporter.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.SUPPORTER.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
        g_configParams.achievements_warrior.renderParam(
            header=Tr.DISPLAY_ACHIEVEMENT_HEADER + ": " + AchievementRegistry.WARRIOR.text,
            body=Tr.DISPLAY_ACHIEVEMENT_BODY
        ),
    ]


# UtilsManager
def _createImg(src, width=None, height=None, vSpace=None, hSpace=None):
    template = "<img src='{0}' "

    absoluteUrl = "img://gui/achievementnotification/" + src
    if width is not None:
        template += "width='{1}' "
    if height is not None:
        template += "height='{2}' "
    if vSpace is not None:
        template += "vspace='{3}' "
    if hSpace is not None:
        template += "hspace='{4}'  "

    template += "/>"
    return template.format(absoluteUrl, width, height, vSpace, hSpace)
