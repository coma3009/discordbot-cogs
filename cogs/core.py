from os import name
from turtle import title
import discord
from discord import message
from discord import embeds
from discord.ext import commands

import os
import psutil
import random
import asyncio
import datetime
import time

import aiosqlite
from discord.ext.commands.core import Command, command


class Core(commands.Cog, name = "봇 기본 명령어", description = "봇 기본 명령어 Cog입니다."):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def hellothisisverification(self, ctx):
        await ctx.send("Coma#3009")
    @commands.command(name="개발자")
    async def mod(self, ctx):
        embed=discord.Embed(title="개발자",color=0x0000ff)
        embed.add_field(name="메인개발자", value="Coma#3009")
        await ctx.send(embed=embed)
    @commands.command(
        name = "핑"
    )
    async def ping(self, ctx):
        await ctx.send(embed = discord.Embed(title = "**Pong!**", description = f":ping_pong: {round(self.bot.latency) * 1000}ms", color= 0x0000ff))

def setup(bot):
    bot.add_cog(Core(bot))
