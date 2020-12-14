import matplotlib
matplotlib.use("Agg")

import matplotlib.figure import Figure
import numpy as np

import datetime
import io
from typing import Sequence
from dataclasses import dataclass
from collections import namedtuple

import discord


@dataclass
class InstantaneousMetrics:
    """Represents all the data for the metrics stored for a particular datetime object."""
    time: datetime.datetime
    author_counts: dict
    channel_counts: dict
    
    def total_count(self) -> int:
        return sum(self.author_counts.values())

    def get_personal_count(self, person: str) -> int:
        # the expected ID is a string, because they're stored as strings in the database. MongoDB doesn't support integer keys.
        return self.author_counts[person]

    def get_channel_count(self, channel: str) -> int:
        return self.channel_counts[channel]

    def clean_hours_repr(self) -> str:
        return self.time.strftime("%H:%M")    # returns in 00:00 format

    def clean_date_repr(self) -> str:
        return self.time.strftime("%d/%m/%Y")

ImageEmbed = namedtuple("ImageEmbed", "file embed")

def parse_data(db_response: dict) -> InstantaneousMetrics:
    """Convert the mongodb response dictionary into the dataclass instance.
    The dictionary is in the form `{datetime: <time inserted>, author_counts: <dict containing message count for each user>, channel_counts: >dict containing message counts for each channel>}`."""
    return InstantaneousMetrics(time=db_response["datetime"], author_counts=db_response["author_counts"], channel_counts=db_response["channel_counts"])


def graph_hourly_message_count(data: Sequence[InstantaneousMetrics]) -> ImageEmbed:
    # data for x and y axes
    x_array = np.array([x.clean_hours_repr() for x in data])
    y_array = np.array([y.total_count() for y in data])
    # prepare bytes buffer using _make_graph function
    buffer = _make_graph("Total messages sent, hourly", xlabel="Time", ylabel="Messages", x_axis=x_array, y_axis=y_array)
    return make_discord_embed(buffer)


def _make_graph(title: str, *, xlabel: str, ylabel: str ,x_axis: np.array, y_axis: np.array) -> io.BytesIO:
    """A general graphing function that is called by all other functions."""
    fig, = Figure()
    ax = fig.subplots()

    ax.plot(x_axis, y_axis)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # a bytes buffer to which the generated graph image will be stored, instead of saving every graph image.
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inchex="tight")     # saves file with name <date>-<first plotted hour>-<last plotted hour>
    plt.close(fig)
    buffer.seek(0)
    
    return buffer

def make_discord_embed(image_buffer: io.BytesIO) -> ImageEmbed:
    """Converts the BytesIO buffer into a discord.File object that can be sent to any channel."""
    file_for_discord = discord.File(fp=image_buffer, filename="metrics-crajybot.png")
    embed = discord.Embed()
    embed.set_image(url="attachment://metrics-crajybot.png")
    return ImageEmbed(file_for_discord, embed)