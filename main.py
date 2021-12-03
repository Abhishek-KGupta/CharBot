import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words=["sad","depressed","angry","alone","lonely","fail","failure","misrerable","frustated"]

starter_encouragement=["Cheer up!", "Hang in there!", "You can do it", "Be Confident", "Fight On", "Dattebayo", "You are a great person", " Love You <3"]

def update_encouragement(encouraging_message):
  if "encouragement" in db.keys():
    encouragement=db["encouragement"]
    encouragement.append(encouraging_message)
    db["encouragement"]=encouragement
  else:
    db["encouragement"]={encouraging_message}

def delete_encouragement(index):
  encouragement=db["encouragement"]
  if len(encouragement) > index:
    del encouragement[index]
    db["encouragement"]=encouragement

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data=json.loads(response.text)
  quote = json_data[0]['q']+" -"+json_data[0]['a']
  return(quote)


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author==client.user:
    return

  msg=message.content

  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')

  if message.content.startswith('$inspire')or(('motivate')in msg):
    q=get_quote()
    await message.channel.send(q)

  if message.content.startswith('$gaali'):
    await message.channel.send('teri maa ki choot')

  options = starter_encouragement
  if "encouragement" in db.keys():
    options=options+db["encouragement"]

  if any (word in msg for word in sad_words):
    await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message=msg.split("$new ",1)[1]
    update_encouragement(encouraging_message)
    await message.channel.send("New encouraging message added")

  if msg.startswith("$del"):
    encouragement=[]
    if "encouragement" in db.keys():
      index =int(msg.split("$del",1)[1])
      delete_encouragement(index)
      encouragement=db["encouragement"]
    await message.channel.send(encouragement)

  # if any (word in msg for word in sad_words):
  #   await message.channel.send(random.choice(starter_encouragement))

  if (('Thank you')in msg):
    await message.channel.send('You are Welcome')

keep_alive()
client.run(os.environ['TOKEN'])
