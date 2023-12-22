from __utils__ import *

async def display_vcnv_answers(vcnv_messages):
    await bot.get_channel(DISPLAY_CHANNEL_ID).send("---------------ĐÁP ÁN CỦA CÁC THÍ SINH---------------")
    # Check if there's no message in a specific channel
    for source_channel_id in SOURCE_CHANNEL_IDS:
        if source_channel_id not in vcnv_messages:
            channel_name = ' '.join(word.capitalize() for word in bot.get_channel(source_channel_id).name.split('-'))
            await bot.get_channel(DISPLAY_CHANNEL_ID).send(f"{channel_name}:")
        else:
            message = vcnv_messages[source_channel_id]
            channel_name = ' '.join(word.capitalize() for word in message['channel_name'].split('-'))
            if message['content'].upper() == "/CNV":
                await bot.get_channel(DISPLAY_CHANNEL_ID).send(f"{channel_name}:")
            else:
                await bot.get_channel(DISPLAY_CHANNEL_ID).send(
                    f"{channel_name}: {message['content'].upper()}"
                )

async def display_tt_answers(tt_messages, start_time):
    await bot.get_channel(DISPLAY_CHANNEL_ID).send("---------------ĐÁP ÁN CỦA CÁC THÍ SINH---------------")
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


async def display_hs_answers(hs_messages):
    for source_channel_id in SOURCE_CHANNEL_IDS:
        if source_channel_id not in hs_messages:
            channel_name = ' '.join(word.capitalize() for word in bot.get_channel(source_channel_id).name.split('-'))
            await bot.get_channel(DISPLAY_CHANNEL_ID).send(
                f"{channel_name} không giải được mật mã vòng Hồi Sức"
            )
        else:
            message = hs_messages[source_channel_id]
            channel_name = ' '.join(word.capitalize() for word in message['channel_name'].split('-'))
            await bot.get_channel(DISPLAY_CHANNEL_ID).send(
                f"{channel_name} không giải được mật mã vòng Hồi Sức"
            ) 