from __utils__ import *
from bot_commands import *

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.event
async def on_message(message):
    global HAS_PINGED_FIRST
    global DISPLAY_PAUSED
    
    global CURRENT_CONTEXT
    global QUESTION_COUNT
    
    global kd_messages
    global vcnv_messages
    global tt_messages
    global hs_messages
    global vd_messages
    global chp_messages
    

    if message.author == bot.user: return

    # Check if the message is from source channels
    if message.channel.id in SOURCE_CHANNEL_IDS:
        # Record the last message details (timestamp, content, channel object)
        kd_messages[message.channel.id] = {
            'content': message.content,
            'channel_name': message.channel.name
        }
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

        if CURRENT_CONTEXT == "vcnv" and str.lower(vcnv_messages[message.channel.id]['content']) == "cnv":
            channel_name = ' '.join(word.capitalize() for word in bot.get_channel(message.channel.id).name.split('-'))
            await bot.get_channel(DISPLAY_CHANNEL_ID).send(f"VƯỢT CHƯỚNG NGẠI VẬT: {channel_name} có tín hiệu trả lời Chướng ngại vật!")
            await bot.get_channel(message.channel.id).send(f"Bạn đã bấm chuông giành quyền trả lời Chướng ngại vật! Bạn KHÔNG ĐƯỢC PHÉP tiếp tục tham gia vòng thi này!")
            DISPLAY_PAUSED = True
        
        if CURRENT_CONTEXT == "hs" and hs_messages[message.channel.id]['content'].upper() == HOI_SUC_KEY.upper():
            channel_name = ' '.join(word.capitalize() for word in bot.get_channel(message.channel.id).name.split('-'))
            await bot.get_channel(message.channel.id).send(f"HỒI SỨC: Bạn đã giải đúng mật mã! Mời bạn dừng nhập đáp án!")
            await bot.get_channel(DISPLAY_CHANNEL_ID).send(f"HỒI SỨC: {channel_name} đã giải đúng mật mã!")
        
        if not HAS_PINGED_FIRST and CURRENT_CONTEXT == "kd" and kd_messages[message.channel.id]['content'] == ",":
            channel_name = ' '.join(word.capitalize() for word in bot.get_channel(message.channel.id).name.split('-'))
            await bot.get_channel(DISPLAY_CHANNEL_ID).send(f"KHỞI ĐỘNG - Câu hỏi số {QUESTION_COUNT}: {channel_name} giành được quyền trả lời câu hỏi này!\n")
            await bot.get_channel(message.channel.id).send("KHỞI ĐỘNG: Bạn đã giành được quyền trả lời câu hỏi này!")
            HAS_PINGED_FIRST = True
            QUESTION_COUNT += 1
            
        if not HAS_PINGED_FIRST and CURRENT_CONTEXT in ["vd1", "vd2", "vd3", "vd4"] and vd_messages[message.channel.id]['content'] == ".":
            channel_name = ' '.join(word.capitalize() for word in bot.get_channel(message.channel.id).name.split('-'))
            await bot.get_channel(DISPLAY_CHANNEL_ID).send(f"VỀ ĐÍCH: {channel_name} giành được quyền trả lời câu hỏi này!\n")
            await bot.get_channel(message.channel.id).send("VỀ ĐÍCH: Bạn đã giành được quyền trả lời câu hỏi Về đích này!")
            HAS_PINGED_FIRST = True
        
        if not HAS_PINGED_FIRST and CURRENT_CONTEXT == "chp" and chp_messages[message.channel.id]['content'] == ";":
            channel_name = ' '.join(word.capitalize() for word in bot.get_channel(message.channel.id).name.split('-'))
            await bot.get_channel(DISPLAY_CHANNEL_ID).send(f"CÂU HỎI PHỤ - Câu hỏi số {QUESTION_COUNT}: {channel_name} giành được quyền trả lời câu hỏi này!\n")
            await bot.get_channel(message.channel.id).send(
                "CÂU HỎI PHỤ: Bạn đã giành được quyền trả lời câu hỏi này! Bạn KHÔNG ĐƯỢC PHÉP tiếp tục tham gia vòng thi này!"
            )
            HAS_PINGED_FIRST = True
            QUESTION_COUNT += 1

    # Check if the message is in the target channel and starts with '/start'
    elif message.channel.id == TARGET_CHANNEL_ID:
        # Check if the message is a command and update the current context
        if message.content.startswith("/start"):
            command = message.content.split()[1].lower()  # Extract the command
            CURRENT_CONTEXT = command
        else:
            CURRENT_CONTEXT = None
        
        HAS_PINGED_FIRST = False
        DISPLAY_PAUSED = False
        await bot.process_commands(message)

    

if __name__ == "__main__":
    bot.run(MY_TOKEN)