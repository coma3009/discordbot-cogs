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
    @commands.command()
    async def hellothisisverification(self, ctx):
        await ctx.send("Coma#3009")
    @commands.command(name="개발자")
    async def mod(self, ctx):
        embed=discord.Embed(title="개발자",color=0x0000ff)
        embed.add_field(name="메인개발자", value="Coma#3009")
        embed.add_field(name="보조개발자", value="근태#5863")
        await ctx.send(embed=embed)
    @commands.command(name="출처")
    async def musicch(self, ctx):
        embed=discord.Embed(title="출처",color=0x0000ff)
        embed.add_field(name="출처", value="해당 뮤직기능은 해피트리봇코드를 사용했습니다!")
        embed.add_field(name="깃헙", value="[하린봇](https://github.com/spacedev-official/harin)")
        await ctx.send(embed=embed)
    @commands.command(
        name = "핑"
    )
    async def ping(self, ctx):
        await ctx.send(embed = discord.Embed(title = "**Pong!**", description = f":ping_pong: {round(self.bot.latency) * 1000}ms", color= 0x0000ff))

    @commands.command(
        name= "서포트",
        aliases= ['ㅅㅍㅌ','서포트서버']
    )
    async def suport(self, ctx):
        embed = discord.Embed(
            title=f"{self.bot.user.name} 서포트서버",
            description=f"[{self.bot.user.name} 공식서버](https://discord.gg/d7zEFsbMVN)\n",
            colour=discord.Colour.random(),
            timestamp=ctx.message.created_at,
        )
        await ctx.send(embed = embed)
#     @commands.command(
#         name= "문의",
#         aliases= ['ㅁㅇ']
#     )
#     async def question(self, ctx):
#         embed = discord.Embed(colour=discord.Colour.blue(), timestamp=ctx.message.created_at)
#         embed.add_field(name='디스코드관리자', value=ctx.author.created_at)
#         embed.add_field(name='문의내용', value=message.content, inline=False)
#         embed.set_footer(text=f'문의 <@{message.author.id}> 문의완료')
#         await self.bot.get_channel(850543503988883476).send(f"`{message.author.name}({message.author.id})`", embed=embed)
    @commands.command(
        name="서버수",
    )
    async def server(self, ctx):
        embed = discord.Embed(
            title=f"서버수",
            description=f"코인봇은 {len(self.bot.guilds)}개의 서버에 있습니다",
            colour=discord.Colour.blue(),
        )
        await ctx.send(embed = embed)
    @commands.command(
        name="작동확인"
    )
    async def on_chack(self, ctx):
        embed = discord.Embed(
            title=f"작동확인",
            description=f"🟢정상 작동중입니다.",
            colour=discord.Colour.blue(),
        )
        await ctx.send(embed = embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self} has been loaded') 
        global startTime 
        startTime = time.time()

    @commands.command(name='업타임', aliases=['Uptime'])
    async def _uptime(self,ctx):
        now = datetime.datetime.now()
        server_uptime = now - datetime.datetime.fromtimestamp(psutil.boot_time())
        python_uptime = now - datetime.datetime.fromtimestamp(
        psutil.Process(os.getpid()).create_time())
        await ctx.send(f"**Server Uptime** {server_uptime}\n" + f"**Bot Uptime** {python_uptime}")
        
    @commands.command(name="메일", help="`>메일 (전체)`로 메일을 확인합니다.")
    async def read_mail(self, ctx, mode=None):
        if mode is None:
            dictcommand = await self.read_email_from_db(ctx=ctx)
            database = dictcommand["database"]
            contents = dictcommand["contents"]
            cur = dictcommand["cur"]
            uncheck_cur = dictcommand["uncheck_cur"]
            timess = dictcommand["timess"]
            pages = dictcommand["pages"]
            check2 = await cur.fetchone()
            uncheck_cur_fetchone = await uncheck_cur.fetchone()
            if uncheck_cur_fetchone is None:
                await database.execute("INSERT INTO uncheck VALUES (?, ?)", (ctx.author.id, str(pages)))
                await database.commit()
                mal = discord.Embed(title=f"📫라이젠 메일함 | {str(pages)}개 수신됨",
                                    description="주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                                    colour=ctx.author.colour)
                cur_page = 1
            else:
                if str(pages) == str(uncheck_cur_fetchone[1]):
                    mal = discord.Embed(title=f"📫라이젠 메일함 | 수신된 메일이 없어요.",
                                        description="주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                                        colour=ctx.author.colour)
                    mal.add_field(name="📭빈 메일함", value="✅모든 메일을 읽으셨어요. 전체메일을 보고싶으시면 `>메일 전체`를 입력하세요.")
                    return await ctx.send(embed=mal)
                await database.execute("UPDATE uncheck SET check_s = ? WHERE user_id = ?",
                                       (str(pages), ctx.author.id))
                await database.commit()
                mal = discord.Embed(title=f"📫라이젠 메일함 | {pages - int(uncheck_cur_fetchone[1])}개 수신됨",
                                    description="주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                                    colour=ctx.author.colour)
                cur_page = int(uncheck_cur_fetchone[1])
            # noinspection DuplicatedCode
            mal.add_field(name=f"{pages}중 {cur_page}번째 메일({timess[contents[cur_page - 1]]}작성)",
                          value=contents[cur_page - 1])
            message = await ctx.send(embed=mal)
            # getting the message object for editing and reacting

            await message.add_reaction("◀️")
            await message.add_reaction("▶️")

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"] and reaction.message.id == message.id

            while True:
                try:
                    reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                    # waiting for a reaction to be added - times out after x seconds, 60 in this
                    # example

                    if str(reaction.emoji) == "▶️" and cur_page != pages:
                        if check2 is None:
                            cur_page += 1
                            mal = discord.Embed(title=f"📫라이젠 메일함 | {str(pages)}개 수신됨",
                                                description="주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                                                colour=ctx.author.colour)
                            mal.add_field(name=f"{pages}중 {cur_page}번째 메일", value=contents[cur_page - 1])
                        else:
                            cur_page += 1
                            mal = discord.Embed(title=f"📫라이젠 메일함 | {pages - int(uncheck_cur_fetchone[1])}개 수신됨",
                                                description="주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                                                colour=ctx.author.colour)
                            mal.add_field(name=f"{pages}중 {cur_page}번째 메일({timess[contents[cur_page - 1]]}작성)",
                                          value=contents[cur_page - 1])
                        await message.edit(embed=mal)

                    elif str(reaction.emoji) == "◀️" and cur_page > 1:
                        if check2 is None:
                            cur_page -= 1
                            mal = discord.Embed(title=f"📫라이젠 메일함 | {str(pages)}개 수신됨",
                                                description="주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                                                colour=ctx.author.colour)
                            mal.add_field(name=f"{pages}중 {cur_page}번째 메일", value=contents[cur_page - 1])
                        else:
                            cur_page -= 1
                            mal = discord.Embed(title=f"📫라이젠 메일함 | {pages - int(uncheck_cur_fetchone[1])}개 수신됨",
                                                description="주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                                                colour=ctx.author.colour)
                            mal.add_field(name=f"{pages}중 {cur_page}번째 메일({timess[contents[cur_page - 1]]}작성)",
                                          value=contents[cur_page - 1])
                        await message.edit(embed=mal)
                except asyncio.TimeoutError:
                    break
        elif mode == "전체":
            dictcommand = await self.read_email_from_db(ctx=ctx)
            contents = dictcommand["contents"]
            timess = dictcommand["timess"]
            pages = dictcommand["pages"]
            mal = discord.Embed(title=f"📫라이젠 메일함",
                                description="주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                                colour=ctx.author.colour)
            cur_page = 1
            # noinspection DuplicatedCode
            mal.add_field(name=f"{pages}중 {cur_page}번째 메일({timess[contents[cur_page - 1]]}작성)",
                          value=contents[cur_page - 1])
            message = await ctx.send(embed=mal)

            await message.add_reaction("◀️")
            await message.add_reaction("▶️")

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"] and reaction.message.id == message.id
                # This makes sure nobody except the command sender can interact with the "menu"

            while True:
                try:
                    reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                    # waiting for a reaction to be added - times out after x seconds, 60 in this
                    # example

                    if str(reaction.emoji) == "▶️" and cur_page != pages:
                        cur_page += 1
                        mal = discord.Embed(title=f"📫라이젠 메일함",
                                            description="주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                                            colour=ctx.author.colour)
                        mal.add_field(name=f"{pages}중 {cur_page}번째 메일({timess[contents[cur_page - 1]]}작성)",
                                      value=contents[cur_page - 1])
                        await message.edit(embed=mal)

                    elif str(reaction.emoji) == "◀️" and cur_page > 1:
                        cur_page -= 1
                        mal = discord.Embed(title=f"📫라이젠 메일함",
                                            description="주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                                            colour=ctx.author.colour)
                        mal.add_field(name=f"{pages}중 {cur_page}번째 메일({timess[contents[cur_page - 1]]}작성)",
                                      value=contents[cur_page - 1])
                        await message.edit(embed=mal)
                except asyncio.TimeoutError:
                    break

    @staticmethod
    async def read_email_from_db(ctx):
        contents = []
        timess = {}
        database = await aiosqlite.connect("db/db.sqlite")
        cur = await database.execute('SELECT * FROM mail')
        uncheck_cur = await database.execute('SELECT * FROM uncheck WHERE user_id = ?',(ctx.author.id,))
        mails = await cur.fetchall()
        for i in mails:
            contents.append(i[1])
            timess[i[1]] = i[2]
        pages = len(contents)
        return {"contents": contents, "timess": timess, "database": database, "cur": cur, "uncheck_cur":uncheck_cur, "pages": pages}
def setup(bot):
    bot.add_cog(Core(bot))
