import pylast
import json
from discord.ext import commands
import discord

config = json.load(open('config.json'))

API_KEY = config['last_token']
API_SECRET = config['shared_secret']

last_user_name = config['last_user']
pass_hash = pylast.md5(config['last_pass'])

network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET, username=last_user_name, password_hash=pass_hash)

class Music:
    def __init__(self, bot=None):
        self.bot = bot

    @commands.command(pass_context=True, name='similar-to')
    async def get_similar_artists(self, ctx, *query):   # Add async when finished and ctx
        artist_name, limit = self.parse_query(query)
        artist_object = network.get_artist(artist_name)
        similar_artists = artist_object.get_similar(limit=limit)
        artists = ''

        for i, artist in enumerate(reversed(similar_artists)):
            artists += '{}. {}\n'.format(i+1, artist.item)
        embed = discord.Embed(title='Similar artists', description=artists, color=0x6606BA)
        await self.bot.say(embed=embed)

    def parse_query(self, query):
        artist = []
        limit = 5
        for item in query:
            if item.isdigit():
                limit = item
            elif isinstance(item, str):
                artist.append(item)
        artist_name = ' '.join(artist)
        return artist_name, limit


def setup(bot):
    bot.add_cog(Music(bot))

"""if __name__ == "__main__":
    test = Music()
    test.get_similar_artists('belmont', 100)
"""