from __utils__ import *
from bot_commands import *

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.event
async def on_message(message):
    global HAS_PINGED_FIRST
    global DISPLAY_PAUSED

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
            DISPLAY_PAUSED = True
        
        if hs_messages[message.channel.id]['content'].upper() == HOI_SUC_KEY.upper():
            channel_name = ' '.join(word.capitalize() for word in bot.get_channel(message.channel.id).name.split('-'))
            await bot.get_channel(message.channel.id).send(f"Bạn đã giải đúng mật mã vòng Hồi Sức! Mời bạn dừng nhập đáp án!")
            await bot.get_channel(DISPLAY_CHANNEL_ID).send(f"{channel_name} đã giải đúng mật mã vòng Hồi Sức!")
        
        if not HAS_PINGED_FIRST and vd_messages[message.channel.id]['content'] == "/.":
            HAS_PINGED_FIRST = True
            channel_name = ' '.join(word.capitalize() for word in bot.get_channel(message.channel.id).name.split('-'))
            await bot.get_channel(DISPLAY_CHANNEL_ID).send(f"{channel_name} giành được quyền trả lời câu hỏi này!")
            await bot.get_channel(message.channel.id).send("Bạn đã giành được quyền trả lời câu hỏi Về đích này!")
        
        if not HAS_PINGED_FIRST and chp_messages[message.channel.id]['content'] == "/.":
            HAS_PINGED_FIRST = True
            channel_name = ' '.join(word.capitalize() for word in bot.get_channel(message.channel.id).name.split('-'))
            await bot.get_channel(DISPLAY_CHANNEL_ID).send(f"{channel_name} giành được quyền trả lời câu hỏi phụ này!")
            await bot.get_channel(message.channel.id).send(
                "Bạn đã giành được quyền trả lời câu hỏi phụ này! Bạn KHÔNG ĐƯỢC PHÉP tiếp tục tham gia vòng thi này!"
            )
            

    # Check if the message is in the target channel and starts with '/start'
    elif message.channel.id == TARGET_CHANNEL_ID: 
        await bot.process_commands(message)

    


bot.run(MY_TOKEN)