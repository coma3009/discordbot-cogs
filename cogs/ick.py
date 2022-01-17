from os import name
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


from discord.ext.commands.core import Command, command

class ick(commands.Cog, name = "익명 채팅", description = "익명채팅명령어입니다"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 887301892194045982:
            await message.delete()
            channel = self.bot.get_channel(887301920480428114)
            embed = discord.Embed(
                title= '익명채팅',
                description=f"익명 : {message.content}"
            )
            channel2 = self.bot.get_channel(890599700917538877)
            embed2 = discord.Embed(
                title= '익명채팅-관리자용',
                description=f"{message.author} : {message.content}"
            )
            await channel2.send(embed=embed2)
            await channel.send(embed=embed)

        if message.channel.id == 890603550672060426:
            await message.delete()
            channel = self.bot.get_channel(887301920480428114)
            channel2 = self.bot.get_channel(890599700917538877)
            embed = discord.Embed(
                title= '익명채팅',
                description=f"관리자 : {message.content}"
            )
            await channel.send(embed=embed)
            await channel2.send(embed=embed)

        # 이렇게 하면 됨 
        # 대상 채널에서는 접두사 없이 됨


def setup(bot):
    bot.add_cog(ick(bot)) # 그건 니가 알아서 바꾸고 난 줌 하러 감