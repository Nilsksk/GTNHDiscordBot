from uuid import uuid4
from datetime import datetime
from ISubscription import ISubscription, Bot, User


class Subscription(ISubscription):
    def __init__(self, name: str, bot: Bot, channel_id: int, users: list = []):
        self.subscription_id = uuid4()
        self.bot = bot
        self.name = name
        self.channel_id = channel_id
        self.channel = self.bot.get_channel(self.channel_id)
        self.users = users

    async def notify(self, message: str):
        await self.channel.send("[{time}][{sub_name}]\n<@{user}>\n{msg}".format(msg=message, time=datetime.now(), sub_name=self.name, user="> <@".join(map(lambda user: str(user.get_discord_id()), self.users))))

    def add_user(self, user: User) -> None:
        """
        Will add a User to the users list, so it gets notified on a new message
        :param user: User that should be added/notified
        :return: None
        """
        self.users.append(user)

    def remove_user(self, user: User) -> None:
        """
        Will remove a given user from the users list
        :param user: User that should be removed/de-notified
        :return:
        """
        self.users.remove(user)

    def get_subscription_id(self):
        return self.subscription_id

    def get_name(self) -> str:
        return self.name

    def get_users(self) -> list:
        return self.users

    def get_channel_id(self) -> int:
        return self.channel_id

    def __repr__(self):
        return "(" + self.get_name() + ", " + str(self.get_channel_id()) + ")"

