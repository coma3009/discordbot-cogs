import imp
from os import name
import discord
from discord import message
from discord import embeds
from discord import mentions
from discord import channel
from discord.ext import commands
import aiosqlite
from discord_components import Button, ButtonStyle, SelectOption, Select, component
import discord_components
import discordSuperUtils
from PycordPaginator import Paginator
import os
import psutil
import random
import asyncio
import datetime
import time

from utils.json import loadjson, savejson


from discord.ext.commands.core import Command, command
#욕설




class management(commands.Cog, name = "서버 관리 명령어", description = "서버 관리 명령어 Cog입니다."):
    def __init__(self, bot):
        self.bot = bot
        self.InfractionManager = discordSuperUtils.InfractionManager(bot)
        self.BanManager = discordSuperUtils.BanManager(bot)
        self.KickManager = discordSuperUtils.KickManager(bot)
        self.MuteManager = discordSuperUtils.MuteManager(bot)
        self.InfractionManager.add_punishments(
            [
                discordSuperUtils.Punishment(self.KickManager, punish_after=4),
                discordSuperUtils.Punishment(self.MuteManager, punish_after=2),
                discordSuperUtils.Punishment(self.BanManager, punish_after=5),
            ]
        )
        super().__init__()
    async def cog_before_invoke(self, ctx: commands.Context):
        print(ctx.command)
        if ctx.command.name != '메일':
            database = await aiosqlite.connect("db/db.sqlite")
            cur = await database.execute(
                'SELECT * FROM uncheck WHERE user_id = ?', (ctx.author.id,)
            )

            if await cur.fetchone() is None:
                cur = await database.execute("SELECT * FROM mail")
                mails = await cur.fetchall()
                check = sum(1 for _ in mails)
                mal = discord.Embed(
                    title=f'📫라이젠 메일함 | {check}개 수신됨',
                    description="아직 읽지 않은 메일이 있어요.'`>메일`'로 확인하세요.\n주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                    colour=ctx.author.colour,
                )

                return await ctx.send(embed=mal)
            cur = await database.execute('SELECT * FROM mail')
            mails = await cur.fetchall()
            check = sum(1 for _ in mails)
            # noinspection DuplicatedCode
            cur = await database.execute("SELECT * FROM uncheck WHERE user_id = ?", (ctx.author.id,))
            # noinspection DuplicatedCode
            check2 = await cur.fetchone()
            if str(check) != str(check2[1]):
                mal = discord.Embed(
                    title=f'📫라이젠 메일함 | {int(check) - int(check2[1])}개 수신됨',
                    description="아직 읽지 않은 메일이 있어요.'`>메일`'로 확인하세요.\n주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                    colour=ctx.author.colour,
                )

                await ctx.send(embed=mal)
    @commands.command(name= '킥', aliases=['추방','kick'])
    @commands.has_permissions(administrator=True)
    async def mod_kick(self, ctx, member: discord.Member, *, reason: str = None):
        embed = discord.Embed(
            title = f"추방",
            description = f"유저를 킥했습니다.\n\n대상: {member}\n관리자: {ctx.author}\n사유: {reason}",
            colour = discord.Colour.dark_orange(),
            timestamp = ctx.message.created_at
        )
        await ctx.send(embed=embed)#해야할거 벤 블랙리스트
        await member.send(embed = embed)
        await ctx.guild.kick(member, reason = reason)
    
    @commands.command(name="밴")
    @commands.has_permissions(administrator=True)
    async def ban(
            self,
            ctx,
            member: discord.Member,
            time_of_ban: discordSuperUtils.TimeConvertor,
            *,
            reason: str = "No reason specified.",
    ):
        embed = discord.Embed(
            title = f"밴",
            description = f"유저를 밴했습니다.\n\n대상: {member}\n관리자: {ctx.author}\n사유: {reason}",
            colour = discord.Colour.dark_orange(),
            timestamp = ctx.message.created_at
        )
        await ctx.send(f"{member}님이 밴되셨어요. 사유: {reason}", embed=embed)
        await member.send(embed=embed)
        await self.BanManager.ban(member, reason, time_of_ban)

    @commands.command(name="언밴")
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, user: discord.User):
        if await self.BanManager.unban(user, guild=ctx.guild):
            await ctx.send(f"{user}님은 언밴되셨어요.")
        else:
            await ctx.send(f"{user}은 밴되어있지않아요.")
    # @commands.command(name="슬로우모드")
    # @commands.has_permissions(manage_channels=True)
    # async def slowmode(ctx, time:int=None):
    #     if time == None:
    #         await ctx.send("\❌ 슬로우모드를 몇초로 설정할지 보내주세요.")
    #         return
    #     elif time == 0:
    #         await ctx.send("\✅슬로우모드를 껐어요.")
    #         await ctx.channel.edit(slowmode_delay=0)
    #         return
    #     elif time > 21600:
    #         await ctx.send("\❌ 슬로우모드를 6시간 이상 설정할수 없어요.")
    #         return
    #     else:
    #         await ctx.channel.edit(slowmode_delay=time)
    #         await ctx.send(f"\✅ 성공적으로 슬로우모드를 {time}초로 설정했어요.")

    
    
    # Server Stats
    @commands.Cog.listener("on_ready")
    async def mn_on_ready(self):
        database = discordSuperUtils.DatabaseManager.connect(
            await aiosqlite.connect("db/db.sqlite")
        )
        await self.InfractionManager.connect_to_database(database, ["infractions"])
        await self.BanManager.connect_to_database(database, ["bans"])
        await self.MuteManager.connect_to_database(database, ["mutes"])

    @staticmethod
    async def make_infraction_embed(member_infractions, member) -> list:
        return discordSuperUtils.generate_embeds(
            [
                f"**사유: **{await infraction.reason()}\n"
                f"**처리ID: **{infraction.id}\n"
                f"**처벌일자: **{await infraction.datetime()}"
                for infraction in member_infractions
            ],
            title=f"{member}의 처벌목록",
            fields=25,
            description=f"{member}의 처벌목록"
        )

    @commands.command(name="뮤트")
    @commands.has_permissions(administrator=True)
    async def mute(
            self,
            ctx,
            member: discord.Member,
            time_of_mute: discordSuperUtils.TimeConvertor,
            *,
            reason: str = "No reason specified.",
    ):
        try:
            await self.MuteManager.mute(member, reason, time_of_mute)
        except discordSuperUtils.AlreadyMuted:
            await ctx.send(f"{member}님은 이미 뮤트되어있어요.")
        else:
            await ctx.send(f"{member}님은 뮤트되었어요. 뮤트 사유: {reason}")

    @commands.command(name="언뮤트")
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member: discord.Member):
        if await self.MuteManager.unmute(member):
            await ctx.send(f"{member.mention}님이 언뮤트되었어요.")
        else:
            await ctx.send(f"{member.mention}은 뮤트되어있지 않아요!")

    @commands.group(name="처벌", invoke_without_command=True)
    async def infractions(self, ctx, member: discord.Member):
        member_infractions = await self.InfractionManager.get_infractions(member)
        embeds = await self.make_infraction_embed(member_infractions, member)
        print(embeds)
        e = Paginator(
            client=self.bot.components_manager,
            embeds=embeds,
            channel=ctx.channel,
            only=ctx.author,
            ctx=ctx)
        await e.start()

    @infractions.command(name="추가")
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, member: discord.Member, *,reason: str = "No reason specified."):
        infraction = await self.InfractionManager.warn(ctx, member, reason)

        embed = discord.Embed(title=f"{member} has been warned.", color=0x00FF00)

        embed.add_field(name="사유", value=await infraction.reason(), inline=False)
        embed.add_field(name="처벌 ID", value=infraction.id, inline=False)
        embed.add_field(
            name="처벌시간", value=str(await infraction.datetime()), inline=False
        )
        # Incase you don't like the Date of Infraction format you can change it using datetime.strftime

        channel=self.bot.get_channel(931498938165522512)
        await ctx.send(embed=embed)
        await channel.send(embed=embed)

    @infractions.command(name="조회")
    async def get(self, ctx, member: discord.Member, infraction_id: str):
        infractions_found = await self.InfractionManager.get_infractions(
            member, infraction_id=infraction_id
        )

        if not infractions_found:
            await ctx.send(
                f"다음 처리ID `{infraction_id}`를 가진 데이터를 찾을 수 없어요. "
            )
            return

        infraction = infractions_found[0]

        embed = discord.Embed(
            title=f"Infraction found on {member}'s account!", color=0x00FF00
        )

        embed.add_field(name="사유", value=await infraction.reason(), inline=False)
        embed.add_field(name="처벌 ID", value=infraction.id, inline=False)
        embed.add_field(
            name="처벌시간", value=str(await infraction.datetime()), inline=False
        )
        # Incase you don't like the Date of Infraction format you can change it using datetime.strftime
        channel=self.bot.get_channel(931498938165522512)
        await ctx.send(embed=embed)
        await channel.send(embed=embed)

    @infractions.command(name="제거", aliases=["삭제", "취소"])
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, member: discord.Member, infraction_id: str):
        infractions_found = await self.InfractionManager.get_infractions(
            member, infraction_id=infraction_id
        )

        if not infractions_found:
            await ctx.send(
                f"다음 처리ID `{infraction_id}`를 가진 데이터를 찾을 수 없어요. "
            )
            return

        removed_infraction = await infractions_found[0].delete()

        embed = discord.Embed(
            title=f"{member}로부터 처벌이 최소되었습니다!", color=0x00FF00
        )

        embed.add_field(name="사유", value=removed_infraction.reason, inline=False)
        embed.add_field(
            name="처벌 ID", value=removed_infraction.id, inline=False
        )
        embed.add_field(
            name="처벌 일시",
            value=str(removed_infraction.date_of_infraction),
            inline=False,
        )

        channel=self.bot.get_channel(931498938165522512)
        await ctx.send(embed=embed)
        await channel.send(embed=embed)

    

    # 코파일럿 최고 흐헿 ?
    # 맞다 오기전까지 저 입퇴장에 카드넣는거 시도 했는데 안됨 해줄수 있음? 
    # # 그건 나도 모르겄다 내가 해본적이 없어서? 할수 있다는 듯이 말하더니.... # 저 레벨 카드땜에 해보적은 있는데 성공의 여부는 알수 없 일단 해보자 
    # #ㄳ 레벨기능을 빼고 텍스트를 이름 아래 코인공식서버에 오신것을 환영합니다 넣으면 된다아님?  ㄱㄷ

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     with open("data/욕설.txt") as f:#오늘 이거 패치하고 한디리에 올리게 
    #         mydict = f.read()
    #     print(mydict)
    #     List = []
    #     List.append(mydict)
        # for i in List:
        #     if message.content in i:
        #         await message.reply(embed= discord.Embed)
        #         await message.delete()
        #     else:
    
    
    #             pass

    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.channel.topic).find("-HOnBdWld") != -1:      
            with open("욕설_리스트.txt", "r", encoding="utf-8") as f:
                data = f.read()
            lists = data.splitlines()
            em=discord.Embed(title=f"⚠️ 욕설감지", colour=discord.Colour.red())
            # for i in data:
            em.add_field(name='사용한 욕설 ⚠️', value=f"|| {message.content} ||")
            em.add_field(name='보낸 사람', value=str(message.author))
            if message.content in lists:
                await message.reply(embed=em)
                await message.delete()
            else:
                pass
        
    @commands.command(name = "청소", aliases = ["ㅊ"])
    @commands.has_permissions(administrator = True)
    async def clean(self, ctx, limit: int = None):
        if not type(limit) == int:
            return await ctx.reply("삭제할 수의 타입은 INT 형식이어야 합니다.")
        await ctx.channel.purge(limit = limit + 1)
        await ctx.send(f"{limit}개의 메시지를 삭제하였습니다.", delete_after = 5)
def setup(bot):
    bot.add_cog(management(bot))
