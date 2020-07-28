import os, datetime
from discord.ext import commands
from util.models import session_scope, Guild


class Bot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with session_scope() as session:
            self.prefixes = dict(
                session.query(Guild.id, Guild.prefix).all())  # Map each prefix by the guild id

        print(self.prefixes)

    async def on_ready(self):
        print(f'{self.user.name} is loading...')

        filenames = [f[:-3] for f in os.listdir('./cogs') if f.endswith('.py')]

        for filename in filenames:
            self.load_extension(f'cogs.{filename}')

        print("All extensions have been loaded")

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(error)
        elif not isinstance(error, commands.CommandNotFound):
            print(f'Error in {ctx.cog} at {str(datetime.now())[:-7]}:\n{error}')


def get_prefix(client, msg):
    prefix = client.prefixes.get(msg.guild.id) or "+"

    return [prefix, f'<@!{client.user.id}> ', f'<@!{client.user.id}>']


if __name__ == "__main__":
    client = Bot(command_prefix=get_prefix, help_command=None)
    client.run()
