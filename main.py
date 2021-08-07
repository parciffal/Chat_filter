from aiogram import types, Dispatcher, executor, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
import config
import pyperclip
from aiogram.dispatcher.filters.state import State, StatesGroup


class First(StatesGroup):
    S1 = State()
    S2 = State()

storage = MemoryStorage()
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=storage)
markup = types.InlineKeyboardMarkup()
markup.add(types.InlineKeyboardButton('Restart', callback_data='d'))


@dp.callback_query_handler(lambda call: call.data == 'd', state=First.S1)
async def callsds_S(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'd':
        await state.finish()


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def start(message: types.Message):
    i = message.text.find(config.PREFIX)
    if i != -1:
        print(message.text[i:i+40])
        #pyperclip.copy(message.text[i:i+40])
        await bot.send_message(message.chat.id, "text", reply_markup=markup)
        await First.S1.set()
    else:
        await bot.send_message(message.chat.id, 'Not found')

if __name__ == "__main__":
    executor.start_polling(dp)
