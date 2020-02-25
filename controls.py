from enum import Enum, auto


class Command(Enum):
    WAIT = auto()
    KEYPRESS = auto()
    KEYDOWN = auto()
    KEYUP = auto()


CONTROLS = {
    "drive": [(Command.KEYDOWN, 'w'), (Command.WAIT, 1), (Command.KEYUP, 'w')],
    "stop": [(Command.KEYUP, 'w')],
    "back": [(Command.KEYDOWN, 's')],
    "right": [(Command.KEYDOWN, 'w'), (Command.KEYDOWN, 'd'), (Command.WAIT, 0.1),
              (Command.KEYUP, 'w'), (Command.KEYUP, 'd')],
    "left": [(Command.KEYDOWN, 'w'), (Command.KEYDOWN, 'a'), (Command.WAIT, 0.1),
             (Command.KEYUP, 'w'), (Command.KEYUP, 'a')],
    "jump": [(Command.KEYPRESS, 'j')],
    "boost": [(Command.KEYPRESS, 'g')],
    "1": [(Command.KEYPRESS, '1')],
    "2": [(Command.KEYPRESS, '2')],
    "3": [(Command.KEYPRESS, '3')],
    "4": [(Command.KEYPRESS, '4')],
    "scoreboard": [(Command.KEYPRESS, 'tab')],
    "bcam": [(Command.KEYPRESS, 'i')],
    "lookback": [(Command.KEYPRESS, 'l')],
    "item": [(Command.KEYPRESS, 'r')],
}
