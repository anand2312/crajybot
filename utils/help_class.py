import discord
from discord.ext import commands

class HelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(command_attrs={
            'help': 'Returns help about a command, or a category of commands.',
            'cooldown': commands.Cooldown(1, 3.0, commands.BucketType.member),
        })

    async def send_bot_help(self, mapping):
        ctx = self.context
        bot = ctx.bot

        embed = discord.Embed(color=discord.Color.blurple())
        embed.add_field(name="Usage", value=f"Do `{self.clean_prefix}help <category | command>` to get help on a command or category", inline=False)

        out = ""
        # bot.cogs returns a dict mapping of name:cog
        for cog_name in bot.cogs:
            if cog_name not in ["Control", "ErrorHandler"]: out += cog_name.capitalize() + "\n"

        embed.add_field(name="Categories", value=out, inline=False)
        embed.add_field(name="Contact us", value="[Join our support server](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=False)
        await ctx.send(embed=embed)

    async def send_cog_help(self, cog):
        ctx = self.context
        bot = ctx.bot

        embed = discord.Embed(title=f"Module **{cog.qualified_name}**", description=cog.description, color=discord.Color.blue())
        commands_in_cog = ""
        for command in cog.get_commands():
            commands_in_cog += command.name + "\n"
        embed.add_field(name="**Commands**", value=commands_in_cog, inline=False)
        embed.set_footer(text=f"Do {self.clean_prefix}help <command> to get help on a specific command.")
        await ctx.send(embed=embed)

    async def send_group_help(self, group):
        ctx = self.context
        embed = discord.Embed(title=f"Group - {group.name}",
                              description=f"{group.help} \n **Usage** `{self.get_command_signature(group)}`",
                              color=discord.Color.blue())
        await ctx.send(embed=embed)

    async def send_command_help(self, command):
        ctx = self.context
        if command.root_parent is None:
            embed = discord.Embed(title=f"Help - {command.name}",
                                  description=f"{command.help} \n **Usage** `{self.get_command_signature(command)}` \n **Aliases** `{', '.join(self.command.aliases)}`",
                                  color=discord.Color.blue())
        else:
            embed = discord.Embed(title=f"Help - {command.name}",
                                  description=f"{command.help} \n **Usage** `{self.get_command_signature(command)}` \n **Aliases** `{', '.join(self.command.aliases)}`",
                                  color=discord.Color.blue())
            embed.set_footer(text=f"This command is part of the {command.root_parent.name} group.")

        await ctx.send(embed=embed)

    def get_command_signature(self, command):
        if not command.signature and not command.parent:  # checking if it has no args and isn't a subcommand
            return f'`{self.clean_prefix}{command.name}`'
        if command.signature and not command.parent:  # checking if it has args and isn't a subcommand
            return f'`{self.clean_prefix}{command.name} {command.signature}`'
        if not command.signature and command.parent:  # checking if it has no args and is a subcommand
            return f'`{command.name}`'
        else:  # else assume it has args a signature and is a subcommand
            return f'`{command.name} {command.signature}`'

    @staticmethod
    def get_clean_usage_signature(command):
        """Used in error handler to get clean usage string for commands. Similar to get_command_signature, but without the prefixs"""
        if not command.signature and not command.parent:  # checking if it has no args and isn't a subcommand
            return f'`{command.name}`'
        if command.signature and not command.parent:  # checking if it has args and isn't a subcommand
            return f'`{command.name} {command.signature}`'
        if not command.signature and command.parent:  # checking if it has no args and is a subcommand
            return f'`{command.name}`'
        else:  # else assume it has args a signature and is a subcommand
            return f'`{command.name} {command.signature}`'