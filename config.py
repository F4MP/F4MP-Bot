import os


class bot:
    token = os.environ["BOT_TOKEN"]
    prefix = "!"
    description = "Bot for the F4MP discord server."
    initial_extensions = ["cogs.troubleshooter", "cogs.GithubManager"]
