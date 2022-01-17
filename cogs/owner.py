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

    @commands.group(name="블랙",invoke_without_command=True)
    async def blacklist(self,ctx:commands.Context):
        database = await aiosqlite.connect("db/db.sqlite")
        cur = await database.execute("SELECT * FROM black WHERE user = ?", (ctx.author.id,))
        if await cur.fetchone() == None:
            return await ctx.reply(f"{ctx.author}님은 블랙리스트에 등록되어있지 않아요.")
        data = await cur.fetchone()
        await ctx.reply(f"블랙사유: {data[1]}")
    @blacklist.command(name= '추가', aliases=['black','블랙','blackadd'])
    @commands.is_owner()
    async def mod_black(self, ctx, user_id:int,*,reason):
        user = await self.bot.fetch_user(user_id)
        db = await aiosqlite.connect("db/db.sqlite")
        cur = await db.execute("SELECT * FROM black WHERE user = ?", (user_id,))
        datas = await cur.fetchone()
        if datas != None:
            embed = discord.Embed(
                title = f"블랙",
                description = f"{user}님은 블랙리스트에 등록되어있어요. \n사유: {datas[1]}",
                colour = discord.Colour.random(),
                timestamp = ctx.message.created_at
            )
            await ctx.send(embed=embed)
        await db.execute("INSERT INTO black(user,reason,username) VALUES (?,?,?)", (user_id, reason, user.name))
        await db.commit()
        embed2=discord.Embed(
            title="블랙",
            description = f"__봇관리자로 부터 블랙 등록되었음을 알려드립니다__ \n\n 관리자가 아래의 사유로 블랙을 등록하셨어요.\n\n 사유 : {reason}",
            colour=discord.Colour.random() )
       
        try:
            await user.send(embed=embed2)
        except:
            pass
        await ctx.reply("등록완료!")
    @blacklist.command(name= '삭제', aliases=['blackdel','제거'])
    @commands.is_owner()
    async def mod_black_del(self, ctx, user_id:int):
        user = await self.bot.fetch_user(user_id)
        db = await aiosqlite.connect("db/db.sqlite")
        cur = await db.execute("SELECT * FROM black WHERE user = ?", (user_id,))
        datas = await cur.fetchone()
        embed=discord.Embed(title="블랙", description=f"{user}님은 블랙리스트에 등록되어있지않아요.",colour=discord.Colour.random())
        if datas ==  None:
            return await ctx.send(embed=embed)
        await db.execute("DELETE FROM black WHERE user = ?", (user_id,))
        await db.commit()
        embed2=discord.Embed(title="블랙", description="__봇 관리자로부터 블랙해제됨.__\n\n 봇관리자가 블랙해제하셨어요.",colour=discord.Colour.random())
        try:
            await user.send(embed=embed2)
        except:
            print
        await ctx.reply("해제완료")
            #await ctx.send(templates[1])
    @blacklist.command(name= '목록', aliases=['조회'])
    @commands.is_owner()
    async def mod_black_jo(self, ctx):
        database = await aiosqlite.connect("db/db.sqlite")
        cur = await database.execute("SELECT * FROM black")
        datas = await cur.fetchall()
        black_list = []
        for i in datas:
            black_list.append(f"```유저아이디|{i[0]} \n사유|{i[1]} \n이름|{i[2]}```")       
        e = Paginator(
                client=self.bot.components_manager,
                embeds=discordSuperUtils.generate_embeds(
                    black_list,
                    title=f"블랙목록에 유저들이 등록되어있어요.",
                    fields=10,
                    description="```블랙해제를 하실거면 \n>블랙 제거 [유저아이디]를 해주시면 됩니다!```",
                ),
                channel=ctx.channel,
                only=ctx.author,
                ctx=ctx,
                use_select=False)
        await e.start()
    @blacklist.command(name= '초기화', aliases=["reset"])
    @commands.is_owner()
    async def black_rest(self, ctx):
        db = await aiosqlite.connect("db/db.sqlite")
        await db.execute("DELETE FROM black")
        await db.commit()
        
        cur = await db.execute("SELECT * FROM black")
        datas = await cur.fetchall()
        if datas != None:
            await ctx.reply("초기화 완료")
    
    @commands.command(name="디엠")
    @commands.is_owner()
    async def dm(self, ctx, user_id:int, *, reason):
        try:
            user1 = await self.bot.fetch_user(user_id)
            embed=discord.Embed(title="알림", description="봇관리자로 부터 메시지가 왔습니다. \n궁금한 사항이나 오류발견시 봇 디엠으로 문의넣어주세요.", colour=discord.Colour.random())
            embed.add_field(name="메시지내용", value=f"{reason}")
            await user1.send(embed=embed)
            await ctx.send("전송완료!")
        except:
            print(traceback.format_exc())
            await ctx.send((traceback.format_exc()))
    @commands.command(name="서버탈퇴" ,aliases=['나와', '나가' '탈퇴'])
    @commands.is_owner()
    async def get_out(self, ctx, guild_id: int):
        if isinstance(ctx.channel, discord.abc.PrivateChannel) == True:
                msg2 = await ctx.send('서버 찾는중 ( ' + '0' + ' )')
                count = 0
                for guild in self.bot.guilds:
                    if guild.id == guild_id:
                        await guild.leave()
                        await ctx.send('`' + str(guild.name) + '` 에서 나왔어요!')
                        print(str(guild.name))
                    else:
                        pass
                    
                    count = count+1
                    show_count = str(count)
                    await msg2.edit(content = '서버 찾는중 ( ' + show_count + ' )')
    @commands.command(name="리붓", aliases=["리부팅","리스타트"])
    @commands.is_owner()
    async def rebooting(self, ctx   ):
        try:
            await ctx.send("리부팅시작!")
            await asyncio.sleep(2)
            os.system("pm2 restart MainRyzen 0")

        except:
            print(traceback.format_exc())
            await ctx.send((traceback.format_exc()))
    @commands.command(name="메일작성")
    @commands.is_owner()
    async def mail(self, ctx, *, va_lue):
        database = await aiosqlite.connect("db/db.sqlite")
        cur = await database.execute('SELECT * FROM mail')
        mails = await cur.fetchall()
        print(mails)
        check = 1
        # noinspection PyBroadException
        try:
            for _ in mails:
                check += 1
        except Exception as e:
            print(e)
        await database.execute(
            'INSERT INTO mail(id,value) VALUES (?,?)', (check, va_lue)
        )

        await database.commit()
        await ctx.send('성공적으로 메일을 발송하였습니다.')
    @commands.command(name="디엠")
    @commands.is_owner()
    async def dm(self, ctx, user_id:int, *, reason):
        try:
            user1 = await self.bot.fetch_user(user_id)
            embed=discord.Embed(title="알림", description="봇관리자로 부터 메시지가 왔습니다. \n궁금한 사항이나 오류발견시 봇 디엠으로 문의넣어주세요.", colour=discord.Colour.random())
            embed.add_field(name="메시지내용", value=f"{reason}")
            await user1.send(embed=embed)
            await ctx.send("전송완료!")
        except:
            print(traceback.format_exc())
def setup(bot):
    bot.add_cog(Owner(bot))