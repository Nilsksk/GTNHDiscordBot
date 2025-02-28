from Subscription import Subscriptions, Subscription


class User:
    def __init__(self, discord_id: int, name: str, subscriptions: Subscriptions = None) -> None:
        self.__discord_id = discord_id
        self.__name = name
        self.subscriptions = subscriptions

    def get_discord_id(self):
        return self.__discord_id

    def get_name(self):
        return self.__name

    def get_subscriptions(self):
        return self.subscriptions

    def __repr__(self) -> str:
        if self.subscriptions is None:
            return str(self.__discord_id) + " " + self.__name + " "
        else:
            return str(self.__discord_id) + " " + self.__name + " " + str(self.subscriptions.get())
