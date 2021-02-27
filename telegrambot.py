#!/usr/bin/env pipenv-shebang
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters)


class TelegramBot:

    def updater(self):
        # horirevens_bot = '1565394227:AAHkdcB1fwKau0ywu2VdtDVgoNaQX2-nQ80'
        # presensi_bot = '1527700084:AAExPWkJoqWuc-L--Ix-sNE6QFSB1DoKOFY'
        return Updater(token='1527700084:AAExPWkJoqWuc-L--Ix-sNE6QFSB1DoKOFY', use_context=True)

    def send_message(self, chat_id='159508674', text='...', parse_mode=None):
        """send message to client"""
        self.updater().bot.send_message(
            chat_id=chat_id, text=text, parse_mode=parse_mode)

    def run(self):
        """run telegram bot"""
        self.updater().start_polling()
        self.updater().idle()


if __name__ == '__main__':
    bot = TelegramBot()
    bot.run()
