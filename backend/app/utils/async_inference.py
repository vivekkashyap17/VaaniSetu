import asyncio


async def run_inference_async(
    function,
    *args
):

    loop = asyncio.get_event_loop()

    result = await loop.run_in_executor(
        None,
        lambda: function(*args)
    )

    return result