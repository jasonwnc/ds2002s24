from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from random import choice, randint
import openai
import json

#Don't forget to istall pip install openai==0.28
#Configure OpenAI API Key
openai.api_key = 'see assignment for keys'
TOKEN = "your token"

#Step 1: BOT SETUP Without intents your bot won't respond
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
client: Client = Client(intents=intents)

def ask_openai(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Choose the model you prefer
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ]
    )
    answer = response['choices'][0]['message']['content']
    return answer

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return 'Well, you are quiet'
    elif 'hello' in lowered:
        return 'Hello there! You need to code your AI Bot here'
    elif 'roll dice' in lowered:
        return f'You rolled a {randint(1, 6)}'
    elif 'help' in lowered:
        return f'you can say !data, !temp, or !pressure'
    else:
        return ask_openai(user_input)


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
