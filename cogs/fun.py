import discord
from discord.ext import commands
import random
import os
import logging
from cogs.functions import cracker_id, creator, magnet_id, enanasPath


class Fun(commands.Cog):
    """Cosas random y divertidas"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def penis(self, context, *, user: discord.Member = None):
        """Buena tula

        Genera un pene de tamaño aleatorio.
        Uso:
        fur penis            --> Tu tula
        fur penis @<usuario> --> La tula de @<usuario>
        """

        num = random.randint(1, 15)
        output = "El pene de {}\n"
        if user == None:
            usuario = str(context.author)[:-5]
        else:
            usuario = str(user)[:-5]

        output += "8"
        for x in range(num):
            output += "="
        output += "D"
        await context.channel.send(output.format(usuario))

    @commands.command()
    async def communism(self, context, *, user: discord.Member = None):
        """Serás un comunista bolivariano que apoya al Coletas?"""

        num = random.randint(0, 100)
        output = "{} es {}% comunista"
        if user == None:
            usuario = str(context.author)[:-5]
        else:
            usuario = str(user)[:-5]
        await context.channel.send(output.format(usuario, num))

    @commands.command()
    async def gay(self, context, *, user: discord.Member = None):
        """Maricon el ultimo"""

        num = random.randint(0, 100)
        output = "{} es {}% gay"
        if user == None:
            if context.author.id == cracker_id:
                num = 100
                usuario = "Cracker"
            elif context.author.id == creator:
                num = 100
                usuario = "Teko"
            elif context.author.id == magnet_id:
                num = 100
                usuario = "Magnet"
            else:
                usuario = str(context.author)[:-5]
        else:
            if user.id == cracker_id:
                num = 100
                usuario = "Cracker"
            elif user.id == magnet_id:
                num = 100
                usuario = "Magnet"
            elif user.id == creator:
                num = 100
                usuario = "Teko"
            else:
                usuario = str(user)[:-5]

        await context.channel.send(output.format(usuario, num))

    @commands.command()
    async def str8(self, context, *, user: discord.Member = None):
        """Super str8 el ultimo"""

        num = random.randint(0, 100)
        output = "{} es {}% hetero"
        if user == None:
            if context.author.id == cracker_id:
                num = 0
                usuario = "Cracker"
            elif context.author.id == creator:
                num = 0
                usuario = "Teko"
            elif context.author.id == magnet_id:
                num = 0
                usuario = "Magnet"
            else:
                usuario = str(context.author)[:-5]
        else:
            if user.id == cracker_id:
                num = 0
                usuario = "Cracker"
            elif user.id == magnet_id:
                num = 0
                usuario = "Magnet"
            elif user.id == creator:
                num = 0
                usuario = "Teko"
            else:
                usuario = str(user)[:-5]

        await context.channel.send(output.format(usuario, num))

    @commands.command()
    async def capitalist(self, context, *, user: discord.Member = None):
        """Serás capitalista y te convertirás en el nuevo lobo de Wall Street?"""

        num = random.randint(0, 100)
        output = "{} es {}% capitalista"
        if user == None:
            usuario = str(context.author)[:-5]
        else:
            usuario = str(user)[:-5]
        await context.channel.send(output.format(usuario, num))

    @commands.command()
    async def enana(self, context, arg: str = None, *, user: discord.Member = None):
        """Elije una enana o consigue una aleatoria de forma totalmente gratuita

        Uso:
            fur enana           ---> Enana aleatoria
            fur enana <palabra> ---> Enana que contega palabra
        """

        if arg == None:
            output = random.choice(os.listdir(enanasPath))
            await context.channel.send(file=discord.File(enanasPath + output))

        else:
            for filenames in os.listdir(enanasPath):
                if arg.lower() in filenames.lower():
                    output = filenames
            await context.channel.send(file=discord.File(enanasPath + output))

    @commands.command()
    async def enanalist(self, context):

        """Lista todas las enanas existentes"""
        output = os.listdir(enanasPath)
        output[:] = [s.replace(".png", "") for s in output]
        output[:] = [s.replace("'", "") for s in output]
        await context.channel.send(output)


def setup(bot):
    bot.add_cog(Fun(bot))
