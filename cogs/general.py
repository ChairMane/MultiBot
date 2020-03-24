import discord
from discord.ext import commands


class General:
    def __init__(self, bot=None):
        self.bot = bot

    @commands.command(pass_context=True)
    async def help(self, ctx, arg=None):
        coms = set(self.bot.commands.keys())

        if arg in coms:
            wt = self.bot.get_command(arg).help

        if arg == None:

            embed = discord.Embed(title='Help', description='Commands', colour=discord.Colour.purple())

            embed.set_author(name="I'm Dumb AF!", url="https://github.com/ChairMane/MultiBot",
                             icon_url="https://avatars1.githubusercontent.com/u/19229124?s=400&u=d98831706311ca2f43bbf12187119ff62d80bd18&v=4")

            embed.add_field(name='similar-to', value='Returns similar artists', inline=True)
            embed.add_field(name='info-on', value='Returns information on given artist', inline=True)
            embed.add_field(name='top-artists', value='Returns top artists from Last.fm', inline=True)
            embed.add_field(name='top-tracks', value='Returns top tracks from Last.fm', inline=True)
            embed.add_field(name='top-tags', value='Returns top tags from Last.fm', inline=True)
            embed.add_field(name='top-albums-for-tag', value='Returns top albums for given tag', inline=True)
            embed.add_field(name='top-tracks-for-tag', value='Returns top tracks for given tag', inline=True)
            embed.add_field(name='top-artists-for-tag', value='Returns top artists for given tag', inline=True)
            embed.add_field(name='top-artists-for-country', value='Returns top artists for given country', inline=True)
            embed.add_field(name='top-tracks-for-country', value='Returns top tracks for given country', inline=True)
            embed.add_field(name='top-albums-for', value='Returns top albums for given artist', inline=True)
            embed.add_field(name='top-tracks-for', value='Returns top tracks for given artist', inline=True)


        else:
            embed = discord.Embed(title=arg, description=wt, colour=discord.Colour.purple())
            embed.set_author(name="I'm Dumb AF!", url="https://github.com/ChairMane/MultiBot",
                             icon_url="https://avatars1.githubusercontent.com/u/19229124?s=400&u=d98831706311ca2f43bbf12187119ff62d80bd18&v=4")

        await self.bot.say(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
