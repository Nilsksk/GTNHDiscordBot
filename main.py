import os
import time
from datetime import datetime
import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from Subscription import Subscription, Subscriptions
from User import User

# Bot Permissions: 1126295044094016
token = os.environ['API_TOKEN']

allgemein_channel_id = 1343316928457871394
test_channel_id = 1343693012382908539

loop_run = False
available_members = []

s1 = Subscription(1, "Test_1")
s2 = Subscription(2, "Test_2")
s3 = Subscription(3, "Test_3")

sl_tmp = Subscriptions()
sl = Subscriptions()
sl.add(s1)
sl.add(s2)
sl.add(s3)

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


def get_subscription_by_topic(topic):
    for subscription in sl.get():
        if subscription.get_name() == topic:
            return subscription


def update_user(user_to_update: User):
    for user in available_members:
        if user.get_discord_id() == user_to_update.get_discord_id():
            available_members.remove(user)
            break
    available_members.append(user_to_update)
    print(available_members)


def add_new_subscription(message, topic, subs):
    for subscription in sl.get():
        if subscription.get_name() == topic:
            update_user(User(get_current_user_id(message), get_current_user_display_name(message), subs))
            break


@bot.command()
async def available_topics(message):
    await message.send("Available Topic to listen on:\n- {}".format("\n- ".join(map(lambda s: s.get_name(), sl.get()))))


@bot.command()
async def notify(message, topic):
    global sl_tmp

    sub_by_topic = get_subscription_by_topic(topic)
    if (sub_by_topic not in sl_tmp.get()) and (sub_by_topic is not None):
        sl_tmp.add(sub_by_topic)
        add_new_subscription(message, topic, sl_tmp)
        await message.send("<@{user}> subscribed on {topic}".format(user=get_current_user_id(message), topic=topic))
    else:
        if sub_by_topic in sl_tmp.get():
            await message.send("Already subscribed on topic with name: {topic}".format(topic=topic))
        else:
            await message.send("Couldn't subscribe on topic with name: {topic}".format(topic=topic))


@bot.command()
async def subscriptions(message):
    current_user = get_user_by_id(get_current_user_id(message))
    message = bot.get_channel(test_channel_id)
    current_user_subscriptions = current_user.get_subscriptions()

    if current_user_subscriptions is not None:
        await message.send("You are subscribed to:\n- {}".format("\n- ".join(map(lambda s: s.get_name(), current_user_subscriptions.get()))))
    else:
        await message.send("You are not subscribed to any topics!")


async def send_message():
    message = bot.get_channel(test_channel_id)

    await message.send("This is a Test {time}".format(time=datetime.now()))


@bot.command()
async def stop_loop(message):
    global loop_run
    loop_run = False


@bot.event
async def on_ready():
    global available_members
    available_members = []

    print("Ready!")

    all_members = get_members_as_list()
    # Fill available members with empty subscriptions. Subscriptions will not be persisted
    for member in all_members:
        available_members.append(User(member.id, member.display_name, None))

    print("Available Users: {}".format(available_members))

    while loop_run:
        await send_message()
        time.sleep(1)


bot.run(token)
