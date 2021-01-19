"""Economy commands. Pretty self explanatory."""
import discord
from discord.ext import commands

from contextlib import suppress
import more_itertools as mitertools

import typing
import asyncio
import random

from utils import embed as em
from internal import enumerations as enums


class EconomyEmbed(em.CrajyEmbed):
    """Made with thumbnail set according to EmbedType passed."""
    def __init__(self, embed_type: enums.EmbedType, **kwargs):
        super().__init__(embed_type=embed_type, **kwargs)
        if embed_type in (enums.EmbedType.BOT, enums.EmbedType.INFO):
            self.set_thumbnail(url=em.EmbedResource.BANK.value)
        elif embed_type == enums.EmbedType.SUCCESS:
            self.set_thumbnail(url=em.EmbedResource.PAYMENT.value)


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        """Restricts these commands to some specific channels. This is server specific, so change the list according to what you need.
        Or you can entirely remove this function."""
        return ctx.channel.name in ["bot-test", "botspam-v2", "botspam"]

    def random_robber(self):
        return random.choice([em.EmbedResource.ROBBER_1.value, em.EmbedResource.ROBBER_2.value])

    def get_item_column(self, inp: str):
        # get corresponding item name column in inventory table. add item names with different column names in this dict.
        mapping = {
            "stock": "stock",
            "heist tools": "heist",
            "chicken": "chicken"
            }
        return mapping.get(inp.lower())

    @commands.command(name="withdraw",
                      aliases=["with"],
                      help="Withdraw money from your account.")
    async def withdraw(self, ctx, amount: typing.Union[int, str]):
        try:
            existing = await ctx.get_user_data(table=enums.Table.ECONOMY)
            if existing['bank'] >= amount:
                await self.bot.db_pool.execute("UPDATE economy SET cash=cash + $1, bank=bank - $1 WHERE user_id=$2", amount, ctx.author.id)
                response = EconomyEmbed(title="Withdrawal", description=f"Withdrew {int(amount)}", embed_type=enums.EmbedType.BOT)
                response.quick_set_author(ctx.author)
                await ctx.reply(embed=response)
            else:
                raise ValueError(f"You do not have that much balance; you're {amount - existing['bank']} short.")
        except TypeError:
            if amount.lower() == "all":
                await self.bot.db_pool.execute("UPDATE economy SET cash=cash + bank, bank=0 WHERE user_id=$1", ctx.author.id)
                response = EconomyEmbed(title="Withdrawal", description=f"Withdrew all money from bank.", embed_type=enums.EmbedType.BOT)
                response.quick_set_author(ctx.author)
                await ctx.reply(embed=response)

    @commands.command(name="deposit",
                      aliases=["dep"],
                      help="Deposit money to your account.")
    async def deposit(self, ctx, amount: typing.Union[int, str]):
        try:
            existing = await ctx.get_user_data(table=enums.Table.ECONOMY)
            if existing['cash'] >= amount:
                await self.bot.db_pool.execute("UPDATE economy SET bank=bank + $1, cash=cash - $1 WHERE user_id=$2", amount, ctx.author.id)
                response = EconomyEmbed(title="Deposit", description=f"Deposited {int(amount)}", embed_type=enums.EmbedType.BOT)
                response.quick_set_author(ctx.author)
                await ctx.reply(embed=response)
            else:
                raise ValueError("You don't have that much moni to deposit")
        except TypeError:
            if amount.lower() == "all":
                await self.bot.db_pool.execute("UPDATE economy SET bank=cash + bank, cash=0 WHERE user_id=$1", ctx.author.id)
                response = EconomyEmbed(title="Deposit", description=f"Deposited all money to bank.", embed_type=enums.EmbedType.BOT)
                response.quick_set_author(ctx.author)
                await ctx.reply(embed=response)
                    
    @commands.command(name='balance',
                      aliases=["bal"],
                      help="Displays your current bank balance.")
    async def balance(self, ctx, user: typing.Union[discord.Member, str]=None):
        if user is None:
            user = ctx.author
        user_data = await self.bot.db_pool.fetchrow("SELECT cash, bank, cash + bank - debt AS networth, debt FROM economy WHERE user_id=$1", user.id)

        response = EconomyEmbed(title="Crajy Bank", description="Balance is:", embed_type=enums.EmbedType.BOT)
        response.add_field(name="Cash Balance: ",value=user_data['cash'], inline=True)
        response.add_field(name="Bank balance: ",value=user_data['bank'], inline=False)
        response.add_field(name="Debt: ",value=user_data['debt'], inline=True)
        response.add_field(name="Net Worth: ",value=user_data['networth'], inline=False)
        response.quick_set_author(user)
        return await ctx.reply(embed=response)

    @commands.command(name='work',
                      help="Do work to earn some money.")
    @commands.cooldown(1, 3600, commands.BucketType.user)  
    async def work(self, ctx):
        rand_val = random.randint(50, 200)
        await self.bot.db_pool.execute("UPDATE economy SET cash = cash + $1 WHERE user_id=$2", rand_val, ctx.author.id)
        response = EconomyEmbed(title="Work", description=f"You earned {rand_val}", embed_type=enums.EmbedType.SUCCESS)
        response.quick_set_author(ctx.author)
        return await ctx.reply(embed=response)

    @commands.command(name='slut',
                      help="Be a slut to earn that dough")
    @commands.cooldown(1, 3600, commands.BucketType.user)          
    async def slut(self, ctx):
        winning_odds=[1, 2, 3, 4, 5, 6]
        if random.randint(1, 10) in winning_odds:
            rand_val = random.randint(60, 200)
            await self.bot.db_pool.execute("UPDATE economy SET cash = cash + $1 WHERE user_id=$2", rand_val, ctx.author.id)
            response = EconomyEmbed(title="You slut.", description=f"You whored out and earned {rand_val}!", embed_type=enums.EmbedType.SUCCESS)
        else:
            rand_val = random.randint(60, 100)
            await self.bot.db_pool.execute("UPDATE economy SET cash = cash - $1 WHERE user_id=$2", rand_val, ctx.author.id)
            response = EconomyEmbed(title="Uh oh...", description=f"You hooked up with a psychopath, lost {rand_val}!", embed_type=enums.EmbedType.FAIL)
            response.set_thumbnail(url=em.EmbedResource.LOSS.value)
        response.quick_set_author(ctx.author)
        return await ctx.reply(embed=response)
    
    @commands.command(name="crime",
                      help="Commit a crime to earn money.")
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def crime(self, ctx):            
        winning_odds=[1, 2, 3, 4]
        if random.randint(1, 10) in winning_odds:
            rand_val = random.randint(150, 400)
            await self.bot.db_pool.execute("UPDATE economy SET cash = cash + $1 WHERE user_id=$2", rand_val, ctx.author.id)
            response = EconomyEmbed(title="Gang shit bro.", description=f"You successfuly commited crime and earned {rand_val}!", embed_type=enums.EmbedType.SUCCESS)
            response.quick_set_author(ctx.author)
            response.set_thumbnail(url=self.random_robber())
        else:
            rand_val = random.randint(150,250)
            await self.bot.db_pool.execute("UPDATE economy SET cash = cash - $1 WHERE user_id=$2", rand_val, ctx.author.id)
            response = EconomyEmbed(title="You're kinda stupid bro.", description=f"You got caught and were fined {rand_val}!", embed_type=enums.EmbedType.FAIL)
            response.set_thumbnail(url=em.EmbedResource.LOSS.value)
        response.quick_set_author(ctx.author)
        return await ctx.reply(embed=response)

    @commands.command(name="leaderboard", 
                      aliases=["top","lb"],
                      help="Economy leaderboard.")   
    async def leaderboard(self, ctx):
        leaderboard_data = await self.bot.db_pool.fetch("SELECT user_id, bank + cash - debt AS networth FROM economy ORDER BY networth DESC")
        embeds = []
        counter = 1
        for chunk in mitertools.chunked(leaderboard_data, 6):
            response = EconomyEmbed(title="Crajy Leaderboard", description="", embed_type=enums.EmbedType.INFO)
            for person in chunk:
                person_obj = ctx.guild.get_member(person['user_id'])
                if person_obj is None:
                    continue
                response.add_field(name=f"{counter}. {person_obj.display_name}", value=f"Net Worth: {person['networth']}", inline=False)
            embeds.append(response)

        pages = em.quick_embed_paginate(embeds)
        return await pages.start(ctx)

    @commands.command(name="get-loan", 
                      aliases=["gl"],
                      help="Take out a loan. Maximum amount you can take is twice your current bank balance."+
                            r"5% interest is applied. 10% fine is applied if you don't repay the loan within 64800 second.")    
    async def loan(self, ctx, loan_val:int):
        raise NotImplementedError
        # make a task loop which checks database periodically for debt times, don't asyncio.sleep for so long.
        """
        user_data = await self.bot.db_pool.fetchrow("SELECT bank, debt FROM economy WHERE user_id=$1", ctx.author.id)
        if loan_val < user_data["bank"] * 2 and user_data["debt"] == 0:
            response = EconomyEmbed(title="Debt.", description=f"You took a loan of {loan_val}!", embed_type=enums.EmbedType.SUCCESS)
            response.quick_set_author(ctx.author) 

            new_debt = (loan_val + int(loan_val * 0.05))
            
            await self.bot.db_pool.execute("UPDATE economy SET debt = $1, cash = cash + $2 WHERE user_id = $3", new_debt, loan_val, ctx.author.id)              
            await ctx.send(embed=response)

            await asyncio.sleep(64800)           
                                   #checks if debt has been repaid, if not sends reminder
                                   #Search for a better option than asyncio.sleep

            user_data = await self.bot.economy_collection.find_one({'user': ctx.author.id})
            if user_data['debt'] != 0:                      
                await ctx.message.author.send("You're about to default on your loan")
            else:
                return
            
            await asyncio.sleep(21600)

            user_data = await self.bot.economy_collection.find_one({'user': ctx.author.id})
            if user_data['debt'] != 0:
                user_data['debt'] = 0
                user_data['cash'] -= (loan_val + int(loan_val * 0.1))
                await self.bot.economy_collection.update_one({'user': ctx.author.id}, {"$set": user_data})
                await ctx.message.author.send(f"poopi you messed up big time")
        else:
            await ctx.message.channel.send("You cannot take a loan greater than twice your current balance / you have an unpaid loan, repay it and try again.")
        """

    @commands.command(name="repay-loan", 
                      aliases=["rl"],
                      help="Repay your loan.")
    async def repay_loan(self, ctx):
        raise NotImplementedError
        """
        user_data = await self.bot.economy_collection.find_one({'user': ctx.author.id})
        if user_data['debt'] > 0:
            if user_data['cash'] >= user_data['debt']:
                user_data['cash'] -= user_data['debt']
                user_data['debt'] = 0
                await self.bot.economy_collection.update_one({'user': ctx.author.id},{"$set": user_data})
                response = discord.Embed(title=ctx.author.id, description="You've paid off your debt!", colour=discord.Color.green())
                return await ctx.send(embed=response)
            else:
                return await ctx.send(f"You do not have enough balance to repay your debt.")

        else:
            return await ctx.send(f"You do not have any debt")
        """

    @commands.command(name="inventory", 
                      aliases=["inv"],
                      help="View your inventory of items.")
    async def inventory(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        user_data = await self.bot.db_pool.fetchrow("SELECT * FROM inventories WHERE user_id = $1", user.id)
        response = EconomyEmbed(title="Inventory", embed_type=enums.EmbedType.INFO)
        response.quick_set_author(user)
        out = []
        data_as_dict = dict(user_data)
        for key, value in data_as_dict.items():
            if key == "user_id":
                continue
            else:
                response.add_field(name=key.capitalize(), value=value, inline=False)
        return await ctx.send(embed=response)

    @commands.command(name='shop',
                      aliases=["store"],
                      help="View the store.")
    async def shop(self, ctx):
        shop_data = await self.bot.db_pool.fetch("SELECT item_name, stock, price FROM shop")
        embeds = []
        for chunk in mitertools.chunked(shop_data, 5):
            response = EconomyEmbed(title="Crajy Shop", description="All available items.", embed_type=enums.EmbedType.INFO)
            for item in chunk:
                stock = "∞" if item["stock"] is None else item["stock"]
                response.add_field(name=item["item_name"], value=f"Stock Remaining: {stock}\nPrice: {item['price']}", inline=False)
            embeds.append(response)
        pages = em.quick_embed_paginate(embeds)
        await pages.start(ctx)

    @commands.command(name="buy", 
                      help="Buy an item from the shop.")                        #IMPORTANT!! - For items that should have unlimited stock, use stock value as None in store_data collection.
    async def buy(self, ctx, number: int, *, item: str):

        store_data = await self.bot.db_pool.fetchrow("SELECT stock, price FROM shop WHERE item_name = $1", item.lower())
        user_cash_data = await self.bot.db_pool.fetchrow("SELECT cash FROM economy WHERE user_id = $1", ctx.author.id)

        if user_cash_data['cash'] >= (number * store_data['price']):
            if store_data['stock'] is not None:
                if store_data['stock'] >= number:
                    new_bal = user_cash_data['cash'] - (number * store_data['price'])
                    await self.bot.db_pool.execute("UPDATE economy SET cash = $1 WHERE user_id = $2", new_bal, ctx.author.id)
                    await self.bot.db_pool.execute(f"UPDATE inventories SET {self.get_item_column(item)} = {self.get_item_column(item)} + $1 WHERE user_id = $2", number, ctx.author.id)
                    await self.bot.db_pool.execute("UPDATE shop SET stock = stock - $1 WHERE item_name = $2", number, item)
                    response = EconomyEmbed(title="Purchase Successful", description=f"You bought {number} {item}s!", embed_type=enums.EmbedType.SUCCESS)      
                    response.quick_set_author(ctx.author)
                    return await ctx.reply(embed=response)
                else:
                    raise ValueError(f"Bruh not enough stock of this item is left.")
            else:
                new_val = user_cash_data['cash'] - (number * store_data['price'])
                await self.bot.db_pool.execute("UPDATE economy SET cash = $1 WHERE user_id = $2", new_bal, ctx.author.id)
                await self.bot.db_pool.execute(f"UPDATE inventories SET {self.get_item_column(item)} = {self.get_item_column(item)} + $1 WHERE user_id = $2", number, ctx.author.id)
                response = EconomyEmbed(title="Purchase Succeessful", description=f"You bought {number} {item}s!", embed_type=enums.EmbedType.SUCCESS)
                response.quick_set_author(ctx.author)
                return await ctx.reply(embed=response)
        else:
            raise ValueError(f"poopi you don't have enough moni {self.bot.get_emoji(703648812669075456)}")

    @commands.command(name="sell",
                      help="Sell an item for the current market price.")
    async def sell(self, ctx, n: int, item: str):
        cur_price = await self.bot.db_pool.fetchval("SELECT price FROM shop WHERE item_name = $1", item)
        await self.bot.db_pool.execute(f"UPDATE inventories SET {self.get_item_column(item)} = {self.get_item_column(item)} - $1 WHERE user_id = $2", n, ctx.author.id)
        await self.bot.db_pool.execute("UPDATE economy SET cash = cash + $1 WHERE user_id = $2", cur_price * n, ctx.author.id)

        response = EconomyEmbed(title="Item Sold.", description=f"You sold {n} {item}s for {cur_price * n}", embed_type=enums.EmbedType.SUCCESS)
        response.quick_set_author(ctx.author)

        return await ctx.reply(embed=response)

    @commands.command(name='givemoney',
                      aliases=["donate"],
                      help="Be a kind soul and give your friends some of your cash.")
    async def givemoney(self, ctx, person: discord.Member, amount: int):
        sender_balance = await self.bot.db_pool.fetchval("SELECT cash FROM economy WHERE user_id = $1", ctx.author.id)
        if sender_balance < amount:
            raise ValueError(f"You don't have that much money; You're short by {amount - sender_balance}")

        if amount < 0:  
            raise ValueError("You can't send negative money poopi")
        else:
            await self.bot.db_pool.execute("UPDATE economy SET cash = cash - $1 WHERE user_id = $2", amount, ctx.author.id)
            await self.bot.db_pool.execute("UPDATE economy SET cash = cash + $1 WHERE user_id = $2", amount, person.id)
            response = EconomyEmbed(title='Money Transfer ', description=f"{ctx.author.mention} transferred {int(amount)} to {person.mention}", embed_type=enums.EmbedType.BOT)
            response.set_thumbnail(url=em.EmbedResource.PAYMENT.value)
        return await ctx.maybe_reply(embed=response, mention_author=True)
                                 
    @commands.command(name="rob",
                      aliases=["steal"],
                      help="Rob your friends.")
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def rob(self, ctx, person: discord.Member):
        robber_heist_tools = await self.bot.db_pool.fetchval("SELECT heist FROM inventories WHERE user_id = $1", ctx.author.id)
        victim = await ctx.get_user_data(table=enums.Table.ECONOMY, member=person)

        if robber_heist_tools > 0 and victim['cash'] > 10:
            await self.bot.db_pool.fetchval("UPDATE inventories SET heist = heist - 1 WHERE user_id = $1", ctx.author.id)
            won = random.choice([True, True, True, False])
            win_percent = random.randint(40, 75)
            
            if won:
                win_amount = int(victim['cash'] * (win_percent/100))
                await self.bot.db_pool.execute("UPDATE economy SET cash = cash + $1 WHERE user_id = $2", win_amount, ctx.author.id)
                await self.bot.db_pool.execute("UPDATE economy SET cash = cash - $1 WHERE user_id = $2", win_amount, person.id)
                response = EconomyEmbed(title="Heist!", description=f"You robbed {win_amount} from {person.mention}", embed_type=enums.EmbedType.SUCCESS)
                response.quick_set_author(ctx.author)
                response.set_thumbnail(url=self.random_robber())
                return await ctx.send(embed=response)
            else:
                fine_amount = random.randint(75, 200)
                await self.bot.db_pool.execute("UPDATE economy SET cash = cash 1 $1 WHERE user_id = $2", fine_amount, ctx.author.id)
                response = EconomyEmbed(title="Uh oh...", description=f"You were caught robbing, and fined {fine_amount}.", embed_type=enums.EmbedType.FAIL)
                response.quick_set_author(ctx.author)
                response.set_thumbnail(url=em.EmbedResource.LOSS)
                return await ctx.send(embed=response)
        else:
            ctx.command.reset_cooldown(ctx)
            raise ValueError("You do not have enough Heist tools items/ person doesn't have enough cash balance.")

    
def setup(bot):
    bot.add_cog(Economy(bot))
