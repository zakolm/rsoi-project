import asyncio

import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(1000):
            tasks.append(asyncio.create_task(session.get('https://example.com')))
        responses = await asyncio.gather(*tasks)
    resps_ok = [resp.ok for resp in responses]
    print(resps_ok)


if __name__ == '__main__':
    asyncio.run(main())
