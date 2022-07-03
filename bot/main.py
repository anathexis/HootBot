# imports from other modules
from dice_cast import Cast
from sentence_generator import SentenceGenerator, TextFileSentenceGenerator
from pathlib import Path

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
    if ctx.message.reference is None:
        await ctx.send('No target, please reply to a message to target a loss of SAN.')

    message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    
    sender = message.author.mention

    try:
        cast = Cast.get_cast_from_ndn_string(ndn_dice_string)
    except ValueError:
        await ctx.send('Bad format, should be ndn, eg: 4d6') 

    await ctx.send(f'{sender}, you loose {cast.get_thrown_sum()} ({ndn_dice_string}) points of SAN. Courtesy of {ctx.author.display_name}.')

hoot_bot.run(os.getenv('DISCORD_TOKEN'))



    
