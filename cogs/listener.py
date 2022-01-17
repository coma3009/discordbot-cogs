from re import A
import discord
from discord import embeds
from discord import colour
from discord import message
from discord.ext import commands

import config
import random
import colorlog
import traceback
import asyncio
from discord import Activity, ActivityType
from discord_components import DiscordComponents
import datetime
import time
import timeit

from utils.embed import Embed


def generate_code(ctx):
    string = ""
    string += "E_"
    string += str(str(ctx.author.id)[:4])
    string += str(str(ctx.guild.id)[:5])
    string += str(len(ctx.command.name))
    string += str(len(str(ctx.command)))
    string += str(random.randrange(1, 7))
    string += str(random.randrange(1, 7))
    string += str(random.randrange(1, 7))
    string += str(random.randrange(1, 7))
    string += str(random.randrange(1, 7))

    return string

class Listener(commands.Cog, description="listener 처리용 파일입니다."):
    def __init__(self, bot):
        self.bot = bot
        self.logger = colorlog.getLogger("Bot")

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        DiscordComponents(self.bot)
        self.logger.info(f"Ready {str(self.bot.user)}({str(self.bot.user.id)})")
        await self.bot.change_presence(
            activity=Activity(
                name="asdf", type=ActivityType.playing
            )
            
        )
        now = datetime.datetime.now()
        logch = self.bot.get_channel(875504332055904266)
        embed = discord.Embed(
            title="봇구동로그",
            description=f"날짜 : {now.year}년 {now.month}월 {now.day}일 \n 시간 : {now.hour:02}시 {now.minute:02}분 \n 봇이 시작됬습니다",
            colour = discord.Colour.blue(),

        ).set_thumbnail(url="https://cdn.discordapp.com/app-icons/872714206246469662/b2cf639a78e58b0af178a980764d472d.png?size=256")        
        await logch.send(embed=embed)

        async def message(games):
            await self.bot.wait_until_ready()

            while not self.bot.is_closed():
                for g in games:
                    await self.bot.change_presence(status = discord.Status.online, activity = discord.Game(g))
                    await asyncio.sleep(5)

        await message(['🟢 정상작동','제작자 : Coma#3009','🙇 모든 문의 DM!','>도움말 해주세요.','접두사 >',f'라이젠은 {len(self.bot.guilds)}개의 서버에 있습니다'])

    @commands.Cog.listener()
    async def on_command(self, ctx):
       self.logger.info(f"{ctx.author}({ctx.author.id}) - {ctx.message.content}")
       await self.bot.get_channel(int(config.BotSettings.logging_channel)).send(f"{ctx.author}({ctx.author.id}) - `{ctx.message.content}`")
       await self.bot.get_channel(int(config.BotSettings.stafflog)).send(f"{ctx.author}({ctx.author.id}) - `{ctx.message.content}`")

    @commands.Cog.listener()
    async def on_command(self, ctx):
        channel = self.bot.get_channel(860099054380908564)
        adminchannel = self.bot.get_channel(895272688510197760)
        embed = discord.Embed(
            title ="일반로그",
            description= f"닉네임 : {ctx.author} \n \n 아이디 : {ctx.author.id} \n \n 명령어로그 : {ctx.message.content}",
            color= 0x0000ff
        ).set_thumbnail(url="https://cdn.discordapp.com/app-icons/872714206246469662/b2cf639a78e58b0af178a980764d472d.png?size=256")        
        embed.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=embed)
        await adminchannel.send(embed=embed)
        


    #@commands.command()
    #async def on_member_join(self, ctx, member):
    #    channel = self.bot.get_channel(id).send(857233842137595904)
    #    if (member.join)
    #    await member.send('안녕하세요')
    #    await channel.send()
    


    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not member.guild.id == 856829534926143538: 
            return
        channel = self.bot.get_channel(857233842137595904)
        embed = discord.Embed(
            description=f" {member.mention},{member.name}님 ℝ𝕪𝕫𝕖𝕟 𝕆𝕗𝕗𝕚𝕔𝕒𝕝 𝕊𝕖𝕣𝕧𝕖𝕣에 오신것을 환영합니다. \n \n__<#858196187622146058>__ 을 해주세요!",
            color= 0x0000ff
        ).set_thumbnail(url="https://cdn.discordapp.com/app-icons/872714206246469662/b2cf639a78e58b0af178a980764d472d.png?size=256")        
        await channel.send(embed=embed)
        await member.add_roles(discord.utils.get(member.guild.roles, id=857396841887694858))
        guild = self.bot.get_guild(856829534926143538)
        alluser = guild.get_channel(894962207991926825)
        user = guild.get_channel(894962209157959770)
        bot= guild.get_channel(894962210441416714)
        await alluser.edit(name = f"모든유저ㅣ {len(guild.members)}")
        await user.edit(name = f"유저ㅣ {len([x for x in guild.members if not x.bot])}")
        await bot.edit(name = f"봇ㅣ {len([x for x in guild.members if x.bot])}")


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if not member.guild.id == 856829534926143538:
            return
        channel = self.bot.get_channel(857234508679348225)
        embed = discord.Embed(
            description=f" {member.mention},{member.name}님 ℝ𝕪𝕫𝕖𝕟 𝕆𝕗𝕗𝕚𝕔𝕒𝕝 𝕊𝕖𝕣𝕧𝕖𝕣에서 나가셨습니다.... \n \n ",
            color= 0x0000ff
        ).set_thumbnail(url="https://cdn.discordapp.com/app-icons/872714206246469662/b2cf639a78e58b0af178a980764d472d.png?size=256")        
        await channel.send(embed=embed)
        guild = self.bot.get_guild(856829534926143538)
        alluser = guild.get_channel(894962207991926825)
        user = guild.get_channel(894962209157959770)
        bot= guild.get_channel(894962210441416714)
        await alluser.edit(name = f"모든유저ㅣ {len(guild.members)}")
        await user.edit(name = f"유저ㅣ {len([x for x in guild.members if not x.bot])}")
        await bot.edit(name = f"봇ㅣ {len([x for x in guild.members if x.bot])}")
                    


    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not before.guild.id == 856829534926143538:
            return
        embed=discord.Embed(title="메시지수정로그", color=0x00FFFF)
        embed.set_footer(text=f"멤버 이름 :{before.author.name} • Message ID: {before.id}")
        embed.timestamp = datetime.datetime.utcnow()
        embed.add_field(name='수정전:', value=before.content , inline=False)
        embed.add_field(name="수정후:", value=after.content , inline=False)
        embed.set_thumbnail(url="https://cdn.discordapp.com/app-icons/872714206246469662/b2cf639a78e58b0af178a980764d472d.png?size=256")        
        channel = self.bot.get_channel(856829534926143541)
        adminchannel = self.bot.get_channel(895272688510197760)
        await channel.send(embed=embed)
        await adminchannel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.guild.id == 856829534926143538:
            return
        embed = discord.Embed(title="메시지 삭제로그", color= 0x0000ff)
        embed.add_field(name="**메시지삭제**", value=f"메시지 : {message.content} \n \n 삭제됨")
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/873899327758692352/810ef9d933f9985d82f441de0a03fb6b.webp?size=80")
        embed.timestamp = datetime.datetime.utcnow()
        embed.colour = (0x000ff)
        dele = self.bot.get_channel(856829534926143541)
        adminchannel = self.bot.get_channel(895272688510197760)
        await dele.send(embed=embed)
        await adminchannel.send(embed=embed)


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        ignoredError = (
            commands.CommandNotFound,
            commands.errors.CheckFailure,
            commands.CheckFailure,
        )
        if isinstance(error, ignoredError):
            return

        elif isinstance(error, commands.CommandOnCooldown):
            cooldown = int(error.retry_after)
            hours = cooldown // 3600
            minutes = (cooldown % 3600) // 60
            seconds = cooldown % 60
            time = []
            if not hours == 0:
                time.append(f"{hours}시간")
            if not minutes == 0:
                time.append(f"{minutes}분")
            if not seconds == 0:
                time.append(f"{seconds}초")
            embed = Embed.warn(
                timestamp=ctx.message.created_at,
                description=f"사용하신 명령어는 ``{' '.join(time)}`` 뒤에 사용하실 수 있습니다.",
            )
            Embed.user_footer(embed, ctx)
            return await ctx.send(embed=embed, hidden=True)

        elif isinstance(error, commands.MissingPermissions):
            a = ""
            for p in error.missing_perms:
                if str(p) == "manage_messages":
                    p = "메시지 관리"
                elif str(p) == "kick_members":
                    p = "멤버 추방"
                elif str(p) == "ban_members":
                    p = "멤버 차단"
                elif str(p) == "administrator":
                    p = "관리자"
                elif str(p) == "create_instant_invite":
                    p = "초대링크 생성"
                elif str(p) == "manage_channels":
                    p = "채널 관리"
                elif str(p) == "manage_guild":
                    p = "서버 관리"
                elif str(p) == "add_reactions":
                    p = "메시지 반응 추가"
                elif str(p) == "view_audit_log":
                    p = "감사 로그 보기"
                elif str(p) == "read_messages":
                    p = "메시지 읽기"
                elif str(p) == "send_messages":
                    p = "메시지 보내기"
                elif str(p) == "read_message_history":
                    p = "이전 메시지 읽기"
                elif str(p) == "mute_members":
                    p = "멤버 음소거 시키기"
                elif str(p) == "move_members":
                    p = "멤버 채널 이동시키기"
                elif str(p) == "change_nickname":
                    p = "자기자신의 닉네임 변경하기"
                elif str(p) == "manage_nicknames":
                    p = "다른유저의 닉네임 변경하기"
                elif str(p) == "manage_roles":
                    p = "역활 관리하기"
                elif str(p) == "manage_webhooks":
                    p = "웹훅크 관리하기"
                elif str(p) == "manage_emojis":
                    p = "이모지 관리하기"
                elif str(p) == "use_slash_commands":
                    p = "/ 명령어 사용"
                if p != error.missing_perms[len(error.missing_perms) - 1]:
                    a += f"{p}, "
                else:
                    a += f"{p}"
            embed = Embed.warn(
                timestamp=ctx.message.created_at,
                description=f"당신의 권한이 부족합니다.\n\n> 필요 권한 : {str(a)}",
            )
            Embed.user_footer(embed, ctx)
            return await ctx.send(
                embed=embed,
                hidden=True,
            )

        elif isinstance(error, commands.BotMissingPermissions):
            a = ""
            for p in error.missing_perms:
                if str(p) == "manage_messages":
                    p = "메시지 관리"
                elif str(p) == "kick_members":
                    p = "멤버 추방"
                elif str(p) == "ban_members":
                    p = "멤버 차단"
                elif str(p) == "administrator":
                    p = "관리자"
                elif str(p) == "create_instant_invite":
                    p = "초대링크 생성"
                elif str(p) == "manage_channels":
                    p = "채널 관리"
                elif str(p) == "manage_guild":
                    p = "서버 관리"
                elif str(p) == "add_reactions":
                    p = "메시지 반응 추가"
                elif str(p) == "view_audit_log":
                    p = "감사 로그 보기"
                elif str(p) == "read_messages":
                    p = "메시지 읽기"
                elif str(p) == "send_messages":
                    p = "메시지 보내기"
                elif str(p) == "read_message_history":
                    p = "이전 메시지 읽기"
                elif str(p) == "mute_members":
                    p = "멤버 음소거 시키기"
                elif str(p) == "move_members":
                    p = "멤버 채널 이동시키기"
                elif str(p) == "change_nickname":
                    p = "자기자신의 닉네임 변경하기"
                elif str(p) == "manage_nicknames":
                    p = "다른유저의 닉네임 변경하기"
                elif str(p) == "manage_roles":
                    p = "역활 관리하기"
                elif str(p) == "manage_webhooks":
                    p = "웹훅크 관리하기"
                elif str(p) == "manage_emojis":
                    p = "이모지 관리하기"
                elif str(p) == "use_slash_commands":
                    p = "/ 명령어 사용"
                if p != error.missing_perms[len(error.missing_perms) - 1]:
                    a += f"{p}, "
                else:
                    a += f"{p}"
            embed = Embed.warn(
                timestamp=ctx.message.created_at,
                description=f"봇의 권한이 부족합니다.\n\n> 필요 권한 : {str(a)}",
            )
            Embed.user_footer(embed, ctx)
            return await ctx.send(
                embed=embed,
            )

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = Embed.warn(
                timestamp=ctx.message.created_at, description="필요한 값이 존재하지 않습니다."
            )
            Embed.user_footer(embed, ctx)
            return await ctx.send(
                embed=embed,
                hidden=True,
            )

        elif isinstance(error, commands.MemberNotFound):
            embed = Embed.warn(timestamp=ctx.message.created_at, description="존재하지 않는 멤버입니다.")
            Embed.user_footer(embed, ctx)
            return await ctx.send(
                embed=embed,
                hidden=True,
            )

        else:
            tb = traceback.format_exception(type(error), error, error.__traceback__)
            err = [line.rstrip() for line in tb]
            errstr = "\n".join(err)
            # f = open(f"logs/{code}.log", "a", encoding="utf-8")
            # f.write(f"{ctx.author}({ctx.author.id}) -{ctx.message.content}\n에러 발생 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            # f.write("\n\n")
            # f.write(errstr)
            # f.close()
            embed = Embed.error(
                timestamp=ctx.message.created_at, description=f"```py\n{errstr}\n```"
            )
            Embed.user_footer(embed, ctx)
            print(errstr)

            return await ctx.send(
                embed=embed,
            )


def setup(bot):
    bot.add_cog(Listener(bot))
