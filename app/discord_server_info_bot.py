import os
import sys
import discord
import requests
from app.constants import Constants


SCRIPT_NAME = os.path.basename(__file__)


class DiscordServerInfoBot(discord.Client):
    def __init__(self, **options):
        super().__init__(**options)
        self.on_ready_actions = self.logout

    def on_server_event(self, event):
        try:
            self.on_ready_actions = getattr(self, f'_on_{event}')
        except AttributeError:
            sys.exit(f'[ERROR] {SCRIPT_NAME}: server event \'{event}\' does not exist')

        self.run(Constants.DISCORD_BOT_ACCESS_TOKEN)

    async def _on_launch(self):
        server_ip = requests.get('https://ident.me/').text or ''
        channel = self.get_channel(Constants.DISCORD_CHANNEL_ID)

        message = f'Hi there 👋, server is running now, JOIN ASAP. ⛏💎\nServer IP: **{server_ip}**'
        await channel.send(message)

        await self.logout()

    async def _on_shutdown(self):
        channel = self.get_channel(Constants.DISCORD_CHANNEL_ID)
        message = f'Server is off now ⛔, waiting for you again. 🧐'
        await channel.send(message)
        await self.logout()

    async def on_ready(self):
        await self.on_ready_actions()


def main():
    if len(sys.argv) != 2:
        sys.exit(f'[ERROR] {SCRIPT_NAME}: only one argument is allowed ({len(sys.argv) - 1} given)')

    server_event = sys.argv[1]
    discord_server_info_bot = DiscordServerInfoBot()
    discord_server_info_bot.on_server_event(server_event)


if __name__ == '__main__':
    main()
