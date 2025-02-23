import os
import discord
from discord.ext import commands

# Bot Permissions: 1126295044094016

print(discord.__version__)

token = os.environ['API_TOKEN']

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


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def stats(ctx):
    member_name_list = get_members_name_as_list()
    print(member_name_list)

    for member in get_members_as_list():
        await ctx.send("Stats for {glb_name} aka {lcl_name}: \n\tID: {id}\n\tJOINED: {joined}"
                        .format(glb_name=member.global_name, lcl_name=member.display_name, id=member.id, joined=member.joined_at))


bot.run(token)
