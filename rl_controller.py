import asyncio
import logging
from typing import List, Tuple, Any

import pyautogui

from controls import Command

logger = logging.getLogger(__name__)


async def handle_commands(commands: List[Tuple[Command, Any]]):
    for command, arg in commands:
        if command == Command.WAIT:
            await asyncio.sleep(arg)
        elif command == Command.KEYDOWN:
            pyautogui.keyDown(arg)
        elif command == Command.KEYUP:
            pyautogui.keyUp(arg)
        elif command == Command.KEYPRESS:
            pyautogui.press(arg)
