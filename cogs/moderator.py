"""BOT moderator commands. Not to be confused with server moderation commands, like muting or kicking.
There are a gazillion bots out there that can do those functions perfectly well. These commands are for 
control of the bot."""
import sys

import discord 
from discord.ext import commands

import datetime

import random
import asyncio
import typing

from tabulate import tabulate

from secret.webhooks import *
from utils import embed as em
from utils import converters
from internal import enumerations as enums

channels_available = ["bot-test","botspam-v2","botspam"]

class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.git_helper_webhook = discord.Webhook.partial(GIT_HELPER['id'], GIT_HELPER['token'], adapter=discord.AsyncWebhookAdapter(self.bot.session))
        self.another_chat_webhook = discord.Webhook.partial(ANOTHERCHAT_HOOK['id'], ANOTHERCHAT_HOOK['token'], adapter=discord.AsyncWebhookAdapter(self.bot.session))
        self.botspam_webhook = discord.Webhook.partial(BOTSPAM_HOOK['id'], BOTSPAM_HOOK['token'], adapter=discord.AsyncWebhookAdapter(self.bot.session))
        self.env = {}

    async def cog_check(self, ctx):
        """Restricts commands to administrators only"""
        return ctx.author.guild_permissions.administrator

    @commands.group(name="change-money",
                    aliases=["c-money","cm"],
                    help="Change a user's balance.")               
    async def change_money(self, ctx):
        pass

    @change_money.command(name="add")
    async def add_money(self, ctx, baltype: str, user: discord.Member, amt: int):
        await self.bot.db_pool.execute(f"UPDATE economy SET {baltype}={baltype} + $1 WHERE user_id=$2", amt, user.id)
        response = em.CrajyEmbed(title="Updating User Balance", description=f"Added {amt} to {user.display_name}\'s {baltype}.", embed_type=enums.EmbedType.SUCCESS)
        response.quick_set_author(ctx.author)
        response.set_thumbnail(url=em.EmbedResource.GREEN_UPDATE.value)
        await ctx.reply(embed=response, mention_author=True) 

    @change_money.command(name="remove")
    async def remove_money(self, ctx, baltype: str, user: discord.Member, amt: int):
        await self.bot.db_pool.execute(f"UPDATE economy SET {baltype}={baltype} - $1 WHERE user_id=$2", amt, user.id)
        response = em.CrajyEmbed(title="Updating User Balance", description=f"Removed {amt} from {user.display_name}\'s {baltype}.", embed_type=enums.EmbedType.FAIL)
        response.quick_set_author(ctx.author)
        response.set_thumbnail(url=em.EmbedResource.RED_UPDATE.value)
        await ctx.reply(embed=response, mention_author=True) 

    @change_money.command(name="set")
    async def set_money(self, ctx, baltype: str, user: discord.Member, amt: int):
        await self.bot.db_pool.execute(f"UPDATE economy SET {baltype}=$1 WHERE user_id=$2", amt, user.id)
        response = em.CrajyEmbed(title="Updating User Balance", description=f"Set {user.display_name}\'s {baltype} to {amt}.", embed_type=enums.EmbedType.BOT)
        response.quick_set_author(ctx.author)
        response.set_thumbnail(url=em.EmbedResource.GREEN_UPDATE.value)
        await ctx.reply(embed=response, mention_author=True) 

    @commands.command(name="remove-user",
                      help="Remove a user from the bot database.")
    async def remove_user(self, ctx, member: discord.Member):
        confirm_embed = em.CrajyEmbed(title="Deleting User Data", description=f"Are you sure you want to delete all of {member.display_name}\'s data?", embed_type=enums.EmbedType.WARNING)
        confirm_embed.set_thumbnail(url=em.EmbedResource.WARNING.value)
        confirm_embed.quick_set_author(self.bot.user)

        ask = await ctx.reply(embed=confirm_embed)
        response = await ctx.get_confirmation(ask)

        if response:
            await self.bot.delete_member(member)
            confirm_embed.description = f"Deleted data for user: {member.display_name}."
            confirm_embed.color = enums.EmbedType.SUCCESS.value
            await ask.edit(embed=confirm_embed)
            await ctx.check_mark()
        else:
            confirm_embed.description = "Did not delete data."
            confirm_embed.color = enums.EmbedType.FAIL.value
            await ask.edit(embed=confirm_embed)
            await ctx.x_mark()         

    @commands.group(name="change-inventory",
                    aliases=["c-inv"],
                    help="Edit a user's inventory.")
    async def change_inventory(self, ctx):
        pass

    @change_inventory.command(name="add")
    async def add_inv(self, ctx, amt: int, item: str, user: discord.Member):
        await self.bot.db_pool.execute(f"UPDATE inventories SET {item}={item} + $1 WHERE user_id=$2", amt, user.id)
        response = em.CrajyEmbed(title="Updating User Inventory", description=f"Added {amt} {item} to {user.display_name}\'s inventory.", embed_type=enums.EmbedType.SUCCESS)
        response.quick_set_author(ctx.author)
        response.set_thumbnail(url=em.EmbedResource.GREEN_UPDATE.value)
        await ctx.reply(embed=response)

    @change_inventory.command(name="remove")
    async def remove_inv(self, ctx, amt: int, item: str, user: discord.Member):
        await self.bot.db_pool.execute(f"UPDATE inventories SET {item}={item} - $1 WHERE user_id=$2", amt, user.id)
        response = em.CrajyEmbed(title="Updating User Inventory", description=f"Remove {amt} {item} from {user.display_name}\'s inventory.", embed_type=enums.EmbedType.FAIL)
        response.quick_set_author(ctx.author)
        response.set_thumbnail(url=em.EmbedResource.RED_UPDATE.value)
        await ctx.reply(embed=response)

    @change_inventory.command(name="set")
    async def set_inv(self, ctx, item: str, user: discord.Member, amt: int):
        await self.bot.db_pool.execute(f"UPDATE inventories SET {item}=$1 WHERE user_id=$2", amt, user.id)
        response = em.CrajyEmbed(title="Updating User Inventory", description=f"Set {amt} {item} to {user.display_name}\'s inventory.", embed_type=enums.EmbedType.BOT)
        response.quick_set_author(ctx.author)
        response.set_thumbnail(url=em.EmbedResource.GREEN_UPDATE.value)
        await ctx.reply(embed=response)

    @commands.command(name="edit-item", 
                    aliases=["edititem"],help="Edit an item on the shop.")
    async def edit_item(self, ctx, item: str, attribute: str, value: int):
        await self.bot.db_pool.execute(f"UPDATE shop SET {attribute}=$1 WHERE item_name=$2", value, item)
        response = em.CrajyEmbed(title="Updating Shop", description=f"Set {item} {attribute} to {value}.", embed_type=enums.EmbedType.BOT)
        response.quick_set_author(ctx.author)
        response.set_thumbnail(url=em.EmbedResource.GREEN_UPDATE.value)
        await ctx.reply(embed=response)    

    @commands.command(name="versions", aliases=['ver'], help="Returns CrajyBot and discord.py versions being used.")
    async def versions(self, ctx):
        embed = em.CrajyEmbed(title="Versions", description=f"[discord.py version: {discord.__version__}](https://github.com/Rapptz/discord.py)\n[Bot version: {self.bot.__version__}](https://github.com/anand2312/CrajyBot-private)", embed_type=enums.EmbedType.INFO)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        return await ctx.reply(embed=embed)

    @commands.command(name="clear-pin", aliases=["clearpins", "clear-pins", "unpin"])
    async def remove_pins(self, ctx, identifiers: commands.Greedy[typing.Union[int, str]]):
        ids, names = [], []
        for i in identifiers:
            if isinstance(i, int):
                ids.append(int(i))
            else:
                names.append(i)

        confirm_embed = em.CrajyEmbed(title="Clearing Pins", embed_type=enums.EmbedType.WARNING)
        listed_pins = "\n".join(f'• {i}' for i in identifiers)
        confirm_embed.quick_set_author(self.bot.user)
        confirm_embed.description = f"Are you sure you want to clear:\n{listed_pins}"
        confirm_embed.set_thumbnail(url=em.EmbedResource.WARNING.value)
        confirm_embed.set_footer(text="This action cannot be undone.")
        ask = await ctx.reply(embed=confirm_embed, mention_author=True)

        response = await ctx.get_confirmation(ask)
        if not response:
            confirm_embed.description = f"Did not delete pins."
            confirm_embed.color = enums.EmbedType.BOT.value
            return await ask.edit(embed=confirm_embed)
        else:
            if len(identifiers) == 1 and identifiers[0].lower() == "all":
                await self.bot.db_pool.execute("DELETE FROM pins")
            else:
                await self.bot.db_pool.execute("DELETE FROM pins WHERE name=ANY($1) OR pin_id=ANY($2)", names, ids)

    @commands.command(name="pin", help="Pins a message to the bot's database. Pins can be viewed with the `pins` command.")
    async def pin(self, ctx, id_: discord.Message, name_: str=None):
        synopsis = id_.content[:30] if id_.content is not None else "<image or embed>"
        url = id_.jump_url
        author = id_.author
        date = datetime.date.today()

        await self.bot.db_pool.fetchval("INSERT INTO pins(synopsis, jump_url, author, pin_date, name) VALUES($1, $2, $3, $4, $5)", synopsis, url, author, date, name_)
        await id_.add_reaction("📌")
        reply_embed = em.CrajyEmbed(title=f"Pinned!", description=f"_{synopsis[:10]+'...'}_\n", embed_type=enums.EmbedType.SUCCESS)
        reply_embed.set_thumbnail(url=em.EmbedResource.PIN.value)
        reply_embed.quick_set_author(self.bot.user)
        reply_embed.set_footer(text=f"Pinned by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=reply_embed)

    @commands.command(name="query", aliases=["db"], help="Query the database. Don't mess with this if you don't know what it is doing.")
    @commands.is_owner()
    async def sql_query(self, ctx, table: str, query: str):
        # wrap query in quotes
        columns =  enums.Table[table.upper()].value
        data = await self.bot.db_pool.fetch(query)
        tabulated = tabulate(data, headers=columns)
        out = "```" + tabulated + "```"
        return await ctx.reply(out, mention_author=True)
                                    
    @commands.command(name="clear")
    async def clear(self, ctx, amount: int, filter: commands.Greedy[converters.KwargConverter] = None):
        if filter:
            def check(message):
                merged_kwargs = {key: value for inner in filter for key, value in inner.items()}
                results = []
                for key, value in merged_kwargs.items():
                    attr = getattr(message, key, None)
                    check_result = attr.name == value or str(attr.id) == value
                    results.append(check_result)
                return any(results)
        else:
            check = None
        deleted = await ctx.channel.purge(limit=amount, check=check)
        return await ctx.send(f"{em.EmbedResource.CHECK_EMOJI.value} Cleared {len(deleted)} messages.", delete_after=5)
    
    @commands.is_owner()
    @commands.command(name="internal-eval", aliases=["int-eval"])
    async def internal_eval(self, ctx, *, code: str):
        code = code.strip("`")
        code = code.lstrip("py")
        real_code = f"""
async def func():
    {textwrap.indent(code, "    ")}
self.env['func'] = func"""
        env = {
            'message': ctx.message,
            'ctx': ctx,
            'discord': discord,
            'self': self,
            'asyncio': asyncio
        }

        eval(compile(real_code, "bruh", "exec"), env)

        await self.env['func']()

        await ctx.check_mark()

    @commands.command(name="reload-module", aliases=["reloadm"])
    async def unload_module(self, ctx, module: str):
        removes = []
        for name in sys.modules:
            if name.startswith(module):
                removes.append(name)
        for name in removes:
            sys.modules.pop(name)
        return await ctx.send(f"Reloaded {module}")

def setup(bot):
    bot.add_cog(Moderator(bot))
