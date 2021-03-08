#!/usr/bin/env pipenv-shebang
import os
from threading import Thread

import yaml
import pretty_errors
from telegram.ext import Updater, CommandHandler, Filters


# read secret.yaml
with open('secret.yaml', 'r') as file:
    secret = yaml.load(file, Loader=yaml.FullLoader)
    PRESENSI = secret['token']['presensi']
    HORIREVENS = secret['token']['horirevens']

updater = Updater(token=PRESENSI, use_context=True)


def send_message(chat_id=159508674, text='...', parse_mode=None):
    """send message to client"""
    updater.bot.send_message(
        chat_id=chat_id, text=text, parse_mode=parse_mode)


def start(update, context):
    """run start command"""
    chat_id = update.message.chat.id
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    message = f'Hello {first_name} {last_name}.. your ID is {chat_id}'
    update.message.reply_text(message)


def stop_and_shutdown():
    updater.stop()
    updater.is_idle = False


def stop(update, context):
    """stop telegram bot"""
    update.message.reply_text('Bot is shutting down...')
    Thread(target=stop_and_shutdown).start()


def checkin(update, context):
    """run checkin.py script"""
    os.system('pipenv-shebang checkin.py')


def checkout(update, context):
    """run checkout.py script"""
    os.system('pipenv-shebang checkout.py')


def main():
    # filter by username
    yogitrismayana = Filters.user(username='@yogitrismayana')

    # init handler
    start_handler = CommandHandler('start', start)
    stop_handler = CommandHandler('stop', stop, filters=yogitrismayana)
    checkin_handler = CommandHandler(
        'checkin', checkin, filters=yogitrismayana)
    checkout_handler = CommandHandler(
        'checkout', checkout, filters=yogitrismayana)

    # add handler to dispatcher
    dispatcher = updater.dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(stop_handler)
    dispatcher.add_handler(checkin_handler)
    dispatcher.add_handler(checkout_handler)

    # start the bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
