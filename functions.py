from __utils__ import *
from write_to_ppt import *

def format_seconds_with_zeros(seconds):
    return "{:05.2f}".format(seconds)

async def display_vcnv_answers(vcnv_messages):
    player_index = 1
    # await bot.get_channel(DISPLAY_CHANNEL_ID).send("---------------ĐÁP ÁN CỦA CÁC THÍ SINH---------------")
    # Check if there's no message in a specific channel
    for source_channel_id in SOURCE_CHANNEL_IDS:
        if source_channel_id not in vcnv_messages:
            channel_name = ' '.join(word.capitalize() for word in bot.get_channel(source_channel_id).name.split('-'))
            # await bot.get_channel(DISPLAY_CHANNEL_ID).send(f"{channel_name}:")
            change_shape_content(PPTPresentation, ANSWER_SLIDE["VCNV"], f"Player{player_index}Name", channel_name)
            change_shape_content(PPTPresentation, ANSWER_SLIDE["VCNV"], f"Player{player_index}Answer", "")
        else:
            message = vcnv_messages[source_channel_id]
            channel_name = ' '.join(word.capitalize() for word in message['channel_name'].split('-'))
            if message['content'].lower() == "cnv":
                await bot.get_channel(DISPLAY_CHANNEL_ID).send(f"{channel_name}")
                change_shape_content(PPTPresentation, ANSWER_SLIDE["VCNV"], f"Player{player_index}Name", channel_name)
                change_shape_content(PPTPresentation, ANSWER_SLIDE["VCNV"], f"Player{player_index}Answer", "")
            else:
                answer = message['content'].upper()
                # await bot.get_channel(DISPLAY_CHANNEL_ID).send(f"{channel_name}: {answer}")
                change_shape_content(PPTPresentation, ANSWER_SLIDE["VCNV"], f"Player{player_index}Name", channel_name)
                change_shape_content(PPTPresentation, ANSWER_SLIDE["VCNV"], f"Player{player_index}Answer", answer)
        player_index += 1
    
    await bot.get_channel(DISPLAY_CHANNEL_ID).send("ĐÃ HOÀN THÀNH VIỆC NHẬP ĐÁP ÁN!")
    player_index = 1

async def display_tt_answers(tt_messages, start_time, delay_seconds):
    # await bot.get_channel(DISPLAY_CHANNEL_ID).send("---------------ĐÁP ÁN CỦA CÁC THÍ SINH---------------")
    sorted_messages = sorted(tt_messages.items(), key=lambda x: (x[1]['timestamp'] - start_time).total_seconds())
    shape_index = 1

    for source_channel_id, last_message in sorted_messages:
        answer = last_message['content'].upper()
        timestamp = last_message['timestamp']
        time_difference = (timestamp - start_time).total_seconds()
        if time_difference > delay_seconds: time_difference = delay_seconds
        channel_name = ' '.join(word.capitalize() for word in last_message['channel_name'].split('-'))
        
        change_shape_content(PPTPresentation, ANSWER_SLIDE["TT"], f"Player{shape_index}Name", channel_name)
        change_shape_content(PPTPresentation, ANSWER_SLIDE["TT"], f"Player{shape_index}Time", format_seconds_with_zeros(time_difference))
        change_shape_content(PPTPresentation, ANSWER_SLIDE["TT"], f"Player{shape_index}Answer", answer)
        shape_index += 1

    # Check if there's no message in a specific channel
    for source_channel_id in SOURCE_CHANNEL_IDS:
        if source_channel_id not in tt_messages:
            channel_name = ' '.join(word.capitalize() for word in bot.get_channel(source_channel_id).name.split('-'))
            
            change_shape_content(PPTPresentation, ANSWER_SLIDE["TT"], f"Player{shape_index}Name", channel_name)
            change_shape_content(PPTPresentation, ANSWER_SLIDE["TT"], f"Player{shape_index}Time", "")
            change_shape_content(PPTPresentation, ANSWER_SLIDE["TT"], f"Player{shape_index}Answer", "")
            shape_index += 1
    
    await bot.get_channel(DISPLAY_CHANNEL_ID).send("ĐÃ HOÀN THÀNH VIỆC NHẬP ĐÁP ÁN!")
    shape_index = 1


async def display_hs_answers(hs_messages, start_time, delay_seconds):
    # await bot.get_channel(DISPLAY_CHANNEL_ID).send("---------------ĐÁP ÁN CỦA CÁC THÍ SINH---------------")
    sorted_messages = sorted(hs_messages.items(), key=lambda x: (x[1]['timestamp'] - start_time).total_seconds())
    shape_index = 1

    for source_channel_id, last_message in sorted_messages:
        answer = last_message['content'].upper()
        timestamp = last_message['timestamp']
        time_difference = (timestamp - start_time).total_seconds()
        if time_difference > delay_seconds: time_difference = delay_seconds
        channel_name = ' '.join(word.capitalize() for word in last_message['channel_name'].split('-'))
        change_shape_content(PPTPresentation, ANSWER_SLIDE["HS"], f"Player{shape_index}Name", channel_name)
        change_shape_content(PPTPresentation, ANSWER_SLIDE["HS"], f"Player{shape_index}Time", format_seconds_with_zeros(time_difference))
        change_shape_content(PPTPresentation, ANSWER_SLIDE["HS"], f"Player{shape_index}Answer", answer)
        shape_index += 1

    # Check if there's no message in a specific channel
    for source_channel_id in SOURCE_CHANNEL_IDS:
        if source_channel_id not in hs_messages:
            channel_name = ' '.join(word.capitalize() for word in bot.get_channel(source_channel_id).name.split('-'))
            change_shape_content(PPTPresentation, ANSWER_SLIDE["HS"], f"Player{shape_index}Name", channel_name)
            change_shape_content(PPTPresentation, ANSWER_SLIDE["HS"], f"Player{shape_index}Time", "")
            change_shape_content(PPTPresentation, ANSWER_SLIDE["HS"], f"Player{shape_index}Answer", "")
            shape_index += 1
    
    await bot.get_channel(DISPLAY_CHANNEL_ID).send("ĐÃ HOÀN THÀNH VIỆC NHẬP ĐÁP ÁN!")
    shape_index = 1