
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parser.settings')
django.setup()
import asyncio
from aiogram import F
from aiogram import Bot, Dispatcher
from aiogram import Router
from aiogram.methods import DeleteWebhook
from aiogram.fsm.context import FSMContext
from aiogram import types
from products_parser.utils import get_products_for_last_parsing


ADMIN_GROUP_ID = '-1002068591035'


bot = Bot('7022682784:AAHTNCQWSKQCqY8TXWqWyiEVjA_ZKKqNLlw')
dp = Dispatcher()
router = Router()


async def on_startup():
    print('Запускаем бота...')
    dp.include_router(router)
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)
    print('Бот запущен')


@router.message(F.text == 'Список товаров')
async def about_us_button(message: types.Message, state: FSMContext):
    print('...')
    msg_text = 'Список товаров последнего парсинга\n'

    products_list = await get_products_for_last_parsing()

    for i, product in enumerate(products_list):
        msg_text += f'\n    <b>{i + 1}.</b> {product.name}\n       <a href="{product.link}">Ссылка</a>'
        if (i + 1) % 20 == 0:
            await message.answer(text=msg_text, parse_mode='HTML')
            msg_text = ''

    await message.answer(text=msg_text, parse_mode='HTML')


def send_notification_about_success(products_count):
    bot = Bot('7022682784:AAHTNCQWSKQCqY8TXWqWyiEVjA_ZKKqNLlw')
    msg_text = f'''
Задача на парсинг товаров с сайта Ozon завершена.
Сохранено: <b>{products_count}</b> товаров.
    '''
    asyncio.run(bot.send_message(chat_id=ADMIN_GROUP_ID,
                     text=msg_text,
                     parse_mode='HTML'))


def send_notification_about_errors(products_count):
    bot = Bot('7022682784:AAHTNCQWSKQCqY8TXWqWyiEVjA_ZKKqNLlw')
    msg_text = f'''
    В процессе выполнения задачи на парсинг товаров с сайта Ozon произошла ошибка.
    Сохранено: <b>{products_count}</b> товаров.
        '''
    asyncio.run(bot.send_message(chat_id=ADMIN_GROUP_ID,
                     text=msg_text,
                     parse_mode='HTML'))


if __name__ == '__main__':
    print('dsggs')
    asyncio.run(on_startup())
