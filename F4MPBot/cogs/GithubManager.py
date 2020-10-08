from github import Github
import discord
import json
import logging
import os
from discord.ext import commands, menus

COG_DIR = os.path.dirname(os.path.abspath(__file__))

GithubBot = Github("Insert Github Personal Access Token (needs read and write permissions for org)")


class GithubCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = logging.getLogger(__name__)

    @commands.command(brief='<Project Column Name>',
                      description='This command is used for looking at F4MP Github project tasks. \n Note: May need '
                                  'to use quotations for multiword args (i.e "Multi Word Arg")')
    @commands.has_role('Contributor')
    async def ProjectTasks(self, ctx, args=""):
        print(args)
        if (args in ["In progress", "in Progress", "in progress", "In Progress"]):
            taskColumn = GithubBot.get_project_column(10872509)
            print(taskColumn.get_cards())
            for card in taskColumn.get_cards():
                cardContents = discord.Embed(title="Project Task:", description=card.note, color=0x3075C6)
                await ctx.send(embed=cardContents)

        elif (args in ["todo", "Todo", "To-Do", "to-do"]):
            taskColumn = GithubBot.get_project_column(10872508)
            print(taskColumn.get_cards())
            for card in taskColumn.get_cards():
                cardContents = discord.Embed(title="Project Task:", description=card.note, color=0x3075C6)
                await ctx.send(embed=cardContents)

        elif (args in ["done", "Done", "DONE"]):
            taskColumn = GithubBot.get_project_column(10872510)
            print(taskColumn.get_cards())
            for card in taskColumn.get_cards():
                cardContents = discord.Embed(title="Project Task:", description=card.note, color=0x3075C6)
                await ctx.send(embed=cardContents)

        elif (args in ["META", "Meta", "meta"]):
            taskColumn = GithubBot.get_project_column(10872662)
            print(taskColumn.get_cards())
            for card in taskColumn.get_cards():
                cardContents = discord.Embed(title="Contributors", description=card.note, color=0x3075C6)
                await ctx.send(embed=cardContents)

        else:
            await ctx.send("No matching column found, check spelling and try again!")

    @commands.command(brief='<Project Column Name> <Project Card Contents>',
                      description="Use this command to add cards to F4MP indev project.")
    @commands.has_role('Contributor')
    async def CreateTask(self, ctx, args, args2):

        if (args in ["In progress", "in Progress", "in progress", "In Progress"]):
            taskColumn = GithubBot.get_project_column(10872509)
            taskColumn.create_card(note=args2)
            await ctx.send("Card added!")

        elif (args in ["todo", "Todo", "To-Do", "to-do"]):
            taskColumn = GithubBot.get_project_column(10872508)
            taskColumn.create_card(note=args2)
            await ctx.send("Card added!")

        elif (args in ["done", "Done", "DONE"]):
            taskColumn = GithubBot.get_project_column(10872510)
            taskColumn.create_card(note=args2)
            await ctx.send("Card added!")

        elif (args in ["META", "Meta", "meta"]):
            taskColumn = GithubBot.get_project_column(10872662)
            taskColumn.create_card(note=args2)
            await ctx.send("Card added!")

        else:
            await ctx.send("No matching column found, check spelling and try again!")


def setup(bot):
    bot.add_cog(GithubCommands(bot))
