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

# TODO LIST
# TAGS:
# Get top tags
# Get top albums/tracks/artists by tag
# GEO:
# Get top artists by country
# Get top tracks by country

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
        """
        Get the top 20 tracks on the Last FM API.
        :param ctx:
        :return: String with top 20 tracks on LastFm
        """
        top_tracks = network.get_top_tracks(limit=20)
        tracks = ''
        for i, artist in enumerate(reversed(top_tracks)):
            tracks += '{}. {}\n'.format(i+1, artist.item)
        embed = discord.Embed(title='Top 20 tracks', description=tracks, color=0x6606BA)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, name='top-tags')
    async def get_top_tags(self, ctx, *query):
        top_tags = network.get_top_tags(limit=10)
        tags = ''
        for i, tag in enumerate(reversed(top_tags)):
            tags += '{}. {}\n'.format(i+1, tag.item)
        embed = discord.Embed(title='Top 10 tags', description=tags, color=0x6606BA)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, name='top-albums-for-tag')
    async def get_top_albums_by_tag(self, ctx, *query):
        tag = ' '.join(query)
        albums = self.get_json(tag, 'TAG1')
        if 'albums' not in albums:
            await self.bot.say('{} is not a tag. Try again.'.format(tag))
            return
        album_tags = ''
        for i, album in enumerate(albums['albums']['album']):
            album_tags += '{}. {} - {}\n'.format(i+1, album['name'], album['artist']['name'])
        embed = discord.Embed(title='Top 10 albums for {}'.format(albums['albums']['@attr']['tag']), description=album_tags, color=0x6606BA)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, name='top-artists-for-tag')
    async def get_top_artists_by_tag(self, ctx, *query):
        tag = ' '.join(query)
        artists = self.get_json(tag, 'TAG2')
        if 'topartists' not in artists:
            await self.bot.say('{} is not a tag. Try again.'.format(tag))
            return
        artist_tags = ''
        for i, artist in enumerate(artists['topartists']['artist']):
            artist_tags += '{}. {}\n'.format(i+1, artist['name'])
        embed = discord.Embed(title='Top 10 artists for {}'.format(artists['topartists']['@attr']['tag']), description=artist_tags, color=0x6606BA)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, name='top-tracks-for-tag')
    async def get_top_tracks_by_tag(self, ctx, *query):
        tag = ' '.join(query)
        tracks = self.get_json(tag, 'TAG3')
        if 'tracks' not in tracks:
            await self.bot.say('{} is not a tag. Try again.'.format(tag))
            return
        track_tags = ''
        for i, track in enumerate(tracks['tracks']['track']):
            track_tags += '{}. {}  -  {}\n'.format(i + 1, track['name'], track['artist']['name'])
        embed = discord.Embed(title='Top 10 artists for {}'.format(tracks['tracks']['@attr']['tag']), description=track_tags, color=0x6606BA)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, name='top-artists-for-country')
    async def get_top_artists_by_country(self, ctx, *query):
        country = ' '.join(query)
        artists = self.get_json(country, 'GEO1')
        if 'topartists' not in artists:
            await self.bot.say('{} is not a country. Try again.'.format(country))
            return
        artist_country = ''
        for i, artist in enumerate(artists['topartists']['artist']):
            artist_country += '{}. {}\n'.format(i+1, artist['name'])
        embed = discord.Embed(title='Top 10 artists for {}'.format(artists['topartists']['@attr']['country']), description=artist_country, color=0x6606BA)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, name='top-tracks-for-country')
    async def get_top_tracks_by_country(self, ctx, *query):
        country = ' '.join(query)
        tracks = self.get_json(country, 'GEO2')
        if 'tracks' not in tracks:
            await self.bot.say('{} is not a country. Try again.'.format(country))
            return
        track_country = ''
        for i, track in enumerate(tracks['tracks']['track']):
            track_country += '{}. {} - {}\n'.format(i+1, track['name'], track['artist']['name'])
        embed = discord.Embed(title='Top 10 tracks for {}'.format(tracks['tracks']['@attr']['country']), description=track_country, color=0x6606BA)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, name='top-albums-for')
    async def get_artist_top_albums(self, ctx, *query):
        artist_name, limit = self.parse_query(query)
        artist_object = network.get_artist(artist_name)
        top_albums = artist_object.get_top_albums(limit=limit)
        X, Y = self.get_last_metadata(top_albums, 'TA')
        self.barchart(artist_name, X, Y, 'TA')
        albums = ''
        for i, artist in enumerate(reversed(top_albums)):
            albums += '{}. {}\n'.format(i+1, artist.item)
        embed = discord.Embed(title='Top albums for {}'.format(artist_name), description=albums, color=0x6606BA)
        await self.bot.send_file(ctx.message.channel, 'images/top_5.png')
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, name='top-tracks-for')
    async def get_artist_top_tracks(self, ctx, *query):
        artist_name, limit = self.parse_query(query)
        artist_object = network.get_artist(artist_name)
        top_tracks = artist_object.get_top_tracks(limit=10)
        X, Y = self.get_last_metadata(top_tracks, 'TT')
        self.barchart(artist_name, X, Y, 'TT')
        tracks = ''
        for i, artist in enumerate(reversed(top_tracks)):
            tracks += '{}. {}\n'.format(i+1, artist.item)
        embed = discord.Embed(title='Top tracks for {}'.format(artist_name), description=tracks, color=0x6606BA)
        await self.bot.send_file(ctx.message.channel, 'images/top_5.png')
        await self.bot.say(embed=embed)

    def get_last_metadata(self, _json, flag):
        x_labels = []
        y_values = []
        listeners = []
        playcounts = []
        track_count = []
        duration = []
        for item in _json:
            query = str(item.item).split(' - ')
            x_labels.append(query[1])
            json = self.get_json(query, flag)
            if 'album' not in json and 'track' not in json:
                listeners.append(0)
                playcounts.append(0)
                track_count.append(0)
                duration.append(0)
            elif 'track' not in json:
                listeners.append(int(json['album']['listeners']))
                playcounts.append(int(json['album']['playcount']))
                track_count.append(len(json['album']['tracks']['track']))
            elif 'album' not in json:
                listeners.append(int(json['track']['listeners']))
                playcounts.append(int(json['track']['playcount']))
                duration.append(len(json['track']['duration']))
        if flag == 'TA':
            y_values.append(listeners)
            y_values.append(playcounts)
            y_values.append(track_count)
        elif flag == 'TT':
            y_values.append(listeners)
            y_values.append(playcounts)
            y_values.append(duration)
        return x_labels, y_values

    def barchart(self, artist, X, Y, flag):

        fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(10,10))
        plt.setp((ax1, ax2, ax3), xticklabels=X)
        rects1 = ax1.bar(X, Y[0])
        rects2 = ax2.bar(X, Y[1])
        rects3 = ax3.bar(X, Y[2])
        if flag == 'TA':
            ax1.set_title('Listeners')
            ax2.set_title('Playcounts')
            ax3.set_title('Track Counts')
        elif flag == 'TT':
            ax1.set_title('Listeners')
            ax2.set_title('Playcounts')
            ax3.set_title('Track Duration')
        ax1.tick_params(labelrotation=15)
        ax2.tick_params(labelrotation=15)
        ax3.tick_params(labelrotation=15)

        fig.tight_layout()
        plt.savefig('images/top_5.png')

    def get_json(self, query, flag):
        if 'TAG' in flag:
            tag = query
        elif 'GEO' in flag:
            country = query
        else:
            artist_name = query[0]
            artist_item = query[1]
        if flag == 'TA':
            url = 'http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={}&artist={}&album={}&format=json'.format(API_KEY, artist_name, artist_item)
        elif flag == 'TT':
            url = 'http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={}&artist={}&track={}&format=json'.format(API_KEY, artist_name, artist_item)
        elif 'TAG' in flag:
            if '1' in flag:
                url = 'http://ws.audioscrobbler.com/2.0/?method=tag.gettopalbums&tag={}&api_key={}&limit=10&format=json'.format(tag, API_KEY)
            elif '2' in flag:
                url = 'http://ws.audioscrobbler.com/2.0/?method=tag.gettopartists&tag={}&api_key={}&limit=10&format=json'.format(tag, API_KEY)
            elif '3' in flag:
                url = 'http://ws.audioscrobbler.com/2.0/?method=tag.gettoptracks&tag={}&api_key={}&limit=10&format=json'.format(tag, API_KEY)
        elif 'GEO' in flag:
            if '1' in flag:
                url = 'http://ws.audioscrobbler.com/2.0/?method=geo.gettopartists&country={}&api_key={}&limit=10&format=json'.format(country, API_KEY)
            elif '2' in flag:
                url = 'http://ws.audioscrobbler.com/2.0/?method=geo.gettoptracks&country={}&api_key={}&limit=10&format=json'.format(country, API_KEY)
        album_metadata = requests.get(url)
        album_json = album_metadata.json()

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