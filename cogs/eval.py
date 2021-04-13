import typing

import aiohttp
import discord
from discord.ext import commands

from internal.bot import CrajyBot
from internal.enumerations import EmbedType
from utils.converters import LanguageConverter, CodeBlockConverter
from utils.embed import CrajyEmbed

PISTON_API_URL = "https://emkc.org/api/v1/piston/execute"
MYSTBIN_API_URL = "https://mystb.in/api/pastes"


class Miscellaneous(commands.Cog):
    def __init__(self, bot: CrajyBot):
        self.bot = bot

    async def _run_eval(self, ctx: commands.Context, language: str, code: str) -> dict:
        json = {'language': language, 'source': code}
        async with ctx.typing():
            async with self.bot.session.post(PISTON_API_URL, json=json) as response:
                return await response.json()
            
    async def get_mystbin_link(self, content: str, syntax: str = None):
        multi_part_writer = aiohttp.MultipartWriter()
        paste_content = multi_part_writer.append(content)
        paste_content.set_content_disposition("form-data", name="data")
        paste_content = multi_part_writer.append_json(
            {"meta": [{"index": 0, "syntax": syntax}]}
        )
        paste_content.set_content_disposition("form-data", name="meta")

        async with self.bot.session.post(MYSTBIN_API_URL, data=multi_part_writer) as response:
            return await response.json()

    @commands.command(name="eval", aliases=("e", "run"))
    @commands.max_concurrency(1, commands.BucketType.user)
    async def _eval(
        self,
        ctx: commands.Context,
        language: typing.Optional[LanguageConverter],
        *,
        code: CodeBlockConverter):

        if not language:
            if code[0]:
                language = code[0].group("lang")
        
        code = code[1]
        eval_data = await self._run_eval(ctx, language, code)
        
        msg = eval_data.get("message")
        if msg:
            return await ctx.reply(
                embed=CrajyEmbed(
                    title="That didn't go as expected.", description=msg, embed_type=EmbedType.FAIL
                )
            )
        if eval_data["language"] in ("python2", "python3"):
            eval_data["language"] = "python"

        output = eval_data["output"].strip().replace("```", '`\u200b``')
        link=None
        lines = output.splitlines()
        if len(lines) > 15:
            lines = '\n'.join(lines)
            output = f"{lines[:15]}\n ... \nTruncated (too many lines)"
            link = await self.get_mystbin_link(eval_data['output'].strip(), eval_data['language'])
            link = f"**Full output [here](https://mystb.in/{link['pastes'][0]['id']})**"
        elif len(output) > 1500:
            output = f"{output[:1500]}\n ... \nTruncated (output too long)\n "
            link = await self.get_mystbin_link(eval_data['output'], eval_data['language'])
            link = f"***Full output [here](https://mystb.in/{link['pastes'][0]['id']})***"

        embed = CrajyEmbed(
            title=f"Ran your code in `{eval_data['language']}`",
            description=f"```{eval_data['language']}\n{output}```" if output else "No output",
            embed_type=EmbedType.SUCCESS 
        )
        if link:
            embed.description += f"\n{link}"
        await ctx.send(embed=embed)

def setup(bot: CrajyBot):
    bot.add_cog(Miscellaneous(bot))
