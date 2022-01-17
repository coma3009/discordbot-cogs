from turtle import color
import discord
from discord.embeds import Embed
from discord.ext import commands
import asyncio
from PycordPaginator import Paginator
import os
import random
from discord.ext.menus import Button
from discord_components import component
import discordSuperUtils
import pytz
import aiosqlite
import datetime
import traceback
class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name = "서버리스트",
        aliases = ['serverlist']
    )
    @commands.is_owner()
    async def owner_serverlist(self, ctx):
        with open("guilds.txt", 'w', -1, "utf-8") as a: # 'guilds.txt' 파일을 생성하고 그것을 'a' 로 지정한다
            a.write(str(self.bot.guilds)) # 'a' 에 봇이 접속한 서버들을 나열한다 
        file1 = discord.File("guilds.txt") # 'file1' 을 'guilds.txt' 로 정의한다
        await ctx.author.send(file=file1) # 명령어를 수행한 멤버의 DM으로 'file1' 을 발송한다
        os.remove("guilds.txt")
        await ctx.reply(f"DM으로 서버 리스트 발송을 완료했습니다!")

    @commands.command(
        name="Check-Error",
        aliases=["elog"],
        usage="elog [code]",
        help=" 코인의 에러 로그를 확인할수 있습니다.",
        hidden=True,
    )
    @commands.is_owner()
    async def owner_elog(self, ctx, code):
        try:
            f = open(f"data/error_logs/{code}", "r", encoding="utf8")
            data = f.read()
            await ctx.send(f"```py\n{data}\n```")
            f.close()
        except:
            await ctx.send(
                content=code, file=discord.File(fp=data, filename=f"{code}.txt")
            )
    @commands.command(
        name="공지",
        aliases=["📢ㅣ공지","notice","🚨ㅣ𝐀𝐧𝐧𝐨𝐮𝐧𝐜𝐞𝐦𝐞𝐧𝐭", "announce"], #공지
        usage="[공지|notice|announce][📌│공지사항] [📢ㅣ공지][🚨ㅣ𝐀𝐧𝐧𝐨𝐮𝐧𝐜𝐞𝐦𝐞𝐧𝐭] [colour] [content]", #공지 [colour code] [content]
        help=f"봇이 들어가 있는 서버에 공지를 전송합니다.",
    )
    @commands.is_owner()
    
    # @commands.dm_only() # DM에서만
    # @commands.guild_only() # 길드에서만    

    async def notice_cmd(self, ctx, *, content: str = None):
        # if colour in ["빨간색", "red", "0xff0000"]:
        #     colour = 0xFF0000
        # elif colour in ["주황색", "orange", "0xffa500"]:
        #     colour = 0xFFA500
        # elif colour in ["노랑색", "yellow", "0x008000"]:
        #     colour = 0xFFFF33
        # elif colour in ["초록색", "녹색", "green", "0x0000ff"]:
        #     colour = 0x008000
        # elif colour in ["파란색", "파랑색", "blue", "0x0000ff"]:
        #     colour = 0x0000FF
        # elif colour in ["보라색", "purple", "0x7f00ff"]:
        #     colour = 0x7F00FF
        # elif colour in "0x" and len(colour) == 8:
        #     colour = colour
        # else:
        colour = 0xFFFF33

        embed = discord.Embed(
            title=f"{self.bot.user.name} 공지",
            description=f" \n{content}\n[{self.bot.user.name} 공식서버](https://discord.gg/zQKzwyTQQU)\n[{self.bot.user.name} 초대링크](https://koreanbots.dev/bots/872714206246469662)\n[웹사이트 리메이크 중]\n-------------------------\n공지는 채널이름에 공지가 포함된 곳에 공지를 보냅니다",
            colour=colour,
            timestamp=ctx.message.created_at,
        )
        await ctx.send(embed=embed)
        embed.set_footer(text="특정 채널에 받고싶다면 '하린아 설정'으로 설정하세요! 권한 확인 필수!")
        msg = await ctx.reply("발송중...")
        guilds = self.bot.guilds
        ok = []
        ok_guild = []
        success = 0
        failed = 0
        for guild in guilds:
            channels = guild.text_channels
            for channel in channels:
                if guild.id in [653083797763522580, 786470326732587008]:
                    break
                if (
                    channel.topic is not None
                    and str(channel.topic).find("-HOnNt") != -1
                ):
                    ok.append(channel.id)
                    ok_guild.append(guild.id)
                    break

        for guild in guilds:
            channels = guild.text_channels
            for _channel in channels:
                if guild.id in ok_guild:
                    break
                if guild.id in [653083797763522580, 786470326732587008]:
                    break
                random_channel = random.choices(channels)
                ok.append(random_channel[0].id)
                break
        for i in ok:
            channel = self.bot.get_channel(i)
            try:
                await channel.send(embed=embed)
                success += 1
            except discord.Forbidden:
                failed += 1
        await msg.edit("발송완료!\n성공: `{ok}`\n실패: `{no}`".format(ok=success, no=failed))

        count = 0
        channel = []
        for i in self.bot.guilds:
            for j in i.text_channels:
                if "공지" in j.name or "announcement" in j.name or "notice" in j.name or "𝐀𝐧𝐧𝐨𝐮𝐧𝐜𝐞𝐦𝐞𝐧𝐭" in j.name or "Announcement" in j.name:
                # if ('공지', 'announcement', 'notice', '𝐀𝐧𝐧𝐨𝐮𝐧𝐜𝐞𝐦𝐞𝐧𝐭','Announcement') in j.name:
                    try:
                        await j.send(embed=embed)
                        count += 1
                        await ctx.author.send(f"{i.name}\n{j.name}")
                    except:
                        for c in i.text_channels:
                            if ('봇' in c.name):
                                try:
                                    await c.send(embed=embed)
                                    count += 1
                                    await ctx.author.send(f"{i.name}\n{c.name}")
                                except Exception as a:
                                    await ctx.send(f'{i.name} 서버의 {j.name} 와 {c.name} 채널에 공지를 보내기 실패했습니다.')
                                    await ctx.send(a)
                                break
                    else:
                        break
        await ctx.send(f"{count} 개의 채널에 공지를 전송했습니다")

        
        # for i in self.bot.guilds:
        #     for j in i.text_channels:
        #         if ("코인" in j.topic):
        #             try:
        #                 await j.send(embed=embed)
        #                 count += 1
        #                 channel.append(f"{i.name} - {j.name}")
        #             except:
        #                 for k in i.text_channels:
        #                     if ("봇" in k.name):
        #                         try:
        #                             await k.send(embed=embed)
        #                             count += 1
        #                             channel.append(f"{i.name} - {j.name}")
        #                         except:
        #                             for l in i.text_channels:
        #                                 if ("공지" in l.name):
        #                                     try:
        #                                         await i.send(embed = embed)
        #                                         count += 1
        #                                         channel.append(f"{i.name} - {l.name}")
        #                                     except:
        #                                         channel.append(f"{i.name} 전송 실패")
        #                                     break                                            
        #             else:
        #                 break
        # await ctx.send(f"{count}개의 길드에 공지를 전송했습니다!")

    # @commands.command(
    #     name = "경고",
    #     aliases = ["warning"]
    # )
    # @commands.has_permissions(administrator = True)
    # async def warning_cmd(self, ctx, user: discord.User, *, reason: str = None):
    #     if not user:
    #         return await ctx.send(f"{ctx.author.mention}, 유저 맨션좀 하지?")
    #     if ctx.guild.get_member(user.id).top_role >= ctx.author.top_role:
    #         return await ctx.send(f"니보다 높은 역할 소유자는 경고 못함 ㅅㄱ")
    #     if user.bot:
    #         return await ctx.send(f"봇한테 경고 먹여서 어디다가 쓸껀데")

    
def setup(bot):
    bot.add_cog(Owner(bot))