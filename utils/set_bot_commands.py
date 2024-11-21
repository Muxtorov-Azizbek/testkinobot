from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish"),
            types.BotCommand("help", "Yordam"),
            types.BotCommand("kino_add", "Kino yaratish(adminlar uchun)"),
            types.BotCommand("kino_delete", "Kinoni o'chirish(adminlar uchun)"),
            types.BotCommand("count_kinos", "Kinolarni soni"),
        ]
    )
