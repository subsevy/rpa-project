import telegram
import env


class telegram_msg:
    my_token = env.token
    bot = telegram.Bot(token=my_token)

    def __init__(self, chat_id):
        self.chat_id = chat_id

    def msg(self, err):
        telegram_msg.bot.sendMessage(
            chat_id=self.chat_id, text="Error occurred during check: {err}".format(err=err))
