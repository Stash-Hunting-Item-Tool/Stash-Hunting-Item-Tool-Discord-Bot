import discord
import responses_read
import responses_file


async def send_message(message, user_message, is_private):
    try:
        response = responses_read.get_response(user_message)
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
            if "addFile" in user_message:
                await message.channel.send(responses_file.add_file_to_db(
                    message, user_message, message.attachments[0].url))
            else:
                await send_message(message, user_message, is_private=False)

    client.run(TOKEN)


if __name__ == '__main__':
    run_discord_bot()
