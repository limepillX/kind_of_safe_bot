from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from database import Message

BOT_TOKEN = ...
ADMIN_ID = ...
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.reply("Привет! Напиши мне сообщение и я перешлю его администратору")


@dp.message()
async def echo(message: types.Message):
    if message.from_user.id == ADMIN_ID and message.reply_to_message:
        info = Message.get_or_none(message_id=message.reply_to_message.message_id)
        if info:
            await bot.send_message(info.user_id, message.text)
            await message.reply('Сообщение отправлено пользователю')
        else:
            await bot.send_message(ADMIN_ID, 'Не удалось найти пользователя/сообщение уже отвечено')
            Message.delete_by_id(info.id)

    elif message.from_user.id != ADMIN_ID:
        sent_message = await bot.send_message(ADMIN_ID, message.text)
        Message.create(message_id=sent_message.message_id, user_id=message.from_user.id)
        await message.reply('Сообщение отправлено администратору')


if __name__ == '__main__':
    dp.run_polling(bot)
