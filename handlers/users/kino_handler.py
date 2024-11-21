from distutils.util import execute
from idlelib.zoomheight import set_window_geometry
from re import search
from string import capwords

from Tools.scripts.pysource import walk_python_files
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from data.config import ADMINS
from loader import dp,bot,kino_db
from keyboards.default.button_kino import menu_movie


class KinoAdd(StatesGroup):
    kino_add=State()
    kino_code=State()

class KinoDelete(StatesGroup):
    kino_code=State()
    is_confirm=State()



#linolar qo'shish uchun handler
@dp.message_handler(commands="kino_add")
async def message_kino_add(message:types.Message):
    admin_id=message.from_user.id
    if admin_id in ADMINS:
        await KinoAdd.kino_add.set()
        await message.answer("𝗞𝗶𝗻𝗼𝗻𝗶 𝘆𝘂𝗯𝗼𝗿𝗶𝗻𝗴 ")

    else:
        await message.answer("𝗦𝗶𝘇 𝗮𝗱𝗺𝗶𝗻𝘀 𝗲𝗺𝗮𝘀𝘀𝗶𝘇. Admin bo'lish uchun @KingKorolevskiy ga yozing")

@dp.message_handler(state=KinoAdd.kino_add,content_types=types.ContentType.VIDEO)
async def kino_file_handler(message:types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['file_id']=message.video.file_id
        data['caption']=message.caption
    await KinoAdd.kino_code.set()
    await message.answer("𝗞𝗶𝗻𝗼 𝘂𝗰𝗵𝘂𝗻 𝗞𝗼𝗱 𝗸𝗶𝗿𝗶𝘁𝗶𝗻𝗴")

@dp.message_handler(state=KinoAdd.kino_code,content_types=types.ContentType.TEXT)
async def kino_code_handler(message:types.Message,state:FSMContext):
    try:
        post_id=int(message.text)
        async with state.proxy() as data:
            data['post_id']=post_id
            kino_db.add_kino(post_id=data['post_id'],file_id=data['file_id'],caption=data['caption'])
        await message.answer("𝗞𝗶𝗻𝗼 𝗺𝘂𝘃𝗮𝗳𝗳𝗶𝗾𝗶𝘆𝗮𝘁𝗹𝗶 𝗾𝗼'𝘀𝗵𝗶𝗹𝗱𝗶 ")
        await state.finish()
    except ValueError :
        await message.answer("𝗜𝗹𝘁𝗶𝗺𝗼𝘀 𝗸𝗶𝗻𝗼 𝗸𝗼𝗱𝗶𝗻𝗶 𝗳𝗮𝗾𝗮𝘁 𝗿𝗮𝗾𝗮𝗺 𝗯𝗶𝗹𝗮𝗻 𝘆𝘂𝗯𝗼𝗿𝗶𝗻𝗴")


#kinolarni topish va uzatish



#movie  delete
@dp.message_handler(commands="kino_delete")
async def movie_delete_handler(message:types.Message):
    admin_id=message.from_user.id
    if admin_id in ADMINS:
        await KinoDelete.kino_code.set()
        await message.answer("O'chirmoqchi bo'lgan kino kodini yuboring ")

    else:
        await message.answer("Siz admin emassiz")


@dp.message_handler(state=KinoDelete.kino_code,content_types=types.ContentType.TEXT)
async def movie_kino_code(message:types,state:FSMContext):
    async with state.proxy() as data:
        data['post_id']=int(message.text)
        result=kino_db.search_kino_by_post_id(data['post_id'])
        if result:
            await message.answer_video(video=result['file_id'],caption=result['caption'])

        else:
            await message.answer(f"{data['post_id']} : kod bilan kino topilmadi ")

    await KinoDelete.is_confirm.set()
    await message.answer("Quyidagilardan birini tanlang  ",reply_markup=menu_movie)


@dp.message_handler(state=KinoDelete.is_confirm, content_types=types.ContentType.TEXT)
async def movie_kino_code(message: types, state: FSMContext):
    async with state.proxy() as data:
        data['is_confirm'] = message.text
        if data['is_confirm']=="✅Tasdiqlash":
            kino_db.delete_kino(data['post_id'])
            await message.answer("Kino muvaffaqiyatli o'chirildi")
            await state.finish()
        else:
            await message.answer("Bekor qilindi")
            await state.finish()

@dp.message_handler(commands="count_kinos")
async def message_count_kino(message:types.Message):
    count=kino_db.count_kinos()
    admin_id=message.from_user.id
    if admin_id in ADMINS:
        await message.answer(f"𝗕𝗮𝘇𝗮𝗱𝗮 {count['count']} 𝘁𝗮 𝗸𝗶𝗻𝗼 𝗯𝗼𝗿")

    else:
        await message.answer("Siz admin emassiz")






@dp.message_handler(lambda x:x.text.isdigit())
async def search_kino_handler(message:types.Message):
    if message.text.isdigit():
        post_id=int(message.text)
        data=kino_db.search_kino_by_post_id(post_id)
        if data:
            try:
                await bot.send_video(
                    chat_id=message.from_user.id,
                    video=data['file_id'],
                    caption=data['caption']
                )
            except Exception as err:
                await message.answer(f" 𝗞𝗶𝗻𝗼 𝘁𝗼𝗽𝗶𝗹𝗱𝗶 𝗹𝗲𝗸𝗶𝗻 𝘆𝘂𝗯𝗼𝗿𝗶𝘀𝗵𝗱𝗮 𝘅𝗮𝘁𝗼𝗹𝗶𝗸 𝗯𝗼𝗿 : {err}")
        else:
            await message.answer(f"{post_id} 𝗸𝗼𝗱 𝗯𝗶𝗹𝗮𝗻 𝗸𝗶𝗻𝗼 𝘁𝗼𝗽𝗶𝗹𝗺𝗮𝗱𝗶")
    else:
        await message.answer("𝗜𝗹𝘁𝗶𝗺𝗼𝘀 𝗸𝗶𝗻𝗼 𝗸𝗼𝗱𝗶𝗻𝗶 𝗿𝗮𝗾𝗮𝗺 𝗯𝗶𝗹𝗮𝗻 𝘆𝘂𝗯𝗼𝗿𝗶𝗻𝗴")




