# imports from other modules
from typing import Optional
from unicodedata import numeric
from dice_cast import Cast, Throw
from sentence_generator import SentenceGenerator, TextFileSentenceGenerator
from pathlib import Path
import random
from scipy.stats import logistic
from emoji_source import all_emojis
import re

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
        await message.reply('Nice try, but as the HootBot, the puppet master of this server, I am immune to loss of SAN')
        return 
    
    if str(payload.emoji) == '🧊':
        author_mention = message.author.mention
        sentence = sentence_gen.draw_sentence(message.content)
        cast = Cast.get_random_cast()
        san_loss = f'You loose {cast.throw().result_sum} ({str(cast)}) points of SAN.'
        courtesy = f'Courtesy of {adding_member}.'

        msg = f'{author_mention}, {sentence} {san_loss} {courtesy}'
        await message.reply(msg)
    return

@hoot_bot.event
async def on_disconnect():
    private_channel = discord.utils.get()

@hoot_bot.event
async def on_message(message):
    if re.match('^HootBot.*\?$', message.content) is not None:
        number = re.search('\d+', message.content)
        if number is not None:
            number = number.group(0)
        else: 
            number = 1

        emoji_cast = random.choices(population=all_emojis, k=int(number))

        await message.reply(''.join(emoji_cast))
        if '🧊' in emoji_cast:
            await message.add_reaction('🧊')
    await hoot_bot.process_commands(message)

        

@hoot_bot.command()
async def roll(ctx, ndn_dice_string: str):
    try:
        cast = Cast.get_cast_from_ndn_string(ndn_dice_string)
    except ValueError:
        await ctx.send('Bad format, should be ndn, eg: 4d6')
    
    throw = cast.throw()

    await ctx.send(f'Result for {ndn_dice_string}: {throw.result_sum} ({", ".join(map(str, throw.values))})')

@hoot_bot.command()
async def divine(ctx, number_text: str = '1'):
    try:
        number = int(number_text)
    except ValueError:
        await ctx.send('Bad format, should be an integer')

    emoji_cast = random.choices(population=all_emojis, k=number)

    if '🧊' in emoji_cast:
        await ctx.message.add_reaction('🧊')

    await ctx.send(''.join(emoji_cast))

@hoot_bot.command()
async def target_san(ctx, ndn_dice_string: str):
    if ctx.message.reference is not None:
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    else:
        await ctx.send("No target, please reply to a message to target a loss of SAN.")
        return
        
    sender = message.author.mention

    try:
        cast = Cast.get_cast_from_ndn_string(ndn_dice_string)
    except ValueError:
        await ctx.send('Bad format, should be ndn, eg: 4d6') 

    sentence = ''
    
    if message.author == hoot_bot.user:
        sentence = 'Nice try, but as the HootBot, the puppet master of this server, I am immune to loss of SAN'

    throw = cast.throw()
    
    # In order to prevent abuse in using the hoot-bot target_san
    if cast.bounds[1] > 1000 and random.random() < logistic.cdf(cast.bounds[1], 2000, 500):
        sentence = f'{ctx.author.mention}, abusing the hoot-bot (well, actually, me), make you loose {throw.result_sum} ({ndn_dice_string}) points of SAN. You know why.'
    else:
        sentence = f'{sender}, you loose {throw.result_sum} ({ndn_dice_string}) points of SAN. Courtesy of {ctx.author.display_name}.'
    
    if message.author == hoot_bot.user:
        sentence = 'Nice try, but as the HootBot, the puppet master of this server, I am immune to loss of SAN'

    await ctx.send(sentence)


@hoot_bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) and "ndn_dice_string is a required argument that is missing" in str(error):
        await ctx.send("You're missing a required argument: the dice to be thrown.")
    if isinstance(error, commands.CommandInvokeError) and "message_id" in str(error):
        await ctx.send("No target, please reply to a message to target a loss of SAN.")

hoot_bot.run(os.getenv('DISCORD_TOKEN'))




    
