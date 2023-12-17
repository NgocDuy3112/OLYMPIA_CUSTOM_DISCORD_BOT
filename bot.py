from __utils__ import *

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

vcnv_messages = {}  # Dictionary to store the last message from each source channel
tt_messages = {}  # Dictionary to store the first message from each source channel
hs_messages = {}
vd_messages = {}
chp_messages = {}

HOI_SUC_KEY = "HOISUC"
HAS_PINGED_FIRST = False
START_STR = "THỜI GIAN TRẢ LỜI BẮT ĐẦU!"
START_PING_STR = "THỜI GIAN 5 GIÂY GÕ CHUÔNG BẮT ĐẦU!"
TIME_UP_STR = "HẾT THỜI GIAN!"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

async def wait_for_no_messages(seconds=5):
    await asyncio.sleep(seconds)
    bot.remove_listener(on_message)
    bot.add_listener(on_message)


@bot.event
async def on_message(message):
    global HAS_PINGED_FIRST

    if message.author == bot.user: return

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
        hs_messages[message.channel.id] = {
            'content': message.content,
            'channel_name': message.channel.name
        }
        vd_messages[message.channel.id] = {
            'content': message.content,
            'channel_name': message.channel.name
        }
        chp_messages[message.channel.id] = {
            'content': message.content,
            'channel_name': message.channel.name
        }

        if str.lower(vcnv_messages[message.channel.id]['content']) == "/cnv":
            channel_name = ' '.join(word.capitalize() for word in bot.get_channel(message.channel.id).name.split('-'))
            await bot.get_channel(DISPLAY_CHANNEL_ID).send(f"{channel_name} có tín hiệu trả lời Chướng ngại vật!")
            await bot.get_channel(message.channel.id).send(f"Bạn đã bấm chuông giành quyền trả lời Chướng ngại vật! Bạn KHÔNG ĐƯỢC PHÉP tiếp tục tham gia vòng thi này!")
            bot.remove_listener(on_message)
            await wait_for_no_messages()
        
        if hs_messages[message.channel.id]['content'] == HOI_SUC_KEY:
            channel_name = ' '.join(word.capitalize() for word in bot.get_channel(message.channel.id).name.split('-'))
            await bot.get_channel(message.channel.id).send(f"Bạn đã giải đúng mật mã vòng Hồi Sức! Mời bạn dừng nhập đáp án!")
            await bot.get_channel(DISPLAY_CHANNEL_ID).send(f"{channel_name} đã giải đúng mật mã vòng Hồi Sức!")
            bot.remove_listener(on_message)
            await wait_for_no_messages(60)
        
        if not HAS_PINGED_FIRST and vd_messages[message.channel.id]['content'] == "/.":
            HAS_PINGED_FIRST = True
            channel_name = ' '.join(word.capitalize() for word in bot.get_channel(message.channel.id).name.split('-'))
            await bot.get_channel(DISPLAY_CHANNEL_ID).send(f"{channel_name} giành được quyền trả lời câu hỏi Về đích này!")
            await bot.get_channel(message.channel.id).send(f"Bạn đã giành được quyền trả lời câu hỏi Về đích này!")
            bot.remove_listener(on_message)
            await wait_for_no_messages(5)
        
        if not HAS_PINGED_FIRST and chp_messages[message.channel.id]['content'] == "/.":
            HAS_PINGED_FIRST = True
            channel_name = ' '.join(word.capitalize() for word in bot.get_channel(message.channel.id).name.split('-'))
            await bot.get_channel(DISPLAY_CHANNEL_ID).send(f"{channel_name} giành được quyền trả lời câu hỏi phụ này!")
            await bot.get_channel(message.channel.id).send(f"Bạn đã giành được quyền trả lời câu hỏi phụ này! Bạn KHÔNG ĐƯỢC PHÉP tiếp tục tham gia vòng thi này!")
            bot.remove_listener(on_message)
            await wait_for_no_messages(15)
            

    # Check if the message is in the target channel and starts with '/start'
    elif message.channel.id == TARGET_CHANNEL_ID and message.content.startswith('/start'):
        HAS_PINGED_FIRST = False
        start_time = datetime.now().astimezone()
        round = message.content.split()[1]
        # Tang toc
        if round in ["tt1", "tt2"]:
            delay_seconds = 20 if round == "tt1" else 40
            try:
                # Extract the delay value from the message content
                await bot.get_channel(DISPLAY_CHANNEL_ID).send(START_STR)
                for source_channel_id in SOURCE_CHANNEL_IDS:
                    await bot.get_channel(source_channel_id).send(START_STR)

                await asyncio.sleep(delay_seconds)

                await bot.get_channel(DISPLAY_CHANNEL_ID).send(TIME_UP_STR)
                for source_channel_id in SOURCE_CHANNEL_IDS:
                    await bot.get_channel(source_channel_id).send(TIME_UP_STR)

                sorted_messages = sorted(tt_messages.items(), key=lambda x: (x[1]['timestamp'] - start_time).total_seconds())

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
                tt_messages.clear()  # Wait for the specified delay
                
                    
            except (IndexError, ValueError):
                pass  # Ignore if there's no delay specified or an invalid delay value


        # Vuot chuong ngai vat
        elif round == "vcnv":
            delay_seconds = 15
            try:
                # Extract the delay value from the message content
                await bot.get_channel(DISPLAY_CHANNEL_ID).send(START_STR)
                for source_channel_id in SOURCE_CHANNEL_IDS:
                    await bot.get_channel(source_channel_id).send(START_STR)

                await asyncio.sleep(delay_seconds)  # Wait for the specified delay

                await bot.get_channel(DISPLAY_CHANNEL_ID).send(TIME_UP_STR)
                for source_channel_id in SOURCE_CHANNEL_IDS:
                    await bot.get_channel(source_channel_id).send(TIME_UP_STR)
            
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
        
        elif round == "hs":
            delay_seconds = 60
            try:
                # Extract the delay value from the message content
                await bot.get_channel(DISPLAY_CHANNEL_ID).send(START_STR)
                for source_channel_id in SOURCE_CHANNEL_IDS:
                    await bot.get_channel(source_channel_id).send(START_STR)

                await asyncio.sleep(delay_seconds)  # Wait for the specified delay

                await bot.get_channel(DISPLAY_CHANNEL_ID).send(TIME_UP_STR)
                for source_channel_id in SOURCE_CHANNEL_IDS:
                    await bot.get_channel(source_channel_id).send(TIME_UP_STR)
            
                # Check if there's no message in a specific channel
                for source_channel_id in SOURCE_CHANNEL_IDS:
                    if source_channel_id not in hs_messages:
                        channel_name = ' '.join(word.capitalize() for word in bot.get_channel(source_channel_id).name.split('-'))
                        await bot.get_channel(DISPLAY_CHANNEL_ID).send(
                            f"{channel_name} không giải được mật mã vòng Hồi Sức"
                        )
                hs_messages.clear()

            except (IndexError, ValueError):
                pass  # Ignore if there's no delay specified or an invalid delay value
        
        
        elif round in ["vd", "chp"]:
            delay_seconds = 5 if round == "vd" else 15
            try:
                for source_channel_id in SOURCE_CHANNEL_IDS:
                    await bot.get_channel(source_channel_id).send(START_PING_STR)

                # Extract the delay value from the message content
                await asyncio.sleep(delay_seconds)  # Wait for the specified delay

                await bot.get_channel(DISPLAY_CHANNEL_ID).send(TIME_UP_STR)
                for source_channel_id in SOURCE_CHANNEL_IDS:
                    await bot.get_channel(source_channel_id).send(TIME_UP_STR)

            except (IndexError, ValueError):
                pass
        

        else:
            pass


    elif message.channel.id == TARGET_CHANNEL_ID and message.content.startswith('/alert'):
        CHANNEL_IDS = SOURCE_CHANNEL_IDS + [DISPLAY_CHANNEL_ID]
        for source_channel_id in CHANNEL_IDS:
            await bot.get_channel(source_channel_id).send(' '.join(message.content.split()[1:]))
        


# Replace BOT_TOKEN, SOURCE_CHANNEL_IDS, TARGET_CHANNEL_ID, and MY_TOKEN with your actual values
bot.run(MY_TOKEN)