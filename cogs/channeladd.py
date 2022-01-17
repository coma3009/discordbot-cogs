from os import name
import discord
from discord import channel
from discord import message
from discord import embeds
from discord.ext import commands, tasks
from discord_components import Button, ButtonStyle, SelectOption, Select
import discord_components
import os
import psutil
import random
import asyncio
import datetime
import time


from discord.ext.commands.core import Command, command


from discord.ext.commands.core import Command, command

ticket_guild_id = 856829534926143538
category_id = 890151936819617822
class channeladd(commands.Cog, name = "역할 및 채널생성명령어", description = "채널생성명령어 Cog입니다."):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='음성채널')
    async def channel_add(self, ctx, args: str):
        ticket_guild = self.bot.get_guild(ticket_guild_id)
        open_ticket_category = ticket_guild.get_channel(category_id)
        channel = await open_ticket_category.create_voice_channel(args)
        await ctx.send(f"{channel.mention} 음성채널을 생성했어요!")


    @commands.command(name= '채팅채널')
    async def text_channel_add(self, ctx, args: str):
        ticket_guild = self.bot.get_guild(ticket_guild_id)
        open_ticket_category = ticket_guild.get_channel(category_id)
        channel = await open_ticket_category.create_text_channel(args)
        await ctx.send(f"{channel.mention} 채팅채널을 생성했어요!")
    @commands.command(name = "채널생성", aliases = ["chadd"])
    async def allchanneladd(self, ctx):
        msg = await ctx.send(embed = discord.Embed(title = "채널 타입", description = "어떤 채널로 채널을 생성하시겠습니까"), components = [
            [
                Button(label = "텍스트채널", emoji = "💬", style = ButtonStyle.gray, id = "textchannel"),
                Button(label = "스테이지 채널", emoji = "🎤", style = ButtonStyle.gray, id = "stagechannel"),
                Button(label = "음성 채널", emoji = "🔊", style = ButtonStyle.gray, id = "voicechannel"),
                Button(label = "취소", emoji = "❌", style = ButtonStyle.red, id = "cancel"),
            ]
        ])

        def check(res):
            return res.user == ctx.author and res.channel == ctx.channel
        
        try:
            res = await self.bot.wait_for("button_click", check = check, timeout = 60)
            if res.component.id == "cancel":
                return await ctx.send(embed = discord.Embed(title = "채널 생성 취소", description = "채널 생성을 취소하였습니다."))
        except asyncio.TimeoutError:
            return await ctx.send(embed = discord.Embed(title = "채널 생성 취소", description = "채널 생성을 취소하였습니다."))
        ticket_guild = self.bot.get_guild(ticket_guild_id)
        category=ticket_guild.get_channel(category_id)
	
        if res.component.id == "textchannel":
            channel = await category.create_text_channel(name= f"{ctx.author.name} 채널")
        elif res.component.id == "stagechannel":
            channel = await category.create_stage_channel(name= f"{ctx.author.name} 채널")

#create_stage_channel
        elif res.component.id == "voicechannel":
            channel = await category.create_voice_channel(name= f" {ctx.author.name} 채널")
        await msg.edit(embed = discord.Embed(title = "생성 완료!", description = f"채널을 생성하였습니다!\n {channel.mention}", colour = discord.Colour.green()))
        await res.respond















def setup(bot):
    bot.add_cog(channeladd(bot))