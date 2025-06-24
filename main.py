import os
import time
import random
from datetime import datetime
from typing import List

import discord
from discord.ext import commands

from Subscription import Subscription
from User import User
from DatabaseConnector import DatabaseConnector

# Bot Permissions: 1126295044094016
token = os.getenv('API_TOKEN')

allgemein_channel_id = 1343316928457871394
test_channel_id = 1343693012382908539

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


async def send_message():
    message = bot.get_channel(test_channel_id)

    await message.send("This is a Test {time}".format(time=datetime.now()))


@bot.command()
async def available_subscriptions(message):
    await message.send("Available Topic to listen on::\n- {}".format("\n- ".join(map(lambda s: s.get_name(), available_subscriptions))))


@bot.command()
async def subscriptions(message):
    for s in available_subscriptions:
        for u in s.get_users():
            if get_current_user_id(message) == u.get_discord_id():
                await message.send("{}".format(s.get_name()))


@bot.command()
async def notify(message, subscription_name):
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


@bot.command()
async def stop_loop(message):
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
    message = bot.get_channel(allgemein_channel_id)
    if check_member(member.id):
        available_members.append(User(member.id, member.display_name))
        await message.send(f"Welcome {member.display_name}")
    else:
        await message.send(f"Welcome back: {member.display_name}")

    print("Available Users: {}".format(available_members))


@bot.event
async def on_ready():
    global available_members
    global available_subscriptions
    available_members = []
    available_subscriptions = []

    print("Ready!")

    all_members = get_members_as_list()
    # Fill available members with empty subscriptions. Subscriptions will not be persisted
    for member in all_members:
        available_members.append(User(member.id, member.display_name))

    print("Available Users: {}".format(available_members))

    available_subscriptions.append(Subscription("TestSubscription1", bot, allgemein_channel_id, []))
    available_subscriptions.append(Subscription("TestSubscription2", bot, allgemein_channel_id, []))
    available_subscriptions.append(Subscription("TestSubscription3", bot, allgemein_channel_id, []))

    db_connector = DatabaseConnector()
    db_connector.connect()
    cursor = db_connector.get_cursor()
    query_response = db_connector.execute_query("SELECT message FROM logs WHERE level=5", cursor)
    print(query_response)

    while loop_run:
        await available_subscriptions[random.randint(0, 2)].notify(db_connector.execute_query("SELECT message FROM logs WHERE level=5", cursor))
        time.sleep(random.randint(1, 5))


bot.run(token)
