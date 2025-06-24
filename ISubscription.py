from abc import ABC, abstractmethod
from User import User
from discord.ext.commands import Bot


class ISubscription(ABC):

    @abstractmethod
    def __init__(self, name: str, bot: Bot, channel_id: int, users: list = []):
        self.name =  name
        self.bot = bot
        self.channel_id = channel_id
        self.users = users

    @abstractmethod
    def add_user(self, user: User) -> None:
        pass

    @abstractmethod
    def remove_user(self, user: User) -> None:
        pass

    @abstractmethod
    def get_subscription_id(self):
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_users(self) -> list:
        pass
