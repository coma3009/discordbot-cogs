import discord
from discord.ext import commands

import os
import pytz
import sqlite3
import asyncio
import datetime
import traceback
from discord_components import Button, ButtonStyle, SelectOption, Select
import discord_components


class warning(commands.Cog, name = "서버 경고 명령어", description = "봇 경고 명령어"):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(
        name = "경고",
        aliases = ["warn"]
    )
    @commands.is_owner()
    async def mod_warn(self, ctx, user: discord.User = None, *, reason):
        logch = self.bot.get_channel(861952657014390815)
        if not user:
            return await ctx.send(f"{ctx.author.mention}, 유저가 없단다")
        if user.bot:
            return await ctx.send("봇은 경고 못함")
        if ctx.guild.get_member(user.id).top_role >= ctx.author.top_role:
            return await ctx.send("너보다 높은면 못함")
        msg = await ctx.send(
            content = f"{user}님에게 {reason}의 사유로 경고를 지급하시겠습니까?",
            components = [
                [
                    Button(label="네", emoji="✅", style=ButtonStyle.green, id="yes"),
                    Button(label="아니요", emoji="❎", style=ButtonStyle.red, id="no"),
                ]
            ]
        )
        def check(res):
            return ctx.author == res.user and res.channel == ctx.channel

        try:
            res = await self.bot.wait_for("button_click", check=check, timeout=60)
            if res.component.id == "no":
                return await msg.edit(content = "취소하였습니다.", components = [])
        except asyncio.TimeoutError:
            return await msg.edit(content = "시간 초과로 취소되었습니다.", components = [])
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM warn;")
        warl = cur.fetchone()
        case = warl[0]
        warnlog = 0
        for a in cur.execute("SELECT * FROM warn WHERE user = '{}'".format(user.id)):
            warnlog += 1
        conn.close()
        warnembed = discord.Embed(
            colour=discord.Colour.gold(),
            title=f"#{int(case) + 1}",
        )
        warnembed.add_field(
            name="👮‍♂️ 처리자",
            value=f"{ctx.author.mention} ({ctx.author})",
            inline=False,
        )
        warnembed.add_field(
            name="🙍‍♂️ 처벌 대상자", value=f"{user.mention} ({user})", inline=False
        )
        warnembed.add_field(
            name="📋 정보",
            value=f"사유 : {reason}\n현재 {user}님의 경고 : {warnlog + 1}/5",
            inline=False,
        )
        m = await logch.send(embed=warnembed)
        try:
            await user.send(embed=warnembed)
        except:
            pass
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO warn VALUES ('{}', '{}', '{}', 'warn', '{}')".format(
                user.id, reason, m.id, ctx.author.id
            )
        )
        conn.commit()
        warn1 = 0
        for a in cur.execute("SELECT * FROM warn WHERE user = '{}'".format(user.id)):
            warn1 += 1
        conn.close()
        if int(warn1) == 5:
            conn = sqlite3.connect("database.db") # 이러니까 안되지 ㅡㅡ
            cur = conn.cursor()
            cur.execute("SELECT count(*) FROM warn;")
            warl = cur.fetchone()
            case = warl[0]
            banembed = discord.Embed(
                colour=discord.Colour.red(),
                title=f"#{int(case) + 1}",
            )
            banembed.add_field(
                name="👮‍♂️ 처리자",
                value=f"{ctx.author.mention} ({ctx.author})",
                inline=False,
            )
            banembed.add_field(
                name="🙍‍♂️ 처벌 대상자", value=f"{user.mention} ({user})", inline=False
            )
            banembed.add_field(
                name="📋 정보", value=f"사유 : 경고가 5회 누적되어 서버에서 차단되었어요.", inline=False
            )
            m = await logch.send(embed=banembed)
            try:
                await user.send(embed=banembed)
            except:
                pass
            await ctx.guild.ban(user, reason="경고가 5회 누적되어 서버에서 차단되었어요.")
            cur.execute(
                "INSERT INTO warn VALUES ('{}', '경고가 5회 누적되어 서버에서 차단되었어요.', '{}', 'ban')".format(
                    user.id, m.id
                )
            )
            conn.commit()
            conn.close()
        await msg.edit(content = f"{ctx.author.mention} 경고 지급을 완료하였습니다!", components = [])


    # @commands.command(
    #     name = "경고",
    #     aliases = ["warn"]
    # )
    # @commands.is_owner()
    # async def mod_warn(self, ctx, user: discord.User = None, *, reason):
    #     try:
    #         logch = self.bot.get_channel(861952657014390815)
    #         if not user:
    #             return await ctx.send(f"{ctx.author.mention}, 유저가 없단다")
    #         if user.bot:
    #             return await ctx.send("봇은 경고 못함")
    #         if ctx.guild.get_member(user.id).top_role >= ctx.author.top_role:
    #             return await ctx.send("너보다 높은면 못함")
    #         msg = await ctx.send(
    #             # content = f"{user}님에게 {reason}의 사유로 경고를 지급하시겠습니까?",
    #         components = [
    #                 [
    #                     Button(label="네", emoji="✅", style=ButtonStyle.green, id="yes"),
    #                     Button(label="아니요", emoji="❎", style=ButtonStyle.red, id="no"),
    #                 ]
    #             ]
    #         )
    #         def check(res):
    #             return ctx.author == res.user and res.channel == ctx.channel

    #         try:
    #             res = await self.bot.wait_for("button_click", check=check, timeout=60)
    #             if res.component.id == "no":
    #                 return await msg.edit(content = "취소하였습니다.", components = [])
    #         except asyncio.TimeoutError:
    #             return await msg.edit(content = "시간 초과로 취소되었습니다.", components = [])
    #         conn = sqlite3.connect("database.db")
    #         cur = conn.cursor()
    #         cur.execute("SELECT count(*) FROM warn;")
    #         warl = cur.fetchone()
    #         case = warl[0]
    #         warnlog = 0
    #         for a in cur.execute("SELECT * FROM warn WHERE user = '{}'".format(user.id)):
    #             warnlog += 1
    #         conn.close()
    #         warnembed = discord.Embed(
    #             colour=discord.Colour.gold(),
    #             title=f"#{int(case) + 1}",
    #         )
    #         warnembed.add_field(
    #             name="👮‍♂️ 처리자",
    #             value=f"{ctx.author.mention} ({ctx.author})",
    #             inline=False,
    #         )
    #         warnembed.add_field(
    #             name="🙍‍♂️ 처벌 대상자", value=f"{user.mention} ({user})", inline=False
    #         )
    #         warnembed.add_field(
    #             name="📋 정보",
    #             value=f"사유 : {reason}\n현재 {user}님의 경고 : {warnlog + 1}/5",
    #             inline=False,
    #         )
    #         m = await logch.send(embed=warnembed)
    #         try:
    #             await user.send(embed=warnembed)
    #         except:
    #             pass
    #         conn = sqlite3.connect("database.db")
    #         cur = conn.cursor()
    #         cur.execute(
    #             "INSERT INTO warn VALUES ('{}', '{}', '{}', 'warn', '{}')".format(
    #                 user.id, reason, m.id, ctx.author.id
    #             )
    #         )
    #         conn.commit()
    #         warn1 = 0
    #         for a in cur.execute("SELECT * FROM warn WHERE user = '{}'".format(user.id)):
    #             warn1 += 1
    #         conn.close()
    #         if int(warn1) == 5:
    #             conn = sqlite3.connect("database.db")
    #             cur = conn.cursor()
    #             cur.execute("SELECT count(*) FROM warn;")
    #             warl = cur.fetchone()
    #             case = warl[0]
    #             banembed = discord.Embed(
    #                 colour=discord.Colour.red(),
    #                 title=f"#{int(case) + 1}",
    #             )
    #             banembed.add_field(
    #                 name="👮‍♂️ 처리자",
    #                 value=f"{ctx.author.mention} ({ctx.author})",
    #                 inline=False,
    #             )
    #             banembed.add_field(
    #                 name="🙍‍♂️ 처벌 대상자", value=f"{user.mention} ({user})", inline=False
    #             )
    #             banembed.add_field(
    #                 name="📋 정보", value=f"사유 : 경고가 5회 누적되어 서버에서 차단되었어요.", inline=False
    #             )
    #             m = await logch.send(embed=banembed)
    #             try:
    #                 await user.send(embed=banembed)
    #             except:
    #                 pass
    #             await ctx.guild.ban(user, reason="경고가 5회 누적되어 서버에서 차단되었어요.")
    #             cur.execute(
    #                 "INSERT INTO warn VALUES ('{}', '경고가 5회 누적되어 서버에서 차단되었어요.', '{}', 'ban')".format(
    #                     user.id, m.id
    #                 )
    #             )
    #             conn.commit()
    #             conn.close()
    #         await msg.edit(content = f"{ctx.author.mention} 경고 지급을 완료하였습니다!", components = [])
    #     except:
    #         await ctx.send(traceback.format_exc())

def setup(bot):
    bot.add_cog(warning(bot))