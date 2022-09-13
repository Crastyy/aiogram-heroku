import logging
import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from aiogram import Bot, types
import socket
from aiohttp import web
from pyngrok import ngrok

# Env all
TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)


async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(text=f'{socket.gethostbyname(socket.gethostname())}')


@dp.message_handler(commands=['ngrok'])
async def negr(message: types.Message):
    await bot.send_message(message.from_user.id, text=f"{ngrok.get_tunnels()}")


if __name__ == '__main__':
    ngrok.set_auth_token("1wPxVgVCc0KYT6rwfF0nmtQndzl_7CLqbECNCy3S94RM4Fquz")
    http_tunnel = ngrok.connect()
    ssh_tunnel = ngrok.connect(80, "tcp")
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
    web.run_app(app)