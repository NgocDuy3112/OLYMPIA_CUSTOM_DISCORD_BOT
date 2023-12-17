from __utils__ import *

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

vcnv_messages = {}  # Dictionary to store the last message from each source channel
tt_messages = {}  # Dictionary to store the first message from each source channel
hoi_suc_messages = {}
ping_messages = {}

HOI_SUC_KEY = "HOISUC"
HAS_PINGED = False

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    # Check if the message is from source channels
    if message.channel.id in SOURCE_CHANNEL_IDS:
        # Record the last message details (timestamp, content, channel object)
        vcnv_messages[message.channel.id] = {
            'content': message.content,
            'channel_name': message.channel.name
        }
        tt_messages[message.channel.id] = {
            'timestamp': message.created_at,
            'content': message.content,
            'channel_name': message.channel.name
        }
        hoi_suc_messages[message.channel.id] = {
            'content': message.content,
            'channel_name': message.channel.name
        }
        ping_messages[message.channel.id] = {
            'content': message.content,
            'channel_name': message.channel.name
        }

        if str.lower(vcnv_messages[message.channel.id]['content']) == "/cnv":
            channel_name = ' '.join(word.capitalize() for word in bot.get_channel(message.channel.id).name.split('-'))
            await bot.get_channel(DISPLAY_CHANNEL_ID).send(f"{channel_name} có tín hiệu trả lời Chướng ngại vật!")
        
        if hoi_suc_messages[message.channel.id]['content'] == HOI_SUC_KEY:
            channel_name = ' '.join(word.capitalize() for word in bot.get_channel(message.channel.id).name.split('-'))
            await bot.get_channel(DISPLAY_CHANNEL_ID).send(f"{channel_name} giải đúng Mã Hồi Sức!")
        
        if ping_messages[message.channel.id]['content'] == "/.":
            channel_name = ' '.join(word.capitalize() for word in bot.get_channel(message.channel.id).name.split('-'))
            await bot.get_channel(DISPLAY_CHANNEL_ID).send(f"{channel_name} giành quyền trả lời câu hỏi!")
            bot.remove_listener(on_message)


    # Check if the message is in the target channel and starts with '/start'
    elif message.channel.id == TARGET_CHANNEL_ID and message.content.startswith('/start'):
        start_time = datetime.now().astimezone()
        delay_seconds = int(message.content.split()[1])
        # Tang toc
        if delay_seconds in [20, 40]:
            try:
                # Extract the delay value from the message content
                await asyncio.sleep(delay_seconds)  # Wait for the specified delay
                await bot.get_channel(DISPLAY_CHANNEL_ID).send("HẾT THỜI GIAN!")
                sorted_messages = sorted(tt_messages.items(), key=lambda x: (x[1]['timestamp'] - start_time).total_seconds())

                for source_channel_id in SOURCE_CHANNEL_IDS:
                    await bot.get_channel(source_channel_id).send("HẾT THỜI GIAN!")

                for source_channel_id, last_message in sorted_messages:
                    timestamp = last_message['timestamp']
                    time_difference = (timestamp - start_time).total_seconds()
                    channel_name = ' '.join(word.capitalize() for word in last_message['channel_name'].split('-'))
                    await bot.get_channel(DISPLAY_CHANNEL_ID).send(
                        f"{channel_name} ({time_difference:.2f}s): {last_message['content'].upper()}"
                    )

                # Check if there's no message in a specific channel
                for source_channel_id in SOURCE_CHANNEL_IDS:
                    if source_channel_id not in tt_messages:
                        channel_name = ' '.join(word.capitalize() for word in bot.get_channel(source_channel_id).name.split('-'))
                        await bot.get_channel(DISPLAY_CHANNEL_ID).send(
                            f"{channel_name} (-): Không có đáp án"
                        )
                sorted_messages.clear()
                tt_messages.clear()
                    
            except (IndexError, ValueError):
                pass  # Ignore if there's no delay specified or an invalid delay value

            

        # Vuot chuong ngai vat
        elif delay_seconds == 15:
            try:
                # Extract the delay value from the message content
                await asyncio.sleep(delay_seconds)  # Wait for the specified delay
                await bot.get_channel(DISPLAY_CHANNEL_ID).send("HẾT THỜI GIAN!")
                for source_channel_id in SOURCE_CHANNEL_IDS:
                    await bot.get_channel(source_channel_id).send("HẾT THỜI GIAN!")
            
                # Check if there's no message in a specific channel
                for source_channel_id in SOURCE_CHANNEL_IDS:
                    if source_channel_id not in vcnv_messages:
                        channel_name = ' '.join(word.capitalize() for word in bot.get_channel(source_channel_id).name.split('-'))
                        await bot.get_channel(DISPLAY_CHANNEL_ID).send(
                            f"{channel_name}: Không có đáp án"
                        )
                    else:
                        message = vcnv_messages[source_channel_id]
                        channel_name = ' '.join(word.capitalize() for word in message['channel_name'].split('-'))
                        await bot.get_channel(DISPLAY_CHANNEL_ID).send(
                            f"{channel_name}: {message['content'].upper()}"
                        )
                vcnv_messages.clear()
            except (IndexError, ValueError):
                pass  # Ignore if there's no delay specified or an invalid delay value
        
        
        else:
            try:
                # Extract the delay value from the message content
                await asyncio.sleep(delay_seconds)  # Wait for the specified delay
                await bot.get_channel(DISPLAY_CHANNEL_ID).send("HẾT THỜI GIAN!")
                for source_channel_id in SOURCE_CHANNEL_IDS:
                    await bot.get_channel(source_channel_id).send("HẾT THỜI GIAN!")
            except (IndexError, ValueError):
                pass 



# Replace BOT_TOKEN, SOURCE_CHANNEL_IDS, TARGET_CHANNEL_ID, and MY_TOKEN with your actual values
bot.run(MY_TOKEN)
