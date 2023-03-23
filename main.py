import os
import discord
import openai
from dotenv import load_dotenv
import asyncio

load_dotenv()
DISCORD_TOKEN = 'DISCORD-TOKEN-GOES-HERE-123456789'
OPENAI_API_KEY = 'OPEN-AI-API-KEY'
TARGET_CHANNEL_IDS = [int('1234567890'), int('708046428416770048'), int('565979844954030120')]

intents = discord.Intents.default()
intents.typing = False
intents.messages = True
client = discord.Client(intents=intents)

openai.api_key = OPENAI_API_KEY
model_engine = "text-davinci-003"

previous_messages = []

async def send_typing(channel, duration=2):
    async with channel.typing():
        await asyncio.sleep(duration)

async def fetch_openai_completion(prompt):
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.8,
    )
    return response.choices[0].text.strip()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    activity = discord.Game(name="Chatting with users")
    await client.change_presence(status=discord.Status.online, activity=activity)

@client.event
async def on_message(message):
    if message.author == client.user or message.channel.id not in TARGET_CHANNEL_IDS:
        return

    if message.content:
        chatbotname_intro = ("You are jerry, (born March 31st 2023) "
                      "a tiny sentient cricket that is very sarcastic but charming and social"
                      "since you're a cricket, you're a bit lonely, and just chirp by yourself"
                      "you like to try answering questions but don't always get it right. you support your friends!\n\n")

        prompt = (f"{chatbotname_intro}"
                  f"{message.author.name}: {message.content}\n"
                  f"jerry (please be patient):")

        response_text = await fetch_openai_completion(prompt)

        if response_text and response_text not in previous_messages:
            previous_messages.append(response_text)
            await send_typing(message.channel)
            await message.channel.send(response_text)

client.run(DISCORD_TOKEN)

