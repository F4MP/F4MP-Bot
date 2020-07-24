import os
import json
import logging
import discord
from discord.ext import commands, menus

COG_DIR = os.path.dirname(os.path.abspath(__file__))


class BinaryTree:
    def __init__(self, val, yes=None, no=None, parent=None):
        self.val = val
        self.parent = parent
        self.yes = yes
        self.no = no

    def to_embed(self, msg, cursor):
        if self.yes is None and self.no is None:
            val = "\n\n*You have reached the end of the troubleshooter. " \
                  "If this did not help you, ask for help in one of the help channels.*"
        else:
            val = "\n\nIf yes, press :white_check_mark:, otherwise, press :x:"
        val = self.val + val
        embed = discord.Embed(title="Troubleshooter", description=val,
                              timestamp=msg.created_at)

        embed.set_author(name=msg.author.name, icon_url=msg.author.avatar_url)
        embed.set_footer(text=f"Position: {cursor}")
        return embed

    @classmethod
    def from_dict(cls, data):
        if data:
            self = cls.__new__(cls)
            self.val = data["val"]
            self.yes = cls.from_dict(data["yes"])
            self.no = cls.from_dict(data["no"])

            if self.yes is not None:
                self.yes.parent = self
            if self.no is not None:
                self.no.parent = self
            return self
        else:
            return None

    def __getitem__(self, item):
        if item == 0 and self.yes is not None:
            return self.yes
        elif item == 1 and self.no is not None:
            return self.no
        else:
            return IndexError(item)


class TroubleshooterMenu(menus.Menu):
    with open(os.path.join(COG_DIR, "troubleshoot.json")) as f:
        base_tree = BinaryTree.from_dict(json.load(f))
    del f

    def __init__(self, message):
        super().__init__(check_embeds=True, clear_reactions_after=True)
        self.tree = self.base_tree
        self.invoke_msg = message
        self.pos = ["0"]

    @property
    def cursor(self):
        return "".join(self.pos)

    async def send_initial_message(self, ctx, channel):
        embed = self.tree.to_embed(self.invoke_msg, self.cursor)
        return await channel.send(embed=embed)

    @menus.button('\N{WHITE HEAVY CHECK MARK}')
    async def yes(self, payload):
        self.tree = self.tree.yes
        await self.message.edit(embed=self.tree.to_embed(self.invoke_msg, self.cursor))
        if self.tree.yes is None and self.tree.no is None:
            self.stop()
        self.pos.append("1")

    @menus.button('\N{CROSS MARK}')
    async def no(self, payload):
        self.tree = self.tree.no
        await self.message.edit(embed=self.tree.to_embed(self.invoke_msg, self.cursor))
        if self.tree.yes is None and self.tree.no is None:
            self.stop()
        self.pos.append("0")


class Troubleshooter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = logging.getLogger(__name__)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def troubleshoot(self, ctx):
        troubleshooter = TroubleshooterMenu(ctx.message)
        if channel := ctx.author.dm_channel is None:
            await ctx.author.create_dm()
            channel = ctx.author.dm_channel
        await troubleshooter.start(ctx, channel=channel)
        if not isinstance(ctx.channel, discord.DMChannel):
            await ctx.send(f"{ctx.author.mention} Check your DM's!", delete_after=10)
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Troubleshooter(bot))
