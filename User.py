class User:
    def __init__(self, discord_id: int, name: str) -> None:
        self.__discord_id = discord_id
        self.__name = name

    def get_discord_id(self):
        return self.__discord_id

    def get_name(self):
        return self.__name

    def __repr__(self) -> str:
        return str(self.__discord_id) + " " + self.__name
