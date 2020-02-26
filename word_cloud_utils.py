import logging
import random
from typing import TYPE_CHECKING, Tuple, NamedTuple, List

from matplotlib.text import Annotation

if TYPE_CHECKING:
    from animated_word_cloud import QueueMessage

logger = logging.getLogger(__name__)

VERTICAL_CHANCE = 0.13
MESSAGE_BASE_SIZE = 20
MESSAGE_MAX_SCALE = 6


class GeneratedAnnotation(NamedTuple):
    annotations: List[Annotation]


def generate_annotation(ax, queue_message: 'QueueMessage', message_scale: float = 1) -> GeneratedAnnotation:
    message_scale = max(1, min(message_scale, MESSAGE_MAX_SCALE))
    x_loc, y_loc = generate_random_location()

    if random.random() < VERTICAL_CHANCE:
        rotation = -90 if random.getrandbits(1) else 90
    else:
        rotation = 0

    control_horizontal_alignment = "center"
    author_horizontal_alignment = "center"
    control_vertical_alignment = "center"
    author_vertical_alignment = "center"

    if rotation == 0:
        control_vertical_alignment = "bottom"
        author_vertical_alignment = "top"
    elif rotation > 0:
        control_horizontal_alignment = "right"
        author_horizontal_alignment = "left"
    elif rotation < 0:
        control_horizontal_alignment = "left"
        author_horizontal_alignment = "right"

    message_annotation = ax.annotate(
        queue_message.control,
        xy=(x_loc, y_loc),
        fontsize=MESSAGE_BASE_SIZE * message_scale,
        xycoords='figure fraction',
        color='k' if queue_message.author_colour is None else queue_message.author_colour,
        rotation=rotation,
        horizontalalignment=control_horizontal_alignment,
        verticalalignment=control_vertical_alignment,
        alpha=1,
    )

    author_annotation = ax.annotate(
        queue_message.author,
        xy=(x_loc, y_loc),
        fontsize=6,
        xycoords='figure fraction',
        color='k' if queue_message.author_colour is None else queue_message.author_colour,
        rotation=rotation,
        horizontalalignment=author_horizontal_alignment,
        verticalalignment=author_vertical_alignment,
        alpha=1,
    )

    # clear_new_location(ax, new_annotation)
    return GeneratedAnnotation([message_annotation, author_annotation])


def generate_random_location() -> Tuple[float, float]:
    x_lim = 0.8
    y_lim = 0.9

    x_multiplier = 1 if random.getrandbits(1) else -1
    y_multiplier = 1 if random.getrandbits(1) else -1

    x_loc = 0.5 + random.uniform(x_lim, 0) * x_multiplier / 2
    y_loc = 0.5 + random.uniform(y_lim, 0) * y_multiplier / 2

    return x_loc, y_loc


def clear_new_location(ax, new_annotation: Annotation):
    current_children = ax.get_children()
    new_annotation_extents = new_annotation.get_window_extent().extents
    # Extents are (x0, y0, x1, y1)

    for old_annotation in current_children:
        if isinstance(old_annotation, Annotation):
            try:
                old_annotation_extents = old_annotation.get_window_extent().extents
                if new_annotation_extents[2] - old_annotation_extents[0] >= 0 \
                        and old_annotation_extents[2] - new_annotation_extents[0] >= 0 \
                        and new_annotation_extents[3] - old_annotation_extents[1] >= 0 \
                        and old_annotation_extents[3] - new_annotation_extents[1] >= 0:
                    old_annotation.remove()
            except Exception as e:
                logger.exception(e)
