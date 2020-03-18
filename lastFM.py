import pylast
import json
from discord.ext import commands
import discord
import requests
import matplotlib.pyplot as plt
import numpy as np

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

    @commands.command(pass_context=True, name='info-on')
    async def get_artist_info(self, ctx, *query):
        artist_name, limit = self.parse_query(query)
        artist_object = network.get_artist(artist_name)
        embed = discord.Embed(title='Info about {}'.format(artist_name), description=artist_object.get_bio_summary(language='en'), color=0x6606BA)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, name='top-artists')
    async def get_top_artists(self, ctx):
        top_artists = network.get_top_artists(limit=20)
        artists = ''
        for i, artist in enumerate(reversed(top_artists)):
            artists += '{}. {}\n'.format(i+1, artist.item)
        embed = discord.Embed(title='Top 20 artists', description=artists, color=0x6606BA)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, name='top-tracks')
    async def get_top_tracks(self, ctx):
        top_tracks = network.get_top_tracks(limit=20)
        tracks = ''
        for i, artist in enumerate(reversed(top_tracks)):
            tracks += '{}. {}\n'.format(i+1, artist.item)
        embed = discord.Embed(title='Top 20 tracks', description=tracks, color=0x6606BA)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, name='top-albums-for')
    async def get_artist_top_albums(self, ctx, *query):
        artist_name, limit = self.parse_query(query)
        artist_object = network.get_artist(artist_name)
        top_albums = artist_object.get_top_albums(limit=limit)
        self.get_album_metadata(top_albums)
        albums = ''
        for i, artist in enumerate(reversed(top_albums)):
            albums += '{}. {}\n'.format(i+1, artist.item)
        embed = discord.Embed(title='Top albums for {}'.format(artist_name), description=albums, color=0x6606BA)
        await self.bot.say(embed=embed)

    def get_album_metadata(self, albums_json):
        x_labels = []
        y_values = []
        listeners = []
        playcounts = []
        track_count = []
        for album in albums_json:
            query = str(album.item).split(' - ')
            x_labels.append(query[1])
            json = self.get_json(query)
            listeners.append(json['album']['listeners'])
            playcounts.append(json['album']['playcount'])
            track_count.append(len(json['album']['tracks']['track']))
        y_values.append(listeners)
        y_values.append(playcounts)
        y_values.append(track_count)
        print(x_labels)
        print(y_values)
        return x_labels, y_values

    def album_barchart(self, X, Y): # THIS FUNCTION IS NOT RIGHT
        n_groups = 5
        means_frank = (90, 55, 40, 65)
        means_guido = (85, 62, 54, 20)

        # create plot
        fig, ax = plt.subplots(3, 1, 1)
        index = np.arange(n_groups)
        bar_width = 0.35
        opacity = 0.8

        rects1 = ax.bar(index, means_frank, bar_width,
                         alpha=opacity,
                         color='b',
                         label='Frank')

        rects2 = ax.bar(index + bar_width, means_guido, bar_width,
                         alpha=opacity,
                         color='g',
                         label='Guido')

        plt.xlabel('Person')
        plt.ylabel('Scores')
        plt.title('Scores by person')
        plt.xticks(index + bar_width, ('A', 'B', 'C', 'D'))
        plt.legend()

        plt.tight_layout()
        plt.show()

    def get_json(self, query):
        artist_name = query[0]
        artist_album = query[1]
        url = 'http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={}&artist={}&album={}&format=json'.format(API_KEY, artist_name, artist_album)
        album_metadata = requests.get(url)
        album_json = album_metadata.json()
        print(url)

        return album_json

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