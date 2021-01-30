#!/usr/bin/env pipenv-shebang
from telegram.ext import Updater


class PythonTelegramBot:
    def __init__(self):
        self.updater = Updater(
            token='1527700084:AAExPWkJoqWuc-L--Ix-sNE6QFSB1DoKOFY',
            use_context=True)
        self.dispatcher = self.updater.dispatcher

    def send_message(self, pchat_id=159508674, ptext='...?'):
        """
        :param pchat_id: 159508674
        :param ptext: 'Hello world'
        send message to client
        """
        self.updater.bot.send_message(chat_id=pchat_id, text=ptext)


if __name__ == '__main__':
    bot = PythonTelegramBot()
    bot.updater.start_polling()
    bot.updater.idle()
