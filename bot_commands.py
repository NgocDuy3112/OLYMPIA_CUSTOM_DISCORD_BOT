from functions import *

@bot.command(name='start')
async def start(ctx, round):
    global HAS_PINGED_FIRST
    global DISPLAY_PAUSED
    
    global kd_messages
    global vcnv_messages
    global tt_messages
    global hs_messages
    global vd_messages
    global chp_messages
    

    # Vuot chuong ngai vat
    if round == "vcnv":
        delay_seconds = 15
        try:
            # Extract the delay value from the message content
            tasks = []
            for source_channel_id in SOURCE_CHANNEL_IDS:
                channel = bot.get_channel(source_channel_id)
                if channel:
                    tasks.append(channel.send("VƯỢT CHƯỚNG NGẠI VẬT: " + START_STR))
            await asyncio.gather(*tasks)
            
            await asyncio.sleep(delay_seconds)  # Wait for the specified delay
            
            tasks = []
            for source_channel_id in SOURCE_CHANNEL_IDS:
                channel = bot.get_channel(source_channel_id)
                if channel:
                    tasks.append(channel.send("VƯỢT CHƯỚNG NGẠI VẬT: " + TIME_UP_STR))
            await asyncio.gather(*tasks)
            
            if not DISPLAY_PAUSED:
                await display_vcnv_answers(vcnv_messages)   
            vcnv_messages.clear()
            
        except (IndexError, ValueError):
            pass  # Ignore if there's no delay specified or an invalid delay value
    
    # Tang toc
    elif round in ["tt1", "tt2"]:
        delay_seconds = 20 if round == "tt1" else 40
        try:
            tasks = []
            # Extract the delay value from the message content
            for source_channel_id in SOURCE_CHANNEL_IDS:
                channel = bot.get_channel(source_channel_id)
                if channel:
                    tasks.append(channel.send("TĂNG TỐC: " + START_PING_STR))
            await asyncio.gather(*tasks)
            
            start_time = datetime.now().astimezone()
            await asyncio.sleep(delay_seconds)
            
            tasks = []
            for source_channel_id in SOURCE_CHANNEL_IDS:
                channel = bot.get_channel(source_channel_id)
                if channel:
                    tasks.append(channel.send("TĂNG TỐC: " + TIME_UP_STR))
            await asyncio.gather(*tasks)
            
            await display_tt_answers(tt_messages, start_time, delay_seconds)
            tt_messages.clear()

        except (IndexError, ValueError):
            pass  # Ignore if there's no delay specified or an invalid delay value
    
    # Hoi suc
    elif round == "hs":
        delay_seconds = 60
        try:
            tasks = []
            # Extract the delay value from the message content
            tasks.append(bot.get_channel(DISPLAY_CHANNEL_ID).send(START_STR))
            # Extract the delay value from the message content
            for source_channel_id in SOURCE_CHANNEL_IDS:
                channel = bot.get_channel(source_channel_id)
                if channel:
                    tasks.append(channel.send("HỒI SỨC: " + START_STR))
            await asyncio.gather(*tasks)

            await asyncio.sleep(delay_seconds)  # Wait for the specified delay

            tasks = []
            tasks.append(bot.get_channel(DISPLAY_CHANNEL_ID).send(TIME_UP_STR))
            for source_channel_id in SOURCE_CHANNEL_IDS:
                channel = bot.get_channel(source_channel_id)
                if channel:
                    tasks.append(channel.send("HỒI SỨC: " + TIME_UP_STR))
            await asyncio.gather(*tasks)
            
            await display_hs_answers(hs_messages)
            hs_messages.clear()

        except (IndexError, ValueError):
            pass  # Ignore if there's no delay specified or an invalid delay value
    
    
    # Ve dich + CHP
    elif round in ["kd", "chp"]:
        global QUESTION_COUNT
        delay_seconds = 5 if round == "kd" else 15
        
        STR = "KHỞI ĐỘNG - " if round == "kd" else "CÂU HỎI PHỤ - "
        try:
            tasks = []
            for source_channel_id in SOURCE_CHANNEL_IDS:
                channel = bot.get_channel(source_channel_id)
                if channel:
                    tasks.append(channel.send(STR + "Câu hỏi số " + str(QUESTION_COUNT) + ": " + START_PING_STR))
            await asyncio.gather(*tasks)

            # Extract the delay value from the message content
            await asyncio.sleep(delay_seconds)  # Wait for the specified delay

            tasks = []
            for source_channel_id in SOURCE_CHANNEL_IDS:
                channel = bot.get_channel(source_channel_id)
                if channel:
                    tasks.append(channel.send(STR + "Câu hỏi số " + str(QUESTION_COUNT) + ": " + TIME_UP_STR))
            await asyncio.gather(*tasks)
                    
            QUESTION_COUNT += 1
            
            if round == "kd":
                kd_messages.clear()
            else:
                chp_messages.clear()

        except (IndexError, ValueError):
            pass
            
        
    elif round in ["vd1", "vd2", "vd3", "vd4"]:
        delay_seconds = 5
        block_player = int(round[-1])
        try:
            tasks = []
            for source_channel_id in SOURCE_CHANNEL_IDS:
                if source_channel_id != SOURCE_CHANNEL_IDS[block_player - 1]:
                    channel = bot.get_channel(source_channel_id)
                    if channel:
                        tasks.append(channel.send("VỀ ĐÍCH: " + START_PING_STR))
            await asyncio.gather(*tasks)

            # Extract the delay value from the message content
            await asyncio.sleep(delay_seconds)  # Wait for the specified delay
            
            tasks = []
            for source_channel_id in SOURCE_CHANNEL_IDS:
                if source_channel_id != SOURCE_CHANNEL_IDS[block_player - 1]:
                    channel = bot.get_channel(source_channel_id)
                    if channel:
                        tasks.append(channel.send("VỀ ĐÍCH: " + TIME_UP_STR))
            await asyncio.gather(*tasks)
            vd_messages.clear()

        except (IndexError, ValueError):
            pass
        
    else:
        pass

@bot.command(name='restart')
async def restart(ctx):
    global QUESTION_COUNT
    QUESTION_COUNT = 1

@bot.command(name='alert')
async def alert(ctx, *args):
    CHANNEL_IDS = SOURCE_CHANNEL_IDS + [DISPLAY_CHANNEL_ID]
    try:
        for source_channel_id in CHANNEL_IDS:
            await bot.get_channel(source_channel_id).send(' '.join(args))
    except (IndexError, ValueError):
        pass


@bot.command(name='delete')
async def delete(ctx, num_messages):
    if CLEAR_COMMAND_ROLE_ID in [role.id for role in ctx.author.roles]:
        try:
            DELETE_CHANNEL_IDS = SOURCE_CHANNEL_IDS + [TARGET_CHANNEL_ID, DISPLAY_CHANNEL_ID]
            num_messages_to_clear = int(num_messages) + 1
            tasks = []
            for channel_id_to_clear in DELETE_CHANNEL_IDS:
                channel_to_clear = bot.get_channel(channel_id_to_clear)
                if channel_to_clear:
                    messages_to_clear = [mess async for mess in channel_to_clear.history(limit=num_messages_to_clear)] 
                    tasks.append(channel_to_clear.delete_messages(messages_to_clear))
            await asyncio.gather(*tasks)
        except (IndexError, ValueError):
            pass



@bot.command(name='rename')
async def rename(ctx, *new_names):
    if CLEAR_COMMAND_ROLE_ID in [role.id for role in ctx.author.roles]:
        try:
            if len(new_names) != len(SOURCE_CHANNEL_IDS):
                return
            
            tasks = []
            for channel_id, new_name in zip(SOURCE_CHANNEL_IDS, new_names):
                channel = bot.get_channel(channel_id)
                if channel:
                    tasks.append(channel.edit(name=new_name))
                else:
                    print(f"Kênh không tìm thấy.")

            # Rename channels simultaneously
            await asyncio.gather(*tasks)
        except IndexError: pass
    else: pass
