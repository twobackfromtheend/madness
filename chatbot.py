import logging
from typing import Callable

from twitchio.ext import commands

from twitch_config import *

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class Bot(commands.Bot):
    def __init__(self, message_callback: Callable):
        super().__init__(
            irc_token=OAUTH_TOKEN,
            client_id=CLIENT_ID,
            nick=NICK,
            prefix='!',
            initial_channels=['callumtheshogun']
        )
        self.message_callback = message_callback

    async def event_ready(self):
        print(f'Ready | {self.nick}')

    async def event_message(self, message):
        logger.info(f"Message on {message.channel.name} by {message.author.name}: {message.content}")
        await self.message_callback(message)
