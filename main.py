import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

bad_words = ["sad", "depressed", "unhappy", "angry", "fml", "miserable", "i can't", "shit", "fuck", "school", "busy", "work", "stress", "gl", "good luck"]

starter_encouragements = ["bulbul", "three pcs", "blow on your mothercard", "lolo mo.", "rockyun foundation", "coomer", "are you listen", "crazy malignant", "why are you gey", "should I call you mista?", "wrong hole", "half a feg"]

good_night = ["good night", "gn", "noot noot", "gg", "ggs", "GG", "GGs"]

good_night_greeting = ["gn! ^^/", "NOOT NOOT!!", "hehe", "Should I call you mista?"]

good_morning = ["wassup", "hi", "h3llo", "henlo", "hewo", "heewo", "hello"]

greeting = ["WASSSUP", "lolo mo wassup", "wrong hole", "heewo!", ":3"]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
  db["encouragements"] = encouragements

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  options = starter_encouragements
  if "encouragements" in db.keys():
    options = options + db["encouragements"]

  if any(word in msg for word in bad_words):
    await message.channel.send(random.choice(options))

  if any(word in msg for word in good_night):
    await message.channel.send(random.choice(good_night_greeting))

  if any(word in msg for word in good_morning):
    await message.channel.send(random.choice(greeting))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragment(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
    
  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")

keep_alive()

client.run(os.getenv('TOKEN'))
