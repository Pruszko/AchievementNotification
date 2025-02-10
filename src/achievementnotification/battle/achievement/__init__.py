import abc
import typing

import BigWorld
import constants

if typing.TYPE_CHECKING:
    # cyclic import, but we need that only for type hints
    from achievementnotification.battle import BattleSession


class BattleListener(object):
    __metaclass__ = abc.ABCMeta

    battleSession = None  # type: BattleSession

    def __init__(self, battleSession):
        self.battleSession = battleSession

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def stop(self):
        pass

    def hasAlreadyDisplayed(self, achievement):
        return achievement.key in self.battleSession.displayedAchievementKeys

    def display(self, achievement, extended=False):
        achievement.displayAchievement(extended=extended)
        self.battleSession.displayedAchievementKeys.add(achievement.key)

    @property
    def player(self):
        return self.battleSession.player

    def isGrandBattle(self):
        return BigWorld.player().arena.guiType == constants.ARENA_GUI_TYPE.EPIC_RANDOM
