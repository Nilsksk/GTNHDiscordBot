import asyncio
import os
import time

import discord
from discord.ext import commands

from Subscription import Subscription
from User import User
from DatabaseConnector import DatabaseConnector

from dotenv import load_dotenv
load_dotenv()

# Bot Permissions: 1126295044094016
token = os.getenv('API_TOKEN')

info_channel_id = int(os.getenv('BOTS_INFO'))
urgent_channel_id = int(os.getenv('BOTS_URGENT'))
notify_interval = int(os.getenv('NOTIFY_INTERVAL'))

loop_run = True
available_members = []
available_subscriptions = []

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


def get_members():
    for elem in bot.get_all_members():
        print(elem)


def get_members_as_list():
    members = []
    for member in bot.get_all_members():
        members.append(member)

    return members


def get_members_name_as_list():
    name_list = []
    for member in bot.get_all_members():
        name_list.append(member.name)

    return name_list


def get_channels():
    for elem in bot.get_all_channels():
        print(elem)


def get_current_user_id(message):
    return message.author.id


def get_current_user_display_name(message):
    return message.author.display_name


def get_user_by_id(id):
    for local_user in available_members:
        if local_user.get_discord_id() == id:
            return local_user


def update_user(user_to_update: User):
    for user in available_members:
        if user.get_discord_id() == user_to_update.get_discord_id():
            available_members.remove(user)
            break
    available_members.append(user_to_update)
    print(available_members)


def info_filter(channel):
    if channel.get_channel_id() == info_channel_id:
        return True
    else:
        return False


def urgent_filter(channel):
    if channel.get_channel_id() == urgent_channel_id:
        return True
    else:
        return False


@bot.command()
async def available_subscriptions(message):
    """
    Prints all available Subscriptions
    """
    current_channel = message.channel.id
    if current_channel == info_channel_id:
        await message.send("Available Topic to listen on:\n- {}".format("\n- ".join(map(lambda s: s.get_name(), filter(info_filter, available_subscriptions)))))
    elif current_channel == urgent_channel_id:
        await message.send("Available Topic to listen on:\n- {}".format("\n- ".join(map(lambda s: s.get_name(), filter(urgent_filter, available_subscriptions)))))
    else:
        return


@bot.command()
async def subscriptions(message):
    """
    Prints the current subscribed Subscriptions
    """
    current_channel = message.channel.id
    if current_channel == info_channel_id or current_channel == urgent_channel_id:
        for s in available_subscriptions:
            for u in s.get_users():
                if get_current_user_id(message) == u.get_discord_id():
                    await message.send("{}".format(s.get_name()))
    else:
        return


@bot.command()
async def notify(message, subscription_name = commands.parameter(description="Name of the Subscription you want to get notified of")):
    """
    Command to notify on a given Subscription
    """
    current_channel = message.channel.id
    if current_channel == info_channel_id or current_channel == urgent_channel_id:
        count = 0
        for s in available_subscriptions:
            if s.get_name() == subscription_name:
                for usr in available_members:
                    if (usr.get_discord_id() == get_current_user_id(message)) and (usr not in s.get_users()):
                        s.add_user(usr)
                        count = count + 1
                        await message.send("<@{user}> subscribed on {subscription}".format(user=get_current_user_id(message), subscription=s.get_name()))

                if count == 0:
                    await message.send("Already subscribed on {subscription}".format(subscription=s.get_name()))
    else:
        return


@bot.command()
async def unnotify(message, subscription_name = commands.parameter(description="Name of the Subscription you want to unnotify from")):
    """
    Command to unnotify from a given Subscription
    """
    current_channel = message.channel.id
    if current_channel == info_channel_id or current_channel == urgent_channel_id:
        count = 0
        for s in available_subscriptions:
            if s.get_name() == subscription_name:
                for usr in available_members:
                    if (usr.get_discord_id() == get_current_user_id(message)) and (usr in s.get_users()):
                        s.remove_user(usr)
                        count = count + 1
                        await message.send("<@{user}> unsubscribed on {subscription}".format(user=get_current_user_id(message), subscription=s.get_name()))

                if count == 0:
                    await message.send("Already unsubscribed on {subscription}".format(subscription=s.get_name()))
    else:
        return


@bot.command()
async def stop_loop(message):
    """
    Stops the whole notifying! (DO NOT USE)
    """
    global loop_run
    loop_run = False
    print("Stopping notify loop!")


def check_member(member_id: int):
    for member in available_members:
        if member.get_discord_id() == member_id:
            return False
    return True


@bot.event
async def on_member_join(member):
    # message = bot.get_channel(bots_info_channel_id)
    if check_member(member.id):
        available_members.append(User(member.id, member.display_name))
        # await message.send(f"Welcome {member.display_name}")
    else:
        # await message.send(f"Welcome back: {member.display_name}")
        return

    print("Available Users: {}".format(available_members))


async def notify_info_thread(subscription, query):
    db_connector = DatabaseConnector()
    db_connector.connect()
    cursor = db_connector.get_cursor()
    query_response = db_connector.execute_query(query, cursor)

    await subscription.notify(query_response)

    time.sleep(2)


async def notify_helper(subscription, query):
    db_connector = DatabaseConnector()
    db_connector.connect()
    cursor = db_connector.get_cursor()
    query_response = db_connector.execute_query(query, cursor)

    if subscription.get_channel_id() == urgent_channel_id:
        await subscription.notify(query_response)
    elif subscription.get_channel_id() == info_channel_id:
        await subscription.notify(query_response)
    else:
        return

    await asyncio.sleep(notify_interval)


@bot.event
async def on_ready():
    global available_members
    global available_subscriptions
    available_members = []
    available_subscriptions = []

    all_members = get_members_as_list()
    for member in all_members:
        available_members.append(User(member.id, member.display_name))

    print("Available Users: {}".format(available_members))

    s1 = Subscription("All-Items", bot, info_channel_id, [])
    available_subscriptions.append(s1)
    #s2 = Subscription("TestSubscription2", bot, urgent_channel_id, [])
    #available_subscriptions.append(s2)
    #s3 = Subscription("TestSubscription3", bot, info_channel_id, [])
    #available_subscriptions.append(s3)
    print("Available Subscriptions: {}".format(available_subscriptions))

    print("Ready!")

    while loop_run:
        await asyncio.gather(
            notify_helper(s1,
                          "WITH data AS (SELECT client_metadata.location, item_stockpiles.time time, item_ids.name, item_stockpiles.amount, ROW_NUMBER() OVER(PARTITION BY item_stockpiles.item_id ORDER BY item_stockpiles.time DESC) AS rowindex from item_stockpiles INNER JOIN client_metadata ON item_stockpiles.client_ids = client_metadata.id INNER JOIN item_ids ON item_stockpiles.item_id = item_ids.id) SELECT * FROM data WHERE rowindex = 1;"),
            #notify_helper(s2,
            #              "select client_metadata.location, max(item_stockpiles.time) time, item_ids.name, item_stockpiles.amount from item_stockpiles inner join client_metadata on item_stockpiles.client_ids = client_metadata.id inner join item_ids on item_stockpiles.item_id = item_ids.id GROUP BY item_stockpiles.item_id ORDER BY item_stockpiles.id DESC;"),
            #notify_helper(s3,
            #              "select client_metadata.location, max(item_stockpiles.time) time, item_ids.name, item_stockpiles.amount from item_stockpiles inner join client_metadata on item_stockpiles.client_ids = client_metadata.id inner join item_ids on item_stockpiles.item_id = item_ids.id GROUP BY item_stockpiles.item_id ORDER BY item_stockpiles.id DESC;")
        )

bot.run(token)
