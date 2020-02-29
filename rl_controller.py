import asyncio
import logging
from collections import defaultdict
import datetime
from typing import List, Tuple, Any

import pyautogui

from controls import Command

logger = logging.getLogger(__name__)

KEYDOWN_COOLDOWNS = {
    # arg: cooldown in seconds
    'j': 3,
}

start_time = datetime.datetime.now()
LAST_USE = defaultdict(lambda: start_time)


async def handle_commands(commands: List[Tuple[Command, Any]]):
    for command, arg in commands:
        if command == Command.WAIT:
            await asyncio.sleep(arg)
        elif command == Command.KEYDOWN:
            if arg in KEYDOWN_COOLDOWNS:
                cooldown = KEYDOWN_COOLDOWNS[arg]
                current_time = datetime.datetime.now()
                last_use_time = LAST_USE[arg]
                if not current_time - last_use_time > datetime.timedelta(seconds=cooldown):
                    # Cooldown not complete. Skip input.
                    logger.info(f"Skipping input due to cooldown: {arg}")
                    continue
                else:
                    # Record input, do not skip input.
                    LAST_USE[arg] = current_time
            pyautogui.keyDown(arg)
        elif command == Command.KEYUP:
            pyautogui.keyUp(arg)
        elif command == Command.KEYPRESS:
            pyautogui.press(arg)
