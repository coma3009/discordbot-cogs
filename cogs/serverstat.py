import asyncio

import aiosqlite
import discord
import discordSuperUtils
from discord.ext import commands

class serverstat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stat = self.bot.loop.create_task(self.stat_loop())


    async def stat_loop(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            database = await aiosqlite.connect("db/db.sqlite")
            cur = await database.execute("SELECT * FROM serverstat")
            datas = await cur.fetchall()
            for i in datas:
                guild = self.bot.get_guild(i[0])
                all_count = len(guild.members)
                user_count = len([m for m in guild.members if not m.bot])
                bot_count = len([m for m in guild.members if m.bot])
                all_channel = self.bot.get_channel(i[2])
                user_channel = self.bot.get_channel(i[4])
                bot_channel = self.bot.get_channel(i[3])
                try:
                    await all_channel.edit(name=i[6].format(all=all_count))
                    await user_channel.edit(name=i[8].format(user=user_count))
                    await bot_channel.edit(name=i[7].format(bots=bot_count))
                except discord.Forbidden:
                    await guild.owner.send("서버스텟을 업데이트하려는 도중 채널관리권한이 부족하여 실패했어요! 제 권한을 확인해주세요.")
            await asyncio.sleep(30)

    def cog_unload(self):
        self.stat.cancel()


def setup(bot):
    bot.add_cog(serverstat(bot))