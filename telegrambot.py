from telegram.ext import Updater


class TelegramBot:
    def __init__(self):
        self.updater = Updater(
            token='1565394227:AAHkdcB1fwKau0ywu2VdtDVgoNaQX2-nQ80',
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
    bot = TelegramBot()
    bot.updater.start_polling()
    bot.updater.idle()
