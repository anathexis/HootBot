# imports from other modules
from dice_cast import Cast
from sentence_generator import SentenceGenerator, TextFileSentenceGenerator
from pathlib import Path
import random
from scipy.stats import logistic

# imports of the discord libs
import discord
from discord.ext import commands

# To get env vars
from dotenv import load_dotenv
load_dotenv()

import os

# To be able to give the bot access to members and messages
intents = discord.Intents.default()
intents.members = True
intents.messages = True

# Initialization of bot
hoot_bot = commands.Bot(command_prefix='!!', intents=intents)
sentence_gen_file_location = Path('sentence_files', 'base_sentence.gen')
sentence_gen = TextFileSentenceGenerator(sentence_gen_file_location)

# React to 🧊: send a random sentence and add a dice throw
@hoot_bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    
    channel = discord.utils.get(hoot_bot.get_all_channels(), id=payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    adding_member = payload.member.display_name
    # Because HootBot not answering itself
    if message.author == hoot_bot.user:
        return
    
    if str(payload.emoji) == '🧊':
        author_mention = message.author.mention
        sentence = sentence_gen.draw_sentence(message.content)
        cast = Cast.get_random_cast()
        san_loss = f'You loose {cast.get_thrown_sum()} ({str(cast)}) points of SAN.'
        courtesy = f'Courtesy of {adding_member}.'

        msg = f'{author_mention}, {sentence} {san_loss} {courtesy}'
        await message.reply(msg)
    return

@hoot_bot.event
async def on_disconnect():
    private_channel = discord.utils.get()

@hoot_bot.command()
async def roll(ctx, ndn_dice_string: str):
    try:
        cast = Cast.get_cast_from_ndn_string(ndn_dice_string)
    except ValueError:
        await ctx.send('Bad format, should be ndn, eg: 4d6')

    await ctx.send(f'Result for {ndn_dice_string}: {cast.get_thrown_sum()} ({", ".join(map(str, cast.current_throw))})')

@hoot_bot.command()
async def target_san(ctx, ndn_dice_string: str):
    if ctx.message.reference is not None:
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    else:
        await ctx.send("No target, please reply to a message to target a loss of SAN.")
        
    sender = message.author.mention

    command_list = ndn_dice_string.split()

    try:
        cast = Cast.get_cast_from_ndn_string(command_list[0])
    except ValueError:
        await ctx.send('Bad format, should be ndn, eg: 4d6') 

    sentence = ''
    
    # In order to prevent abuse in using the hoot-bot target_san function.
    if cast.bounds[1] > 1000 and random.random() < logistic.cdf(cast.bounds[1], 2000, 500):
        sentence = f'{ctx.author.mention}, abusing the hoot-bot (well, actually, me), make you loose {cast.get_thrown_sum()}. You know why.'
    else:
        justification = '.'
        if len(command_list) > 1:
            justification = ', ' + ' '.join(command_list[1:])
        sentence = f'{sender}, you loose {cast.get_thrown_sum()} ({ndn_dice_string}) points of SAN. Courtesy of {ctx.author.display_name}{justification}'

    await ctx.send(sentence)


@hoot_bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) and "ndn_dice_string is a required argument that is missing" in str(error):
        await ctx.send("You're missing a required argument: the dice to be thrown.")
    if isinstance(error, commands.CommandInvokeError) and "message_id" in str(error):
        await ctx.send("No target, please reply to a message to target a loss of SAN.")

hoot_bot.run(os.getenv('DISCORD_TOKEN'))




    
