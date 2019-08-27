from twilio.rest import Client
import env


class text_msg:
    account_sid = env.account_sid
    auth_token = env.auth_token
    client = Client(account_sid, auth_token)

    def __init__(self, num):
        self.num = num

    def msg(self, err):
        message = text_msg.client.messages \
            .create(
                body="Error occurred during check: {err}".format(err=err),
                from_='+12173885711',
                to='+82' + self.num[1:]
            )
        message.sid
