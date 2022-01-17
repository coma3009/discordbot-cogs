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


class helps(commands.Cog, name = "봇 도움 명령어", description = "봇 도움 명령어 Cog입니다."):
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
    @commands.command(name="도움말", aliases=["도움"])
    async def helps(self, ctx):
        embed=discord.Embed(title="도움말", description="[라이젠서포트서버](https://discord.gg/d7zEFsbMVN) \n라이젠봇 접두사는 `>` 입니다.", color=0x0000ff)
        embed.add_field(name="관리기능", value="""
```diff
+ 킥
+ 밴
+ 언밴
+ 뮤트
+ 언뮤트
+ 청소
+ 처벌
+ 처벌 추가
+ 처벌 제거
+ 처벌 조회
+ 옵션
+ 티켓설정
```
        """)
        embed.add_field(name="기본기능", value="""
```diff
+ 도움말
+ 작동확인
+ 유저정보
+ 서버정보
+ 프사
+ 가위바위보
+ 서포트
+ 하트인증
+ 블랙
+ 생일
+ 생일삭제
+ 생일등록
```
        """)
        embed.add_field(name="뮤직기능", value="""
```diff
+ 나가
+ 재생
+ 지금곡
+ 들어와
+ 일시정지
+ 이어재생
+ 볼륨
+ 루프
+ 큐루프
+ 노래기록
+ 정지
+ 스킵
+ 큐
+ 반복확인
+ 셔플
+ 자동재생
+ 이전곡
+ 뮤직셋업(관리자기능)
```
        """)
        embed.add_field(name="코로나", value="""
```diff
+ 코로나현황
```
        """)
        embed.add_field(name="도박기능", value="""
```diff
+ 가입
+ 돈확인
+ 지원금
+ 도박
+ 입금
+ 출금
+ 탈퇴
```
        """)
        embed.add_field(name="개발자전용기능", value="""
```diff
+ 공지
+ 돈주기
+ 블랙 추가
+ 블랙 삭제
+ 서버리스트
+ 서버탈퇴
+ 도박목록
```
        """)
        embed.add_field(name="업데이트", value="""
```diff
+ 1월 16일 모든 시스템 리메이크 database 초기화
```
        """)
        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(helps(bot))
