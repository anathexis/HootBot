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

# Display lexicon of emojis used on the server and their meaning - based on Pyrope's original message
@hoot_bot.command(name='lexicon', help='Display legend of the different emojis used around the Hoot server.')
async def display_help(ctx):
    gen_channel = ctx.guild.get_channel(847457155220242434)
    lex_msg = await gen_channel.fetch_message(847535432488452188)
    await ctx.channel.send(lex_msg.content)

@hoot_bot.event
async def on_disconnect():
    private_channel = discord.utils.get()


hoot_bot.run(os.getenv('DISCORD_TOKEN'))



    