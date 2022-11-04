# import discord


# TOKEN = "MTAzNzgyNzY1MDE2NjcyMjU4MQ.G0H7N2.h5Ns4x1ktDAY06vNXdCJM3rX28P-NTwoMJl9Yc"

# CALL = '!SHIT '
# intents = discord.Intents.default()
# intents.messages = True
# client = discord.Client(intents=intents)
# # client = discord.Client()


# @client.event
# async def on_ready():
#     print("i've started, big dick energy")
#     print("Logged in as {0.user}".format(client))


# # @client.event
# # async def on_message(message):
# #     if message.author == client.user:
# #         return

# #     if message.content == 'hello':
# #         response = "i'm alive"
# #         await message.channel.send(response)
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     username = str(message.author).split('#')[0]
#     user_message = str(message.content)
#     channel = str(message.channel.name)
#     print(
#         username + ";" +
#         user_message + ";" +
#         channel + ";"
#     )
#     print(message)

#     if user_message.lower() == 'hello':
#         await message.channel.send(f'hello {username}')
#         return

#     # brooklyn_99_quotes = [
#     #     'I\'m the human form of the 💯 emoji.',
#     #     'Bingpot!',
#     #     (
#     #         'Cool. Cool cool cool cool cool cool cool, '
#     #         'no doubt no doubt no doubt no doubt.'
#     #     ),
#     # ]

#     # if message.content == '99!':
#     #     response = brooklyn_99_quotes[0]
#     #     await message.channel.send(response)

# client.run(TOKEN)

import discord
import responses


async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)


def run_discord_bot():
    print(discord.__version__)

    TOKEN = 'MTAzNzgyNzY1MDE2NjcyMjU4MQ.G0H7N2.h5Ns4x1ktDAY06vNXdCJM3rX28P-NTwoMJl9Yc'
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    client.run(TOKEN)


if __name__ == '__main__':
    run_discord_bot()
