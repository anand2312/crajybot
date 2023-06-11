import sys
import typing

import aiohttp
import discord
from discord.ext import commands

from internal.bot import CrajyBot
from internal.context import CrajyContext
from internal.enumerations import EmbedType
from utils.converters import LanguageConverter, CodeBlockConverter
from utils import embed as em


PISTON_API_URL = "https://emkc.org/api/v1/piston/execute"
MYSTBIN_API_URL = "https://mystb.in/api/pastes"


class Miscellaneous(commands.Cog):
    def __init__(self, bot: CrajyBot) -> None:
        self.bot = bot

    async def _run_eval(self, ctx: CrajyContext, language: str, code: str) -> dict:
        json = {"language": language, "source": code}
        async with ctx.typing():
            async with self.bot.session.post(PISTON_API_URL, json=json) as response:
                return await response.json()

    async def get_mystbin_link(
        self, content: str, syntax: typing.Optional[str] = None
    ) -> dict:
        multi_part_writer = aiohttp.MultipartWriter()
        paste_content = multi_part_writer.append(content)
        paste_content.set_content_disposition("form-data", name="data")
        paste_content = multi_part_writer.append_json(
            {"meta": [{"index": 0, "syntax": syntax}]}
        )
        paste_content.set_content_disposition("form-data", name="meta")

        async with self.bot.session.post(
            MYSTBIN_API_URL, data=multi_part_writer
        ) as response:
            return await response.json()

    @commands.command(
        name="versions",
        aliases=["ver"],
        help="Returns CrajyBot and discord.py versions being used.",
    )
    async def versions(self, ctx: CrajyContext) -> None:
        # TODO: move this to some other cog
        embed = em.CrajyEmbed(
            title="Versions",
            description=(
                f"[discord.py version: {discord.__version__}](https://github.com/Rapptz/discord.py)\n"
                f"[Python version: {sys.version}](https://python.org)"
            ),
            embed_type=EmbedType.INFO,
        )

        if self.bot.user is not None:
            if self.bot.user.avatar is None:
                av = self.bot.user.default_avatar
            else:
                av = self.bot.user.avatar
            embed.set_thumbnail(url=av.url)
        await ctx.reply(embed=embed)

    @commands.command(name="eval", aliases=("e", "run"))
    @commands.max_concurrency(1, commands.BucketType.user)
    async def _eval(
        self,
        ctx: CrajyContext,
        language: typing.Optional[LanguageConverter],
        *,
        code: CodeBlockConverter,
    ):
        if not language:
            if code[0]:  # type: ignore
                language = code[0].group("lang")  # type: ignore

        code = code[1]  # type: ignore
        eval_data = await self._run_eval(ctx, language, code)  # type: ignore

        msg = eval_data.get("message")
        if msg:
            return await ctx.reply(
                embed=em.CrajyEmbed(
                    title="That didn't go as expected.",
                    description=msg,
                    embed_type=EmbedType.FAIL,
                )
            )
        if eval_data["language"] in ("python2", "python3"):
            eval_data["language"] = "python"

        output = eval_data["output"].strip().replace("```", "`\u200b``")
        link = None
        lines = output.splitlines()
        if len(lines) > 15:
            lines = "\n".join(lines)
            output = f"{lines[:15]}\n ... \nTruncated (too many lines)"
            link = await self.get_mystbin_link(
                eval_data["output"].strip(), eval_data["language"]
            )
            link = f"**Full output [here](https://mystb.in/{link['pastes'][0]['id']})**"
        elif len(output) > 1500:
            output = f"{output[:1500]}\n ... \nTruncated (output too long)\n "
            link = await self.get_mystbin_link(
                eval_data["output"], eval_data["language"]
            )
            link = (
                f"***Full output [here](https://mystb.in/{link['pastes'][0]['id']})***"
            )

        embed = em.CrajyEmbed(
            title=f"Ran your code in `{eval_data['language']}`",
            description=f"```{eval_data['language']}\n{output}```"
            if output
            else "No output",
            embed_type=EmbedType.SUCCESS,
        )
        if link:
            assert embed.description
            embed.description += f"\n{link}"
        await ctx.send(embed=embed)
