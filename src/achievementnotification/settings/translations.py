import json

import ResMgr
from helpers import getClientLanguage

from achievementnotification.utils import createLogger


logger = createLogger(__name__)

# if this is set to some language code, then below code will treat game language as that
# used only for debugging
DEBUG_LANGUAGE = None

# thanks to:
# - shuxue - for Russian translations

DEFAULT_TRANSLATIONS_MAP = {}
TRANSLATIONS_MAP = {}


def loadTranslations():
    defaultTranslationsMap = _loadLanguage("en")

    global DEFAULT_TRANSLATIONS_MAP
    DEFAULT_TRANSLATIONS_MAP = defaultTranslationsMap if defaultTranslationsMap is not None else {}

    if DEBUG_LANGUAGE is not None:
        language = DEBUG_LANGUAGE
        logger.info("Client language (debug): %s", language)
    else:
        language = getClientLanguage()
        logger.info("Client language: %s", language)

    translationsMap = _loadLanguage(language)

    if translationsMap is not None:
        logger.info("Translations for language %s detected" % language)
        global TRANSLATIONS_MAP
        TRANSLATIONS_MAP = translationsMap
    else:
        logger.info("Translations for language %s not present, fallback to en" % language)


def _loadLanguage(language):
    translationsRes = ResMgr.openSection("gui/achievementnotification/translations/translations_%s.json" % language)
    if translationsRes is None:
        return None

    translationsStr = str(translationsRes.asBinary)
    return json.loads(translationsStr, encoding="UTF-8")


class TranslationBase(object):

    def __init__(self, tokenName):
        self._tokenName = tokenName
        self._value = None

    def __get__(self, instance, owner=None):
        if self._value is None:
            self._value = self._generateTranslation()
        return self._value

    def _generateTranslation(self):
        raise NotImplementedError()


class TranslationElement(TranslationBase):

    def _generateTranslation(self):
        global TRANSLATIONS_MAP
        if self._tokenName in TRANSLATIONS_MAP:
            return TRANSLATIONS_MAP[self._tokenName]

        global DEFAULT_TRANSLATIONS_MAP
        return DEFAULT_TRANSLATIONS_MAP[self._tokenName]


class TranslationList(TranslationBase):

    def _generateTranslation(self):
        global TRANSLATIONS_MAP
        if self._tokenName in TRANSLATIONS_MAP:
            return "".join(TRANSLATIONS_MAP[self._tokenName])

        global DEFAULT_TRANSLATIONS_MAP
        return "".join(DEFAULT_TRANSLATIONS_MAP[self._tokenName])


class Tr(object):
    # common
    MODNAME = TranslationElement("modname")
    CHECKED = TranslationElement("checked")
    UNCHECKED = TranslationElement("unchecked")
    DEFAULT_VALUE = TranslationElement("defaultValue")

    # intro
    INTRO_LABEL = TranslationElement("intro.label")
    INTRO_HEADER = TranslationElement("intro.header")
    INTRO_BODY = TranslationList("intro.body")
    INTRO_NOTE = TranslationList("intro.note")

    # common settings
    COMMON_SETTINGS_LABEL = TranslationElement("common-settings.label")

    SCALE_LABEL = TranslationElement("common-settings.scale.label")
    SCALE_BODY = TranslationList("common-settings.scale.body")

    DISPLAY_MODE_LABEL = TranslationElement("common-settings.display-mode.label")
    DISPLAY_MODE_BODY = TranslationList("common-settings.display-mode.body")
    DISPLAY_MODE_OPTION_COMPACT = TranslationElement("common-settings.display-mode.option.compact")
    DISPLAY_MODE_OPTION_DETAILED = TranslationElement("common-settings.display-mode.option.detailed")

    VERTICAL_POSITION_LABEL = TranslationElement("common-settings.vertical-position.label")
    VERTICAL_POSITION_BODY = TranslationList("common-settings.vertical-position.body")

    FIRST_DISPLAY_TIME_LABEL = TranslationElement("common-settings.first-display-time.label")
    FIRST_DISPLAY_TIME_BODY = TranslationList("common-settings.first-display-time.body")

    CONSECUTIVE_DISPLAY_TIME_LABEL = TranslationElement("common-settings.consecutive-display-time.label")
    CONSECUTIVE_DISPLAY_TIME_BODY = TranslationList("common-settings.consecutive-display-time.body")

    # achievements settings
    ACHIEVEMENTS_SETTINGS_LABEL = TranslationElement("achievements-settings.label")
    DISPLAY_ACHIEVEMENT_HEADER = TranslationElement("display-achievement.header")
    DISPLAY_ACHIEVEMENT_BODY = TranslationList("display-achievement.body")
