
class Subscription:
    def __init__(self, subscription_id: int, name: str) -> None:
        self.__subscription_id = subscription_id
        self.__name = name

    def get_id(self) -> int:
        return self.__subscription_id

    def get_name(self) -> str:
        return self.__name

    def __repr__(self) -> str:
        return str(self.__subscription_id) + " " + self.__name


class Subscriptions:
    def __init__(self, subscriptions: [Subscription] = None) -> None:
        if subscriptions is None:
            self.__subscriptions = []
        else:
            self.__subscriptions = subscriptions

    def add(self, subscription: Subscription) -> None:
        self.__subscriptions.append(subscription)

    def remove(self, subscription) -> None:
        for elem in self.__subscriptions:
            if elem.get_id() == subscription.get_id() and elem.get_name() == subscription.get_name():
                self.__subscriptions.remove(subscription)

    def get(self) -> [Subscription]:
        return self.__subscriptions

