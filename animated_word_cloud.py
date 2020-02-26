import asyncio
import logging
from collections import defaultdict
from queue import Queue, Empty
from typing import NamedTuple, Optional, DefaultDict, List

import matplotlib
import matplotlib.pyplot as plt
from twitchio import Message

from controls import CONTROLS
from word_cloud_utils import generate_annotation, GeneratedAnnotation

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

matplotlib.use("Qt5Agg")

ALPHA_DECAY = 0.92
MAX_SCALE = 6
FIG_SIZE = (8, 4.5)
SLEEP = 0.032

window_closed = False


def handle_close(event):
    global window_closed
    window_closed = True


class QueueMessage(NamedTuple):
    control: str
    author: str
    author_colour: Optional[str]  # This may not be received.


async def show_plot(queue: Queue):
    fig = plt.figure('TwitchWordCloud', figsize=FIG_SIZE)
    fig.canvas.mpl_connect('close_event', handle_close)
    ax = fig.add_subplot(111, frameon=False)

    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)

    def update(annotations: DefaultDict[str, List[GeneratedAnnotation]]):
        # logger.info(f"Updating plot.")
        while True:
            try:
                message: QueueMessage = queue.get_nowait()
                message_control = message.control
                message_scale = len(annotations[message_control]) ** 0.8
                generated_annotation = generate_annotation(ax, message, message_scale=message_scale)
                annotations[message_control].append(generated_annotation)
            except Empty:
                break
        for control, control_annotations in annotations.items():
            remaining_annotations = []
            for generated_annotation in control_annotations:
                alpha = generated_annotation.annotations[0].get_alpha()
                remove = alpha < 0.05
                for annotation in generated_annotation.annotations:
                    if remove:
                        annotation.remove()
                    else:
                        annotation.set_alpha(alpha * ALPHA_DECAY)
                if not remove:
                    remaining_annotations.append(generated_annotation)
            annotations[control] = remaining_annotations

    plt.show(block=False)

    annotations: DefaultDict[str, List[GeneratedAnnotation]] = defaultdict(list)  # Word: [annotations]
    while not window_closed:
        await asyncio.sleep(SLEEP)
        update(annotations)
        fig.canvas.draw_idle()
        plt.pause(0.001)


async def message_callback(message: Message):
    message_content = message.content.lower()
    author = message.author.name
    author_colour = message.author.colour if message.author.colour else None

    for control in CONTROLS:
        if message_content.startswith(control):
            queue.put(QueueMessage(control, author, author_colour))
            logger.info(f"Control by {author}: {control}")
            break


async def main():
    while not window_closed:
        await asyncio.sleep(1)
    bot_task.cancel()


if __name__ == '__main__':
    from chatbot import Bot

    queue = Queue()

    bot = Bot(message_callback)

    loop = asyncio.get_event_loop()
    bot_task = loop.create_task(bot.start())
    plot_task = loop.create_task(show_plot(queue))
    loop.run_until_complete(main())
