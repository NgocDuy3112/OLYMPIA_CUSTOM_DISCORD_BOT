from functions import *

@bot.command(name='start')
async def start(ctx, round):
    global HAS_PINGED_FIRST
    global DISPLAY_PAUSED
    global vcnv_messages
    global tt_messages
    global hs_messages
    global vd_messages
    global chp_messages

    HAS_PINGED_FIRST = False
    start_time = datetime.now().astimezone()

    # Vuot chuong ngai vat
    if round == "vcnv":
        delay_seconds = 15
        try:
            # Extract the delay value from the message content
            for source_channel_id in SOURCE_CHANNEL_IDS:
                await bot.get_channel(source_channel_id).send(START_STR)
            await asyncio.sleep(delay_seconds)  # Wait for the specified delay
            for source_channel_id in SOURCE_CHANNEL_IDS:
                await bot.get_channel(source_channel_id).send(TIME_UP_STR)
            if not DISPLAY_PAUSED:
                await display_vcnv_answers(vcnv_messages)   
            vcnv_messages.clear()
            
        except (IndexError, ValueError):
            pass  # Ignore if there's no delay specified or an invalid delay value
    
    # Tang toc
    elif round in ["tt1", "tt2"]:
        delay_seconds = 20 if round == "tt1" else 40
        try:
            # Extract the delay value from the message content
            for source_channel_id in SOURCE_CHANNEL_IDS:
                await bot.get_channel(source_channel_id).send(START_STR)
            await asyncio.sleep(delay_seconds)
            for source_channel_id in SOURCE_CHANNEL_IDS:
                await bot.get_channel(source_channel_id).send(TIME_UP_STR)
            await display_tt_answers(tt_messages, start_time)
            tt_messages.clear()

        except (IndexError, ValueError):
            pass  # Ignore if there's no delay specified or an invalid delay value
    
    # Hoi suc
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
            
            await display_hs_answers(hs_messages)
            hs_messages.clear()

        except (IndexError, ValueError):
            pass  # Ignore if there's no delay specified or an invalid delay value
    
    
    # Ve dich + CHP
    elif round in ["vd", "chp"]:
        delay_seconds = 5 if round == "vd" else 15
        try:
            for source_channel_id in SOURCE_CHANNEL_IDS:
                await bot.get_channel(source_channel_id).send(START_PING_STR)

            # Extract the delay value from the message content
            await asyncio.sleep(delay_seconds)  # Wait for the specified delay
            
            for source_channel_id in SOURCE_CHANNEL_IDS:
                await bot.get_channel(source_channel_id).send(TIME_UP_STR)

        except (IndexError, ValueError):
            pass
    else:
        pass



@bot.command(name='alert')
async def alert(ctx, *args):
    CHANNEL_IDS = SOURCE_CHANNEL_IDS + [DISPLAY_CHANNEL_ID]
    try:
        for source_channel_id in CHANNEL_IDS:
            await bot.get_channel(source_channel_id).send(' '.join(args))
    except (IndexError, ValueError):
        await bot.get_channel(DISPLAY_CHANNEL_ID).send("Bạn bị thiếu câu thông báo kìa!")



@bot.command(name='cont')
async def cont(ctx):
    global DISPLAY_PAUSED
    DISPLAY_PAUSED = False
    display_vcnv_answers(vcnv_messages)



@bot.command(name='delete')
async def delete(ctx, num_messages):
    if CLEAR_COMMAND_ROLE_ID in [role.id for role in ctx.author.roles]:
        try:
            DELETE_CHANNEL_IDS = SOURCE_CHANNEL_IDS + [TARGET_CHANNEL_ID, DISPLAY_CHANNEL_ID]
            num_messages_to_clear = int(num_messages) + 1
            for channel_id_to_clear in DELETE_CHANNEL_IDS:
                channel_to_clear = bot.get_channel(channel_id_to_clear)
                messages_to_clear = [mess async for mess in channel_to_clear.history(limit=num_messages_to_clear)] 
                await channel_to_clear.delete_messages(messages_to_clear)
            await bot.get_channel(DISPLAY_CHANNEL_ID).send(f"Đã xóa {num_messages_to_clear - 1} tin nhắn ở cả 4 kênh!")
        except (IndexError, ValueError):
            await bot.get_channel(DISPLAY_CHANNEL_ID).send("Bạn bị thiếu số lượng tin nhắn cần xóa kìa!")



@bot.command(name='rename')
async def rename(ctx,  *new_names):
    if CLEAR_COMMAND_ROLE_ID in [role.id for role in ctx.author.roles]:
        try:
            # Rename the channels
            for channel_id in SOURCE_CHANNEL_IDS:
                channel = bot.get_channel(channel_id)
                if channel:
                    await channel.edit(name=new_names.pop(0))  
                else:
                    await bot.get_channel(DISPLAY_CHANNEL_ID).send(f"Kênh không tìm thấy.")
            await bot.get_channel(DISPLAY_CHANNEL_ID).send(f"Đã đổi tên.")
        except IndexError:
            await bot.get_channel(DISPLAY_CHANNEL_ID).send("Lệnh bị gõ sai.")
    else:
        await bot.get_channel(DISPLAY_CHANNEL_ID).send("Bạn không có quyền sử dụng lệnh /rename.")



@bot.command(name='block')
async def block(ctx, role_index: int):
    pass
    

@bot.command(name='unblock')
async def block(ctx, role_index: int):
    pass