import asyncio
import logging

from twitchio import Message

from chatbot import Bot
from controls import CONTROLS
from rl_controller import handle_commands

logger = logging.getLogger(__name__)


async def message_callback(message: Message):
    message_content = message.content.lower()
    author = message.author.name
    for control in CONTROLS:
        if message_content.startswith(control):
            control_commands = CONTROLS[control]
            await handle_commands(control_commands)
            logger.info(f"Control by {author}: {control}")
            break


if __name__ == '__main__':
    bot = Bot(message_callback)

    loop = asyncio.get_event_loop()
    loop.create_task(bot.start())

    loop.run_forever()
