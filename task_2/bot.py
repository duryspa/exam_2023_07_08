from aiogram import Bot, Dispatcher, executor, types

from core import CONFIG
from core.logger import get_logger
from core.google_sheets import record_values


API_TOKEN = CONFIG.get('TOKEN')


logger = get_logger('bot')


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Введите текст для записи в Google таблицу")


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(
        "Если возникли вопросы или проблемы напишите нам "
        "на электронную почту fomenko.bot@gmail.com"
    )


@dp.message_handler()
async def receive_message(message: types.Message):
    username = message.from_user.username

    if not username:
        username = 'ОТСУТСТВУЕТ'
    
    try:
        result = record_values(username, message.text)
        
        if not result:
            raise Exception("Unsuccessful value records.")
        
    except Exception as e:
        logger.error(
            f"Receive message from user, user_id {message.from_user.id}. "
            f"Message: {e}"
        )
        await message.answer('❌ Ошибка!')
        return
        
    await message.answer('Принято!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
