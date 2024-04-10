from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

#Step 0: load our token from somewhere safe
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
#print (TOKEN)

#Step 1: BOT SETUP Without intents your bot won't respond
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
client: Client = Client(intents=intents)

#Step 2: Message Function
async def send_message(message: Message,user_message: str) -> None:
    if not user_message:
        print('(Message was empty becuase intents were not enabled...prob)')
        return
#check to see if you need to resopnd to private messages
    if is_private := user_message[0] =='?':
        user_message = user_message[1:]

    try:
        response: str= get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

#Step 3: Handle the startup of the bot
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

#Step 4:  Let's handle the messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user: #The bot wrote the message, or the bot talks to itself
        return

    username: str= str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

#Step 5 Main Starting point

def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()
