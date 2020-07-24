import datetime
import json
import logging
from collections import deque
import aiohttp
import discord
from discord.ext import commands

from . import config

log = logging.getLogger(__name__)


def _prefix_callable(bot, msg):
    user_id = bot.user.id
    base = [f"<@!{user_id}> ", f"<@{user_id}> "]
    if msg.guild is None:
        base.extend(["?", "!", ""])
    else:
        base.append(config.bot.prefix)
    return base


class F4MPBot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=_prefix_callable, description=config.bot.description,
                         pm_help=None, help_attrs=dict(hidden=True),
                         fetch_offline_members=False, heartbeat_timeout=150.0)

        self.session = aiohttp.ClientSession(loop=self.loop)
        self._prev_events = deque(maxlen=10)

        self.uptime = None

        for extension in config.bot.initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                log.error(f"Failed to load extension {extension}.", exc_info=e)
                raise

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send("This command cannot be used in private messages.")
        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send("Sorry. This command is disabled and cannot be used.")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.author.send("This command is currently on cooldown,"
                                  f" please wait {int(error.retry_after)} seconds.")
        elif isinstance(error, commands.CommandInvokeError):
            original = error.original
            if not isinstance(original, discord.HTTPException):
                log.error(f"In {ctx.command.qualified_name}:", exc_info=original)
        elif isinstance(error, commands.ArgumentParsingError):
            await ctx.send(error)

    async def on_ready(self):
        self.uptime = datetime.datetime.utcnow()

        log.info(f"Ready: {self.user} (ID: {self.user.id})")

    async def close(self):
        await super().close()
        await self.session.close()

    def run(self):
        try:
            super().run(config.bot.token, reconnect=True)
        finally:
            self.close()
            with open('prev_events.log', 'w', encoding='utf-8') as fp:
                for data in self._prev_events:
                    try:
                        x = json.dumps(data, indent=4)
                    except:
                        fp.write(f'{data}\n')
                    else:
                        fp.write(f'{x}\n')
