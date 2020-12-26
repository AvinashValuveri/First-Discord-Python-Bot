import discord
import requests
import json
import random
from replit import db
from discord.ext import commands



bad_words = ["Bad Word1" "Bad Word2" "Bad Word3" "Bad Word4"]

stop_that = ["That's not nice", "Please stop using those words", "That's mean", "Please be nicer"]


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)


def update_banned(banned_message):
  if "banned" in db.keys():
    banned = db["banned"]
    banned.append(banned_message)
    db["encouragements"] = banned
  else:
    db["banned"] = [banned_message]


def delete_banned(index):
  banned = db["banned"]
  if len(banned) > index:
    del banned[index]
    db["banned"] = banned

client = commands.Bot(command_prefix = "$")

@client.command()
async def ping(ctx):
  await ctx.send(f'Pong! {round{client.latency * 1000}}ms')



@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))






@client.event
async def on_message(message):
  if message.author == client.user:
    return

  
  
  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')
  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)
  if message.content == '$pingme':
    await message.channel.send('Pinging {}'.format(message.author.mention))
  options = stop_that
  if "banned" in db.keys():
    options = options + db["banned"]

  if any(word in message.content for word in bad_words):
    await message.channel.send(random.choice(options))

  if message.content.startswith("$newphrase "):
    banned_message = message.content.split("$newphrase ",1)[1]
    update_banned(banned_message)
    await message.channel.send("New warning phrase added.")

  if message.content.startswith("$delphrase"):
    banned = []
    if "banned" in db.keys():
      index = int(message.content.split("$delphrase",1)[1])
      delete_banned(index)
      banned = db["banned"]
    await message.channel.send(banned)


client.run(TOKEN)
