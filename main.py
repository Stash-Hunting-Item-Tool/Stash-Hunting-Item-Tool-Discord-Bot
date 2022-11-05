import discord
import responses_read
import responses_file
import config


async def send_message(message, user_message, is_private, user: str):
    try:
        response = responses_read.get_response(user_message, user)
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

        if user_message.split(" ")[0] == config.PREFIX:
            print(user_message)
            user_message = user_message.removeprefix(config.PREFIX).strip()
            print(user_message)
            if not (username in config.ALLOWED_USERNAMES):
                print(username + " tried and had no access")
                await message.channel.send(username + " tried and had no access")
            elif not (channel in config.ALLOWED_CHANNELS):
                print(f"wrong channel used user {username} tried {channel}")
                await message.channel.send(
                    f"wrong channel used user {username} tried {channel}")
            else:
                print(f'{username} said: "{user_message}" ({channel})')

                if user_message[0] == '?':
                    user_message = user_message[1:]
                    await send_message(message, user_message, is_private=True, user=username)
                else:
                    if "addFile" in user_message:
                        await message.channel.send(responses_file.add_file_to_db(
                            message, user_message, message.attachments[0].url))
                    else:
                        await send_message(message, user_message, is_private=False, user=username)

    client.run(TOKEN)


if __name__ == '__main__':
    run_discord_bot()
