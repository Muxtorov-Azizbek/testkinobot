from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish\n",
            "/help - Yordam\n"
            "/kino_add - Kino yaratish\n"
            "/kino_delete - Kinoni o'chirish\n"
            "/count_kinos - Kinolarni soni\n")

    await message.answer("\n".join(text))